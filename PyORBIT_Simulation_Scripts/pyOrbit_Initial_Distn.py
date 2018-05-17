# PTC-PyORBIT Script used to test initial distributions for a given lattice
# In this case the SIS18 lattice is used (with Sextupole)

# Requirements:
# Haroon Rafique's PyORBIT libraries found at:
# https://github.com/HaroonRafique/PyORBIT_Utils/tree/master/lib
# SIS18 lattice and simulation files:
# SIS18/*
# SIS18.madx, simulation_parameters.py, print_flat_file.ptc
# found at:
# https://github.com/HaroonRafique/PyORBIT_Utils/tree/master/SIS18/Simulation/Step1
# access to CERN AFS or a local MAD-X installation

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
from orbit.space_charge.analytical import scAccNodes, scLatticeModifications
from spacecharge import SpaceChargeCalcAnalyticGaussian
# from spacecharge import GaussianLineDensityProfile
from spacecharge import InterpolatedLineDensityProfile

#PIC
from orbit.space_charge.sc2p5d import scAccNodes, scLatticeModifications
from spacecharge import SpaceChargeCalc2p5D, Boundary2D
from spacecharge import SpaceChargeCalcSliceBySlice2D


from lib.output_dictionary import *
from lib.pyOrbit_GenerateInitialDistribution2 import *
# ~ from lib.pyOrbit_GenerateMatchedDistribution import *
from lib.save_bunch_as_matfile import *

#----------------------------------------------
# Simulation Switches
#----------------------------------------------
space_charge_on = 0

print "Start ..."
comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
rank = orbit_mpi.MPI_Comm_rank(comm)

#----------------------------------------------
# Create folder structure
#----------------------------------------------
from lib.mpi_helpers import mpi_mkdir_p
mpi_mkdir_p('input')
mpi_mkdir_p('output')

#----------------------------------------------
# Generate Lattice (MADX + PTC)
#----------------------------------------------
if not rank:
	# ~ os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < Flat_file.madx")
	os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < SIS18.madx")
	# ~ os.system("madx < SIS18.madx")
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
# ~ readScriptPTC('Input/time.ptc')
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
p['phi_s']           = 0
p['gamma']           = bunch.getSyncParticle().gamma()
p['beta']            = bunch.getSyncParticle().beta()
p['energy']          = 1e9 * bunch.mass() * bunch.getSyncParticle().gamma()
p['bunch_length'] = p['blength_rms']/speed_of_light/bunch.getSyncParticle().beta()*4
kin_Energy = bunch.getSyncParticle().kinEnergy()
Particle_distribution_file = generate_initial_distribution(p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
# ~ Particle_distribution_file = generate_initial_distribution_y02(p, Lattice,  output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')

bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution_file, bunch, p['n_macroparticles'] + 1) #read in only first N_mp particles.
bunch.addPartAttr("macrosize")
map(lambda i: bunch.partAttrValue("macrosize", i, 0, p['macrosize']), range(bunch.getSize()))
ParticleIdNumber().addParticleIdNumbers(bunch) # Give them unique number IDs
bunch.dumpBunch("input/mainbunch_start.dat")
saveBunchAsMatfile(bunch, "input/mainbunch")
saveBunchAsMatfile(bunch, "output/mainbunch_-000001")

##########
## EXIT ##
##########

sys.exit()

lostbunch = Bunch()
bunch.copyEmptyBunchTo(lostbunch)
lostbunch.addPartAttr('ParticlePhaseAttributes')
lostbunch.addPartAttr("LostParticleAttributes")
paramsDict["lostbunch"]=lostbunch
paramsDict["bunch"]= bunch

#----------------------------------------------------
# Add space charge nodes
#----------------------------------------------------
if space_charge_on:
        print '\nAdding space charge nodes ...'
        # Make a SC solver
        sizeX = 32
        sizeY = 32
        sizeZ = 32  # Number of longitudinal slices in the 2.5D solver
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
tunes.assignTwiss(Twiss_at_parentnode_entrance['betax'], Twiss_at_parentnode_entrance['alphax'], Twiss_at_parentnode_entrance['etax'], Twiss_at_parentnode_entrance['etapx'], Twiss_at_parentnode_entrance['betay'], Twiss_at_parentnode_entrance['alphay'])
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



#----------------------------------------------------
# Do some turns and dump particle information
#----------------------------------------------------
print '\nnow start tracking...'

for turn in range(p['turns_max']):
	Lattice.trackBunch(bunch, paramsDict)
	bunchtwissanalysis.analyzeBunch(bunch)  # analyze twiss and emittance	
	
	# subtract circumference each turn in order to reconstruct the turn number from loss position
	map(lambda i: lostbunch.partAttrValue("LostParticleAttributes", i, 0, 
					  lostbunch.partAttrValue("LostParticleAttributes", i, 0)-p['circumference']), xrange(lostbunch.getSize()))

	bunch.addParticlesTo(bunch_tmp)	

	saveBunchAsMatfile(bunch, "output/mainbunch_%s"%(str(turn).zfill(6)))
	saveBunchAsMatfile(lostbunch, "output/lostbunch_%s"%(str(turn).zfill(6)))
	output.save_to_matfile('output/output')

	output.update()
