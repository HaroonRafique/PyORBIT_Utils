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
slicebyslice = s['SliceBySlice']        # Slice by slice space charge
twopointfived = s['TwoPointFiveD']        # 2.5D space charge

if twopointfived: slicebyslice = 0

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
if slicebyslice:
	from spacecharge import SpaceChargeCalcSliceBySlice2D
elif twopointfived:
	from spacecharge import SpaceChargeCalc2p5D
	
from orbit.space_charge.sc2p5d import scAccNodes, scLatticeModifications
from spacecharge import SpaceChargeCalcAnalyticGaussian
from spacecharge import InterpolatedLineDensityProfile

from lib.output_dictionary import *
from lib.pyOrbit_GenerateInitialDistribution import *
from lib.save_bunch_as_matfile import *
from lib.suppress_stdout import suppress_STDOUT
readScriptPTC_noSTDOUT = suppress_STDOUT(readScriptPTC)

# MPI stuff
#-----------------------------------------------------------------------
comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
rank = orbit_mpi.MPI_Comm_rank(comm)
print 'Start on MPI process: ', rank

# Create folder structure
#-----------------------------------------------------------------------
print '\nmkdir on MPI process: ', rank
from lib.mpi_helpers import mpi_mkdir_p
mpi_mkdir_p('input')
mpi_mkdir_p('bunch_output')
mpi_mkdir_p('output')
mpi_mkdir_p('lost')

# Dictionary for simulation status
#-----------------------------------------------------------------------
import pickle # HAVE TO CLEAN THIS FILE BEFORE RUNNING A NEW SIMULATION
status_file = 'input/simulation_status.pkl'
if not os.path.exists(status_file):
        sts = {'turn': -1}
else:
        with open(status_file) as fid:
                sts = pickle.load(fid)

# Generate Lattice (MADX + PTC) - Use MPI to run on only one 'process'
#-----------------------------------------------------------------------
print '\nStart MADX on MPI process: ', rank
PTC_File = "PTC-PyORBIT_flat_file.flt"

if not rank:
	if os.path.exists(PTC_File):
		print '\nUsing existing PTC flat file'
	else:
		print '\nFlat file not found. Using MAD-X to generate a new flat file'
		os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < Flat_file.madx")
orbit_mpi.MPI_Barrier(comm)

# Generate PTC RF table
#-----------------------------------------------------------------------
print '\nstart RF file on MPI process: ', rank
from lib.write_ptc_table import write_RFtable
from simulation_parameters import RFparameters as RF 
write_RFtable('input/RF_table.ptc', *[RF[k] for k in ['harmonic_factors','time','Ekin_GeV','voltage_MV','phase']])

# Initialize a Teapot-Style PTC lattice
#-----------------------------------------------------------------------
print '\nstart PTC Flat file on MPI process: ', rank
Lattice = PTC_Lattice("PS")
Lattice.readPTC(PTC_File)

readScriptPTC_noSTDOUT('PTC/fringe.ptc')
readScriptPTC_noSTDOUT('PTC/time.ptc')
readScriptPTC_noSTDOUT('PTC/ramp_cavities.ptc')

# Create a dictionary of parameters
#-----------------------------------------------------------------------
print '\nparamsDict on MPI process: ', rank
paramsDict = {}
paramsDict["length"]=Lattice.getLength()/Lattice.nHarm

# Add apertures
#-----------------------------------------------------------------------
print '\nAdd apertures on MPI process: ', rank
position = 0
for node in Lattice.getNodes():
	myaperturenode = TeapotApertureNode(1, 10, 10, position)
	node.addChildNode(myaperturenode, node.ENTRANCE)
	node.addChildNode(myaperturenode, node.BODY)
	node.addChildNode(myaperturenode, node.EXIT)
	position += node.getLength()
	
# Load bunch from previously run simulation
path_to_distn = 'mainbunch_000874.mat'
bunch = bunch_from_matfile(path_to_distn)

lostbunch = Bunch()
bunch.copyEmptyBunchTo(lostbunch)
lostbunch.addPartAttr('ParticlePhaseAttributes')
lostbunch.addPartAttr("LostParticleAttributes")	
saveBunchAsMatfile(lostbunch, "input/lostbunch")
paramsDict["lostbunch"]=lostbunch

# Add space charge
#-----------------------------------------------------------------------
print '\nAdding slice-by-slice space charge nodes on MPI process: ', rank
# Make a SC solver
calcsbs = SpaceChargeCalcSliceBySlice2D(s['GridSizeX'], s['GridSizeY'], s['GridSizeZ'], useLongitudinalKick=s['LongitudinalKick'])
sc_path_length_min = 1E-8
# Add the space charge solver to the lattice as child nodes
sc_nodes = scLatticeModifications.setSC2p5DAccNodes(Lattice, sc_path_length_min, calcsbs)
print '  Installed', len(sc_nodes), 'space charge nodes ...'

# Add tune analysis child node
#-----------------------------------------------------------------------
parentnode_number = 97
parentnode = Lattice.getNodes()[parentnode_number]
Twiss_at_parentnode_entrance = Lattice.getNodes()[parentnode_number-1].getParamsDict()
tunes = TeapotTuneAnalysisNode("tune_analysis")

tunes.assignTwiss(*[Twiss_at_parentnode_entrance[k] for k in ['betax','alphax','etax','etapx','betay','alphay','etay','etapy']])
tunes.assignClosedOrbit(*[Twiss_at_parentnode_entrance[k] for k in ['orbitx','orbitpx','orbity','orbitpy']])
addTeapotDiagnosticsNodeAsChild(Lattice, parentnode, tunes)
bunchtwissanalysis = BunchTwissAnalysis() #Prepare the analysis class that will look at emittances, etc.

# Track one turn
#-----------------------------------------------------------------------

paramsDict["bunch"]= bunch
Lattice.trackBunch(bunch, paramsDict)
bunchtwissanalysis.analyzeBunch(bunch)

from simulation_parameters import parameters as p
p['harmonic_number'] = Lattice.nHarm 
p['phi_s']           = 0
p['gamma']           = bunch.getSyncParticle().gamma()
p['beta']            = bunch.getSyncParticle().beta()
p['energy']          = 1e9 * bunch.mass() * bunch.getSyncParticle().gamma()
p['bunch_length'] = p['bunch_length']

twiss_dict = dict()
twiss_dict['alpha_x'] 			= bunchtwissanalysis.getAlpha(0)
twiss_dict['alpha_y'] 			= bunchtwissanalysis.getAlpha(1)
twiss_dict['beta_x'] 			= bunchtwissanalysis.getBeta(0)
twiss_dict['beta_y'] 			= bunchtwissanalysis.getBeta(1)
twiss_dict['D_x'] 				= bunchtwissanalysis.getDispersion(0)
twiss_dict['D_y'] 				= bunchtwissanalysis.getDispersion(1)
twiss_dict['D_xp'] 				= bunchtwissanalysis.getDispersionDerivative(0)
twiss_dict['D_yp'] 				= bunchtwissanalysis.getDispersionDerivative(1)
twiss_dict['x0'] 				= Lattice.orbitx0
twiss_dict['xp0'] 				= Lattice.orbitpx0
twiss_dict['y0'] 				= Lattice.orbity0
twiss_dict['yp0'] 				= Lattice.orbitpy0
twiss_dict['gamma_transition'] 	= Lattice.gammaT
twiss_dict['circumference']    	= Lattice.getLength()
twiss_dict['length'] 			= Lattice.getLength()/Lattice.nHarm

# Make new distn
print '\ngenerate_initial_distribution on MPI process: ', rank
Particle_distribution_file = generate_initial_distribution_from_tomo_manual_Twiss(p, twiss_dict, 1, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution_file, bunch, p['n_macroparticles'] + 1) #read in only first N_mp particles.

saveBunchAsMatfile(bunch, "bunch_output/mainbunch_Tomo_Twiss_Test")
