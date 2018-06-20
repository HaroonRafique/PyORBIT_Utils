#-----------------------------------------------------------------
#	This simulation will take a particle and iterate through the
#	required number of turns until the synchrotron tune of the 
# 	particle meets the requirement.
#	Requires: one particle, no Sextupole or Space Charge.
#-----------------------------------------------------------------

import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()
# ... do something ...


#----------------------------------------------
# Simulation Switches
#----------------------------------------------
from simulation_parameters import switches as s


slicebyslice = s['SliceBySlice']        # 2.5D space charge
frozen = s['Frozen']                    # Frozen space charge
if frozen:
        slicebyslice=0

horizontal = s['Horizontal']            # Horizontal Poincare Distn

import math
import sys
import time
import orbit_mpi
import timeit
import numpy as np
import scipy.io as sio
import os

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
if frozen:
        from orbit.space_charge.analytical import scAccNodes, scLatticeModifications
        from spacecharge import SpaceChargeCalcAnalyticGaussian
        from spacecharge import GaussianLineDensityProfile
        #from spacecharge import InterpolatedLineDensityProfile
if slicebyslice:
        #PIC
        from orbit.space_charge.sc2p5d import scAccNodes, scLatticeModifications
        # ~ from spacecharge import SpaceChargeCalc2p5D, Boundary2D
        # ~ from spacecharge import SpaceChargeCalcSliceBySlice2D
        from spacecharge import SpaceChargeCalcAnalyticGaussian
        from spacecharge import InterpolatedLineDensityProfile


from lib.output_dictionary import *
from lib.pyOrbit_GenerateInitialDistribution2 import *
# ~ from lib.pyOrbit_GenerateMatchedDistribution import *
from lib.save_bunch_as_matfile import *

print "Start ..."
comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
rank = orbit_mpi.MPI_Comm_rank(comm)

#----------------------------------------------
# Create folder structure
#----------------------------------------------
from lib.mpi_helpers import mpi_mkdir_p
mpi_mkdir_p('input')
mpi_mkdir_p('output')
mpi_mkdir_p('lost')


#----------------------------------------------
# Generate Lattice (MADX + PTC)
#----------------------------------------------
if not rank:
	# ~ os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < Flat_file.madx")
	os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < SIS18.madx")
orbit_mpi.MPI_Barrier(comm)

#----------------------------------------------
# Generate PTC RF table
#----------------------------------------------
# ~ if not rank:
        # ~ from lib.write_ptc_table import write_RFtable
        # ~ from simulation_parameters import RFparameters as RF
        # ~ write_RFtable('input/RF_table.ptc', *[RF[k] for k in ['harmonic_factors','time','Ekin_GeV','voltage_MV','phase']])
# ~ orbit_mpi.MPI_Barrier(comm)

#----------------------------------------------
# Initialize a Teapot-Style PTC lattice
#----------------------------------------------
PTC_File = "SIS_18_BENCHMARK.flt"
Lattice = PTC_Lattice("MACHINE")
Lattice.readPTC(PTC_File)
# ~ readScriptPTC('Input/fringe.txt')
readScriptPTC('time.ptc')
# ~ readScriptPTC('Input/chrom.ptc')

paramsDict = {}
paramsDict["length"]=Lattice.getLength()/Lattice.nHarm

#----------------------------------------------
# Add apertures
#----------------------------------------------
position = 0
for node in Lattice.getNodes():
	myaperturenode = TeapotApertureNode(1, 10, 10, position)
	node.addChildNode(myaperturenode, node.ENTRANCE)
	node.addChildNode(myaperturenode, node.BODY)
	node.addChildNode(myaperturenode, node.EXIT)
	position += node.getLength()


#----------------------------------------------
# Add the main bunch and lost particles bunch
#----------------------------------------------
bunch = Bunch()
setBunchParamsPTC(bunch)

from simulation_parameters import parameters as p
p['harmonic_number'] = Lattice.nHarm 
# ~ p['rf_voltage']      = rf_voltage
#~ p['rf_voltage']      = 0.025e6
p['phi_s']           = 0
p['gamma']           = bunch.getSyncParticle().gamma()
p['beta']            = bunch.getSyncParticle().beta()
p['energy']          = 1e9 * bunch.mass() * bunch.getSyncParticle().gamma()
p['bunch_length'] = p['blength_rms']/speed_of_light/bunch.getSyncParticle().beta()*4
kin_Energy = bunch.getSyncParticle().kinEnergy()
print 'Energy of particle = ', p['energy']
print 'Kinetic Energy of particle = ', kin_Energy

if horizontal:
        # ~ Particle_distribution_file = generate_initial_5mm_distributionH(0.1E-3, p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
        Particle_distribution_file = generate_initial_5mm_distributionH(0, p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
else:
        Particle_distribution_file = generate_initial_5mm_distributionV(0.1E-3, p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')

bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution_file, bunch, p['n_macroparticles'] + 1) #read in only first N_mp particles.
bunch.addPartAttr("macrosize")
map(lambda i: bunch.partAttrValue("macrosize", i, 0, p['macrosize']), range(bunch.getSize()))
ParticleIdNumber().addParticleIdNumbers(bunch) # Give them unique number IDs
bunch.dumpBunch("input/mainbunch_start.dat")
saveBunchAsMatfile(bunch, "output/mainbunch_-000001")

lostbunch = Bunch()
bunch.copyEmptyBunchTo(lostbunch)
lostbunch.addPartAttr('ParticlePhaseAttributes')
lostbunch.addPartAttr("LostParticleAttributes")
paramsDict["lostbunch"]=lostbunch
paramsDict["bunch"]= bunch

#----------------------------------------------------
# Add space charge nodes - FROZEN
#----------------------------------------------------
if frozen:
        print '\nSetting up the space charge calculations ...'
        # Make a SC solver using frozen potential
        # ~ sc_path_length_min = 1E-8
        sc_path_length_min = s['MinPathLength']
        LineDensity=GaussianLineDensityProfile(p['blength_rms'])
        sc_params1 = {'intensity': p['intensity'], 'epsn_x': p['epsn_x'], 'epsn_y': p['epsn_y'], 'dpp_rms': p['dpp_rms'], 'LineDensity': LineDensity}
        space_charge_solver1 = SpaceChargeCalcAnalyticGaussian(*[sc_params1[k] for k in ['intensity','epsn_x','epsn_y','dpp_rms','LineDensity']])
        print dir(scLatticeModifications)
        sc_nodes1 = scLatticeModifications.setSCanalyticalAccNodes(Lattice, sc_path_length_min, space_charge_solver1)
        print 'Installed %i space charge nodes'%(len(sc_nodes1))

#----------------------------------------------------
# Add space charge nodes - SliceBySlice
#----------------------------------------------------
if slicebyslice:
        print '\nAdding space charge nodes ...'
        # Make a SC solver
        sizeX = 32
        sizeY = 4
        sizeZ = 4  # Number of longitudinal slices in the 2.5D solver
        calcsbs = SpaceChargeCalcSliceBySlice2D(sizeX,sizeY,sizeZ)
        sc_path_length_min = 0.00000001
        # Add the space charge solver to the lattice as child nodes
        sc_nodes = scLatticeModifications.setSC2p5DAccNodes(Lattice, sc_path_length_min, calcsbs)
        print '  Installed', len(sc_nodes), 'space charge nodes ...'

#-----------------------------------------------------
# Add tune analysis child node
#-----------------------------------------------------
parentnode_number = 97
parentnode = Lattice.getNodes()[parentnode_number]
Twiss_at_parentnode_entrance = Lattice.getNodes()[parentnode_number-1].getParamsDict()
tunes = TeapotTuneAnalysisNode("tune_analysis")

if slicebyslice:
        tunes.assignTwiss(Twiss_at_parentnode_entrance['betax'], Twiss_at_parentnode_entrance['alphax'], Twiss_at_parentnode_entrance['etax'], Twiss_at_parentnode_entrance['etapx'], Twiss_at_parentnode_entrance['betay'], Twiss_at_parentnode_entrance['alphay'])
        addTeapotDiagnosticsNodeAsChild(Lattice, parentnode, tunes)
if frozen:
        tunes.assignTwiss(*[Twiss_at_parentnode_entrance[k] for k in ['betax','alphax','etax','etapx','betay','alphay','etay','etapy']])
        tunes.assignClosedOrbit(*[Twiss_at_parentnode_entrance[k] for k in ['orbitx','orbitpx','orbity','orbitpy']])
        addTeapotDiagnosticsNodeAsChild(Lattice, parentnode, tunes)

#----------------------------------------------------
# Prepare a bunch object to store particle coordinates
#----------------------------------------------------
bunch_tmp = Bunch()
bunch.copyEmptyBunchTo(bunch_tmp)
bunch_tmp.addPartAttr('ParticlePhaseAttributes')

#----------------------------------------------------
# Define twiss analysis and output dictionary
#----------------------------------------------------
bunchtwissanalysis = BunchTwissAnalysis() #Prepare the analysis class that will look at emittances, etc.
get_dpp = lambda b, bta: np.sqrt(bta.getCorrelation(5,5)) / (b.getSyncParticle().gamma()*b.mass()*b.getSyncParticle().beta()**2)
get_bunch_length = lambda b, bta: 4 * np.sqrt(bta.getCorrelation(4,4)) / (speed_of_light*b.getSyncParticle().beta())
get_eps_z = lambda b, bta: 1e9 * 4 * pi * bta.getEmittance(2) / (speed_of_light*b.getSyncParticle().beta())

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

if frozen or slicebyslice:
        output.addParameter('BE_intensity1', lambda: sc_params1['intensity'])
        output.addParameter('BE_epsn_x1', lambda: sc_params1['epsn_x'])
        output.addParameter('BE_epsn_y1', lambda: sc_params1['epsn_y'])
        output.addParameter('BE_dpp_rms1', lambda: sc_params1['dpp_rms'])

#----------------------------------------------------
# Function for restoring forxe
#----------------------------------------------------

names = bunch.getPossiblePartAttrNames()

print names

def LinearRestoringForce(b, force):

		rank = 0
		numprocs = 1
		
		mpi_init = orbit_mpi.MPI_Initialized()
		comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
		
		if(mpi_init):
			rank = orbit_mpi.MPI_Comm_rank(comm)
			numprocs = orbit_mpi.MPI_Comm_size(comm)
		
		nparts_arr_local = []
		for i in range(numprocs):
			nparts_arr_local.append(0)
				
		nparts_arr_local[rank] = b.getSize()
		data_type = mpi_datatype.MPI_INT
		op = mpi_op.MPI_SUM
	
		nparts_arr = orbit_mpi.MPI_Allreduce(nparts_arr_local,data_type,op,comm)

                for i in range(b.getSize()):
                        en = b.dE(i)

                        en = en + b.z(i) * force
                        
                        b.dE(i,en)
                        

#----------------------------------------------------
# Do some turns and dump particle information
#----------------------------------------------------

# Create the range of forces to be iterated
# ~ force_range=[]
f_start= -2.0E-11
f_int = 1E-13
f_stop = (-0.1E-11 + f_int)
force_range =  np.arange(f_start, f_stop, f_int, dtype=float)
force_iterator=int(0)

z_diff_end	=	100
z_diff_mid	=	100

initial_z = bunch.z(0)

end_tolerance = 0.1 * (initial_z / 100) #0.1%
mid_tolerance = 1 * (initial_z / 100) #1%

fileout = open("Force.txt","w+")
fileout.write("#Force\tz_diff_mid\tz_diff_end")
fileout.close()
# ~ fileout.write( "\n%f\t%f\t%f" % (1, z_diff_mid, z_diff_end))

# ~ sys.exit()

print '\nnow start tracking...'
for f in force_range:
	initial_z = bunch.z(0)
	print 'initial z = ', initial_z
	for turn in range(p['turns_max']):		
	# ~ print 'turn =', turn
		Lattice.trackBunch(bunch, paramsDict)
		LinearRestoringForce(bunch, f)
			
		bunchtwissanalysis.analyzeBunch(bunch)  # analyze twiss and emittance	
		
		# subtract circumference each turn in order to reconstruct the turn number from loss position
		map(lambda i: lostbunch.partAttrValue("LostParticleAttributes", i, 0, 
						  lostbunch.partAttrValue("LostParticleAttributes", i, 0)-p['circumference']), xrange(lostbunch.getSize()))
		
		if turn == (p['turns_max']/2):
			# ~ z_diff_mid = ( (-1*initial_z - bunch.z(0)) / -1*initial_z ) * 100
			z_diff_mid = (initial_z - bunch.z(0))
	# ~ z_diff_end = ( (-1*initial_z - bunch.z(0)) / -1*initial_z ) * 100
	z_diff_end = initial_z - bunch.z(0)
	
	print '\n\n\n\t\tForce = ', f
	print '\t\tz_diff_mid = ', z_diff_mid
	print '\t\tz_diff_end = ', z_diff_end 		
	fileout = open("Force.txt","a+")
	# ~ fo = float(f)
	fileout.write( "\n%e\t%f\t%f" % (float(f), z_diff_mid, z_diff_end))
	fileout.close()
	
	# ~ print "He's got %s eyes and %s hair." % (my_eyes, my_hair)
	
	
	if (z_diff_end < end_tolerance) and (z_diff_mid < mid_tolerance):
		print 'Convergence found - Force = ',f
		break
		
	# Have to redo the bunch	
	bunch = Bunch()
	if horizontal:
        # ~ Particle_distribution_file = generate_initial_5mm_distributionH(0.1E-3, p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
		Particle_distribution_file = generate_initial_5mm_distributionH(0, p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
	else:
		Particle_distribution_file = generate_initial_5mm_distributionV(0.1E-3, p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')

	bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution_file, bunch, p['n_macroparticles'] + 1) #read in only first N_mp particles.
	bunch.addPartAttr("macrosize")
	map(lambda i: bunch.partAttrValue("macrosize", i, 0, p['macrosize']), range(bunch.getSize()))
	
	paramsDict["bunch"]= bunch

# ~ fileout.close()

pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
pr.dump_stats('profile.txt')
# ~ ps.print_stats()
# ~ print s.getvalue()
