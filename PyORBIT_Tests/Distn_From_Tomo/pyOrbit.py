'''
PTC-PyORBIT example script demonstrating:
> Use of PTC and a MAD-X lattice to generate a PTC flat file
> Use of pickle to resume interrupted simulations
> Use of the output dictionary
> Generating the necessary PTC RF table
> Use of measured tomoscope data to generate the initial distribution

Post processing scripts are provided to:
> Plot the initial distribution
> Create a GIF of the longitudinal distribution evolution
> Plot all relevant bunch output

Pre processing scripts are provided to:
> Convert the saved tomoscope data into a format used as input for 
the user defined GenerateInitialDistribution2 functions that create the
initial distribution

In this case the Proton Synchrotron (PS) lattice is used

Requirements (for this script):
Haroon Rafique's PyORBIT libraries found at:
https://github.com/HaroonRafique/PyORBIT_Utils/tree/master/lib
PS lattice and simulation files:
PS/*
Flat_file.madx, simulation_parameters.py, print_flat_file.ptc

found at:
https://github.com/HaroonRafique/PyORBIT_Utils/tree/master/PS_Injection/Simulation/1p3evs_1.6
access to CERN AFS or a local MAD-X installation
'''

import math
import sys
import time
import orbit_mpi
import timeit
import numpy as np
import scipy.io as sio
import os

# Use switches in simulation_parameters.py in current folder
#-------------------------------------------------------------
from simulation_parameters import switches as s
slicebyslice = s['SliceBySlice']        # 2.5D space charge
frozen = s['Frozen']                    # Frozen space charge

if frozen:	slicebyslice=0

# utils
from orbit.utils.orbit_mpi_utils import bunch_orbit_to_pyorbit, bunch_pyorbit_to_orbit
from orbit.utils.consts import mass_proton, speed_of_light, pi

# bunch
from bunch import Bunch
from bunch import BunchTwissAnalysis, BunchTuneAnalysis
from orbit.bunch_utils import ParticleIdNumber

# diagnostics
from orbit.diagnostics import TeapotStatLatsNode, TeapotMomentsNode, TeapotTuneAnalysisNode
from orbit.diagnostics import addTeapotDiagnosticsNodeAsChild
from orbit.diagnostics import addTeapotMomentsNodeSet, addTeapotStatLatsNodeSet

# PTC lattice
from libptc_orbit import *
from ext.ptc_orbit import PTC_Lattice
from ext.ptc_orbit import PTC_Node
from ext.ptc_orbit.ptc_orbit import setBunchParamsPTC, readAccelTablePTC, readScriptPTC
from ext.ptc_orbit.ptc_orbit import updateParamsPTC, synchronousSetPTC, synchronousAfterPTC
from ext.ptc_orbit.ptc_orbit import trackBunchThroughLatticePTC, trackBunchInRangePTC
from orbit.aperture import TeapotApertureNode

# transverse space charge
# Use switches as these conflict
#----------------------------------------------
if frozen:
        from orbit.space_charge.analytical import scAccNodes, scLatticeModifications
        from spacecharge import SpaceChargeCalcAnalyticGaussian
        from spacecharge import GaussianLineDensityProfile
if slicebyslice:
        from orbit.space_charge.sc2p5d import scAccNodes, scLatticeModifications
        from spacecharge import SpaceChargeCalcSliceBySlice2D
        from spacecharge import SpaceChargeCalcAnalyticGaussian
        from spacecharge import InterpolatedLineDensityProfile

from lib.output_dictionary import *
from lib.pyOrbit_GenerateInitialDistribution2 import *
from lib.save_bunch_as_matfile import *

# MPI
# Here we define the communicator 'comm' - as we wish to perform the same
# actions on each mpi process we may use the MPI_COMM_WORLD communicator.
# The rank is the unique numerical identity (name) of each MPI process.
# We use rank 0 to perform actions that should only be executed once.
#-----------------------------------------------------------------------
comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
rank = orbit_mpi.MPI_Comm_rank(comm)
print 'Start on MPI process: ', rank

# Folder Structure
# We already have the folders 'Input', 'lib', and 'PS'
# Input: contains relevent input files
# lib: contains user defined classes and functions
# PS: contains PS lattice files
# input: destination for input files generated within script
# bunch_output: destination for dumped bunch files
# output: destination for the output dictionary file
# lost: destination for dumped lost particle files
#-----------------------------------------------------------------------
print '\nmkdir on MPI process: ', rank
from lib.mpi_helpers import mpi_mkdir_p
mpi_mkdir_p('input')
mpi_mkdir_p('bunch_output')
mpi_mkdir_p('output')
mpi_mkdir_p('lost')

# Dictionary for simulation status
# The pickle file was historically created to allow a simulation to be
# resumed if interrupted. This is particlulary useful when using the 
# HTCondor system at CERN. Though not always needed, it is used here
# as part of the example. The user must make sure that this file does
# not exist when starting a new simulation
#-----------------------------------------------------------------------
import pickle 
# HAVE TO REMOVE THIS FILE BEFORE RUNNING A NEW SIMULATION
status_file = 'input/simulation_status.pkl'
if not os.path.exists(status_file):
        sts = {'turn': -1}
else:
        with open(status_file) as fid:
                sts = pickle.load(fid)

# Generate PTC flat file using PTC in MAD-X
# Here we execute MAD-X on the system using our 'Flat_file.madx' input
# file. 'if not rank' is the same as 'if rank == 0'. We must use an MPI
# barrier so that all MPI processes wait until the flat file (used to 
# create the accelerator model) has been created by MAD-X.
#-----------------------------------------------------------------------
print '\nStart MADX on MPI process: ', rank
if not rank:
	os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < Flat_file.madx")
orbit_mpi.MPI_Barrier(comm)

# PTC RF table
# In order to properly track through RF cavities, PTC requires us to 
# provide an 'RF table' input file. This must be defined in the
# 'simulation_parameters.py' input file.
#-----------------------------------------------------------------------
print '\nstart RF file on MPI process: ', rank
from lib.write_ptc_table import write_RFtable
from simulation_parameters import RFparameters as RF 
write_RFtable('input/RF_table.ptc', *[RF[k] for k in ['harmonic_factors','time','Ekin_GeV','voltage_MV','phase']])


# Initialize a Teapot-Style PTC lattice
# Here we use the generated flat file to define the lattice in PyORBIT.
# Note that it is imperative to use the 'time.ptc' so that PTC tracks
# using the correct co-ordinates.
#-----------------------------------------------------------------------
print '\nstart PTC Flat file on MPI process: ', rank
PTC_File = "SPACE_CHARGE_STUDIES_INJECTION.flt"
Lattice = PTC_Lattice("PS")
Lattice.readPTC(PTC_File)

readScriptPTC('Input/fringe.txt')
readScriptPTC('Input/time.ptc')
readScriptPTC('Input/ramp_cavities.ptc')

# Parameter Dictionary
# This is a user defined dictionary used to output bunch data, for
# example the emittances, bunch length, and intensity, are all contained
# within this file. All parameters are defined by the user either in 
# functions or using existing PyORBIT functionality.
#-----------------------------------------------------------------------
print '\nparamsDict on MPI process: ', rank
paramsDict = {}
paramsDict["length"]=Lattice.getLength()/Lattice.nHarm

# Add apertures
# PyORBIT requires that we create an aperture, but the apertures from
# the flat file will be used. This step is necessary but the defined
# aperture is not used and therefore not important.
#-----------------------------------------------------------------------
print '\nAdd apertures on MPI process: ', rank
position = 0
for node in Lattice.getNodes():
	myaperturenode = TeapotApertureNode(1, 10, 10, position)
	node.addChildNode(myaperturenode, node.ENTRANCE)
	node.addChildNode(myaperturenode, node.BODY)
	node.addChildNode(myaperturenode, node.EXIT)
	position += node.getLength()

# Make a bunch and import relevant parameters for it
# First we check the pickle file - if the turn is greater than 0 we will
# load parameters etc from there. If not, we use the parameters from the
# lattice and the simulation_parameters.py input file (defined by the
# user).
#-----------------------------------------------------------------------
if sts['turn'] < 0:
	print '\nBunches on MPI process: ', rank
	bunch = Bunch()
	setBunchParamsPTC(bunch)

	from simulation_parameters import parameters as p
	p['harmonic_number'] = Lattice.nHarm 
	p['phi_s']           = 0
	p['gamma']           = bunch.getSyncParticle().gamma()
	p['beta']            = bunch.getSyncParticle().beta()
	p['energy']          = 1e9 * bunch.mass() * bunch.getSyncParticle().gamma()
	p['bunch_length'] = p['blength_rms']/speed_of_light/bunch.getSyncParticle().beta()*4
	kin_Energy = bunch.getSyncParticle().kinEnergy()

	print '\nbunch_orbit_to_pyorbit on MPI process: ', rank
	for i in p:
		print '\t', i, '\t = \t', p[i]

# Create the initial distribution
# In this case we are importing the longitudinal distribution from a 
# measured tomoscope file. This is in the format given by the 
# proton synchrotron / proton synchrotron booster tomoscopes at CERN
# used and tested at the end of run II of the LHC (October 2018).
# The functions used are detailed in the lib/GenerateInitialDistribution2.py
# user defined library file. After generating the distribution it must
# be converted to the correct format using the function
# bunch_orbit_to_pyorbit.
#-----------------------------------------------------------------------
	print '\ngenerate_initial_distribution on MPI process: ', rank
	if s['ImportFromTomo']:		
			Particle_distribution = generate_initial_distribution_from_tomo(p, 1, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
	else:
		Particle_distribution = generate_initial_distribution(p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')

	print '\bunch_orbit_to_pyorbit on MPI process: ', rank
	bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution, bunch, p['n_macroparticles'] + 1) #read in only first N_mp particles.
	
# Add Macrosize and particle ID to bunch
#-----------------------------------------------------------------------
	bunch.addPartAttr("macrosize")
	map(lambda i: bunch.partAttrValue("macrosize", i, 0, p['macrosize']), range(bunch.getSize()))
	ParticleIdNumber().addParticleIdNumbers(bunch) # Give them unique number IDs

# Dump and save bunch as Matfile
#-----------------------------------------------------------------------
	bunch.dumpBunch("input/mainbunch_start.dat")
	saveBunchAsMatfile(bunch, "bunch_output/mainbunch_-000001")
	saveBunchAsMatfile(bunch, "input/mainbunch")
	sts['mainbunch_file'] = "input/mainbunch"

# Create empty lost bunch to store lost particles when tracking
#-----------------------------------------------------------------------
	lostbunch = Bunch()
	bunch.copyEmptyBunchTo(lostbunch)
	lostbunch.addPartAttr('ParticlePhaseAttributes')
	lostbunch.addPartAttr("LostParticleAttributes")	
	saveBunchAsMatfile(lostbunch, "input/lostbunch")
	sts['lostbunch_file'] = "input/lostbunch"

# Add items to pickle parameters
#-----------------------------------------------------------------------
	sts['turns_max'] = p['turns_max']
	sts['turns_update'] = p['turns_update']
	sts['turns_print'] = p['turns_print']
	sts['circumference'] = p['circumference']
	if frozen:
		sts['sc_params1'] = {'intensity': p['intensity'],
											 'epsn_x':    p['epsn_x'],
											 'epsn_y':    p['epsn_y'],
											 'dpp_rms':   p['dpp_rms']}

bunch = bunch_from_matfile(sts['mainbunch_file'])
lostbunch = bunch_from_matfile(sts['lostbunch_file'])
paramsDict["lostbunch"]=lostbunch
paramsDict["bunch"]= bunch

#############################-------------------########################
#############################	SPACE CHARGE	########################
#############################-------------------########################
# In this example we have turned space charge off (see the 
# simulation parameters file - where the frozen and slice_by_slice 
# values are set to 0. The following is kept for completeness but not
# detailed here.

# Add space charge nodes - FROZEN
#----------------------------------------------------
if frozen:
	LineDensity=GaussianLineDensityProfile(p['blength_rms'])
	print '\nSetting up the space charge calculations ...'
	# Make a SC solver using frozen potential
	sc_path_length_min = s['MinPathLength']
	sc_params1 = {'intensity': p['intensity'], 'epsn_x': p['epsn_x'], 'epsn_y': p['epsn_y'], 'dpp_rms': p['dpp_rms'], 'LineDensity': LineDensity}
	space_charge_solver1 = SpaceChargeCalcAnalyticGaussian(*[sc_params1[k] for k in ['intensity','epsn_x','epsn_y','dpp_rms','LineDensity']])
	print dir(scLatticeModifications)
	sc_nodes1 = scLatticeModifications.setSCanalyticalAccNodes(Lattice, sc_path_length_min, space_charge_solver1)
	print 'Installed %i space charge nodes'%(len(sc_nodes1))

# Add space charge nodes
#----------------------------------------------------
if slicebyslice:
	print '\nAdding space charge nodes on MPI process: ', rank
	# Make a SC solver
	sizeX = s['GridSizeX']
	sizeY = s['GridSizeY']
	sizeZ = s['GridSizeZ']  # Number of longitudinal slices in the 2.5D solver
	calcsbs = SpaceChargeCalcSliceBySlice2D(sizeX,sizeY,sizeZ)
	sc_path_length_min = 1E-8
	# Add the space charge solver to the lattice as child nodes
	sc_nodes = scLatticeModifications.setSC2p5DAccNodes(Lattice, sc_path_length_min, calcsbs)
	print '  Installed', len(sc_nodes), 'space charge nodes ...'


# Add tune analysis child node
# This is used to calculate various parameters on a turn-by-turn basis.
# Our output dictionary was defined to store this information for output.
#-----------------------------------------------------
parentnode_number = 97
parentnode = Lattice.getNodes()[parentnode_number]
Twiss_at_parentnode_entrance = Lattice.getNodes()[parentnode_number-1].getParamsDict()
tunes = TeapotTuneAnalysisNode("tune_analysis")

tunes.assignTwiss(*[Twiss_at_parentnode_entrance[k] for k in ['betax','alphax','etax','etapx','betay','alphay','etay','etapy']])
tunes.assignClosedOrbit(*[Twiss_at_parentnode_entrance[k] for k in ['orbitx','orbitpx','orbity','orbitpy']])
addTeapotDiagnosticsNodeAsChild(Lattice, parentnode, tunes)

if frozen:
# Prepare a bunch object to store particle coordinates
#-----------------------------------------------------------------------
	print '\nBunch on MPI process: ', rank
	bunch_tmp = Bunch()
	bunch.copyEmptyBunchTo(bunch_tmp)
	bunch_tmp.addPartAttr('ParticlePhaseAttributes')

# Define twiss analysis and output dictionary
#-----------------------------------------------------------------------
print '\nTWISS on MPI process: ', rank
bunchtwissanalysis = BunchTwissAnalysis() #Prepare the analysis class that will look at emittances, etc.
get_dpp = lambda b, bta: np.sqrt(bta.getCorrelation(5,5)) / (b.getSyncParticle().gamma()*b.mass()*b.getSyncParticle().beta()**2)
get_bunch_length = lambda b, bta: 4 * np.sqrt(bta.getCorrelation(4,4)) / (speed_of_light*b.getSyncParticle().beta())
get_eps_z = lambda b, bta: 1e9 * 4 * pi * bta.getEmittance(2) / (speed_of_light*b.getSyncParticle().beta())

output_file = 'output/output.mat'
output = Output_dictionary()
output.addParameter('turn', lambda: turn)
output.addParameter('intensity', lambda: bunchtwissanalysis.getGlobalMacrosize())
output.addParameter('n_mp', lambda: bunchtwissanalysis.getGlobalCount())
output.addParameter('gamma', lambda: bunch.getSyncParticle().gamma())
output.addParameter('mean_x', lambda: bunchtwissanalysis.getAverage(0))
output.addParameter('mean_xp', lambda: bunchtwissanalysis.getAverage(1))
output.addParameter('mean_y', lambda: bunchtwissanalysis.getAverage(2))
output.addParameter('mean_yp', lambda: bunchtwissanalysis.getAverage(3))
output.addParameter('mean_z', lambda: bunchtwissanalysis.getAverage(4))
output.addParameter('mean_dE', lambda: bunchtwissanalysis.getAverage(5))
output.addParameter('epsn_x', lambda: bunchtwissanalysis.getEmittanceNormalized(0))
output.addParameter('epsn_y', lambda: bunchtwissanalysis.getEmittanceNormalized(1))
output.addParameter('eps_z', lambda: get_eps_z(bunch, bunchtwissanalysis))
output.addParameter('bunchlength', lambda: get_bunch_length(bunch, bunchtwissanalysis))
output.addParameter('dpp_rms', lambda: get_dpp(bunch, bunchtwissanalysis))

if frozen:
	output.addParameter('BE_intensity1', lambda: sc_params1['intensity'])
	output.addParameter('BE_epsn_x1', lambda: sc_params1['epsn_x'])
	output.addParameter('BE_epsn_y1', lambda: sc_params1['epsn_y'])
	output.addParameter('BE_dpp_rms1', lambda: sc_params1['dpp_rms'])

if os.path.exists(output_file):
	output.import_from_matfile(output_file)

# Track
#-----------------------------------------------------------------------
print '\nTracking on MPI process: ', rank

# Loop over 'remaining' turns
for turn in range(sts['turn']+1, sts['turns_max']):
		
	Lattice.trackBunch(bunch, paramsDict)	# Track
	bunchtwissanalysis.analyzeBunch(bunch)  # Analyse twiss and emittance	
	
	# subtract circumference each turn in order to reconstruct the turn number from loss position
	if frozen:
		map(lambda i: lostbunch.partAttrValue("LostParticleAttributes", i, 0, lostbunch.partAttrValue("LostParticleAttributes", i, 0)-p['circumference']), xrange(lostbunch.getSize()))
		bunch.addParticlesTo(bunch_tmp)
					
	if turn in sts['turns_update']:			# Update turn in pickle file
		sts['turn'] = turn

	output.update()							# Update the output dictionary
	
	if turn in sts['turns_print']:			# Print respective output files
		saveBunchAsMatfile(bunch, "input/mainbunch")								# Used to resume via pickle
		saveBunchAsMatfile(bunch, "bunch_output/mainbunch_%s"%(str(turn).zfill(6)))	# Dump bunch
		saveBunchAsMatfile(lostbunch, "lost/lostbunch_%s"%(str(turn).zfill(6)))		# Dump lost particles
		output.save_to_matfile(output_file)		        							# Write to output dictionary
		if not rank:
			with open(status_file, 'w') as fid:
				pickle.dump(sts, fid)		# Write to pickle file
