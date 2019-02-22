import math
import sys
import time
import timeit
import numpy as np
import scipy.io as sio
import os
import orbit_mpi

from simulation_parameters import parameters as p
from simulation_parameters import RFparameters as RF
#from lib.generate_distribution_from_Tomoscope import *
from lib.pyOrbit_GenerateInitialDistribution2 import *

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

# longitudinal space charge
from orbit.space_charge.sc1d import addLongitudinalSpaceChargeNode, addLongitudinalSpaceChargeNodeAsChild, SC1D_AccNode
from spacecharge import LSpaceChargeCalc

# transverse space charge
from orbit.space_charge.sc2p5d import scAccNodes, scLatticeModifications
from spacecharge import SpaceChargeCalc2p5D, Boundary2D

# apertures 
from orbit.utils import orbitFinalize, NamedObject, ParamsDictObject
from orbit.aperture import addTeapotApertureNode
from orbit.aperture import TeapotApertureNode, CircleApertureNode, EllipseApertureNode, RectangleApertureNode
from orbit.aperture import addCircleApertureSet, addEllipseApertureSet, addRectangleApertureSet

# collimator
from orbit.collimation import TeapotCollimatorNode
from orbit.collimation import addTeapotCollimatorNode
from collimator import Collimator

# dictionary
from lib.output_dictionary import *
from lib.save_bunch_as_matfile import *

print "Start ..."
comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
rank = orbit_mpi.MPI_Comm_rank(comm)

#----------------------------------------------
# Create folder sctructure
#----------------------------------------------
from lib.mpi_helpers import mpi_mkdir_p
mpi_mkdir_p('input')
mpi_mkdir_p('output')
mpi_mkdir_p('bunch_output')

#----------------------------------------------
# Generate Lattice (MADX + PTC)
#----------------------------------------------
if not rank:
	os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < PSB_create_flat_file.madx")
orbit_mpi.MPI_Barrier(comm)


#----------------------------------------------
# Generate PTC RF table 
#----------------------------------------------
from lib.write_ptc_table import write_RFtable
from simulation_parameters import RFparameters as RF
write_RFtable('Tables/RF_table.ptc', *[RF[k] for k in ['harmonic_factors','time','Ekin_GeV','voltage_MV','phase']])

#----------------------------------------------
# Initialize a Teapot-Style PTC lattice
#----------------------------------------------
# PTC_File='Input/PSB_FLAT_Pert_r0.TXT'
PTC_File='input/PSB_FLAT.TXT'
Lattice = PTC_Lattice("PSB")
Lattice.readPTC(PTC_File)
readScriptPTC('ptc/fringe.txt')
readScriptPTC('ptc/time.txt')
readScriptPTC('ptc/chrom.txt')
# readScriptPTC('ptc/ramp_magnet.ptc')
readScriptPTC('ptc/ramp_cavities.ptc')
readScriptPTC('ptc/energize_lattice.ptc')
readScriptPTC('ptc/twiss_script.ptc')

paramsDict = {}
paramsDict["length"]=Lattice.getLength()/Lattice.nHarm
print '\nLattice parameters ...'
print '  circumference: \t', Lattice.getLength(), 'm'
print '  alphax0: \t\t', Lattice.alphax0
print '  betax0: \t\t', Lattice.betax0, 'm'
print '  alphay0: \t\t', Lattice.alphay0
print '  betay0: \t\t', Lattice.betay0, 'm'
print '  Dx0: \t\t\t', Lattice.etax0, 'm'
print '  Dpx0: \t\t', Lattice.etapx0, 'm'
print '  harm. number: \t', Lattice.nHarm
print '  nodes: \t\t', Lattice.nNodes

#----------------------------------------------
# Add apertures
#----------------------------------------------
# CHECK APERTURES!!!
position = 0
pos_start = 0
pos_stop  = Lattice.getLength()
n=0
for node in Lattice.getNodes():
	(node_pos_start,node_pos_stop) = Lattice.getNodePositionsDict()[node]
	print "node: ",n, ", name: ",node.getName()," type:",node.getType()," pos:",node_pos_start," L=",node.getLength()," end=",node_pos_start+node.getLength()
	myaperturenode = TeapotApertureNode(1, 100, 18, position)
	node.addChildNode(myaperturenode, node.ENTRANCE)
	node.addChildNode(myaperturenode, node.BODY)
	node.addChildNode(myaperturenode, node.EXIT)
	position += node.getLength()
	n += 1

#-----------------------------------------------------
# Add tune analysis child node
#-----------------------------------------------------
parentnode_number = 0
parentnode = Lattice.getNodes()[parentnode_number]
Twiss_at_parentnode_entrance = Lattice.getNodes()[parentnode_number-1].getParamsDict()
tunes = TeapotTuneAnalysisNode("tune_analysis")
tunes.assignTwiss(Twiss_at_parentnode_entrance['betax'], Twiss_at_parentnode_entrance['alphax'], Twiss_at_parentnode_entrance['etax'], Twiss_at_parentnode_entrance['etapx'], Twiss_at_parentnode_entrance['betay'], Twiss_at_parentnode_entrance['alphay'])
addTeapotDiagnosticsNodeAsChild(Lattice, parentnode, tunes)

#----------------------------------------------
# Add the main bunch and lost particles bunch
#----------------------------------------------
print '\nAdding main bunch ...'

bunch = Bunch()
setBunchParamsPTC(bunch)

#p['harmonic_number'] = Lattice.nHarm * np.atleast_1d(RF['harmonic_factors']) #harmonic_factors
#p['rf_voltage'] = 1e6*RF['voltage_MV'][0]
#p['phi_s'] = pi + RF['phase'][0]
#p['bunch_length'] = p['blength_rms']/speed_of_light/bunch.getSyncParticle().beta()*4

p['circumference'] = Lattice.getLength()
p['harmonic_number'] = Lattice.nHarm 
p['gamma'] = bunch.getSyncParticle().gamma()
p['beta'] = bunch.getSyncParticle().beta()
p['energy'] = 1e9 * bunch.mass() * bunch.getSyncParticle().gamma()

#Particle_distribution_file = generate_initial_distribution(p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
Particle_distribution_file = generate_initial_distribution_from_tomo_offset(p, 1, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')

bunch.readBunch(Particle_distribution_file)

bunch.addPartAttr("macrosize")
map(lambda i: bunch.partAttrValue("macrosize", i, 0, p['macrosize']), range(bunch.getSize()))

ParticleIdNumber().addParticleIdNumbers(bunch) # Give them unique number IDs

bunch.dumpBunch("input/mainbunch_start.dat")
saveBunchAsMatfile(bunch, "input/mainbunch")
saveBunchAsMatfile(bunch, "bunch_output/mainbunch_-000001")

lostbunch = Bunch()
bunch.copyEmptyBunchTo(lostbunch)
lostbunch.addPartAttr('ParticlePhaseAttributes')
lostbunch.addPartAttr("LostParticleAttributes")
paramsDict['lostbunch'] = lostbunch
saveBunchAsMatfile(lostbunch, "input/lostbunch")

#----------------------------------------------------
# Define twiss analysis and output dictionary
#----------------------------------------------------
bunchtwissanalysis = BunchTwissAnalysis() #Prepare the analysis class that will look at emittances, etc.
get_dpp = lambda b, bta: np.sqrt(bta.getCorrelation(5,5)) / (b.getSyncParticle().gamma()*b.mass()*b.getSyncParticle().beta()**2)
get_bunch_length = lambda b, bta: 4 * np.sqrt(bta.getCorrelation(4,4)) / (speed_of_light*b.getSyncParticle().beta())
get_eps_z = lambda b, bta: 1e9 * 4 * pi * bta.getEmittance(2) / (speed_of_light*b.getSyncParticle().beta())

output_file = 'output/output'
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
output.addParameter('eps_x', lambda: bunchtwissanalysis.getEmittance(0))
output.addParameter('epsn_y', lambda: bunchtwissanalysis.getEmittanceNormalized(1))
output.addParameter('eps_y', lambda: bunchtwissanalysis.getEmittance(1))
output.addParameter('eps_z', lambda: get_eps_z(bunch, bunchtwissanalysis))
output.addParameter('bunchlength', lambda: get_bunch_length(bunch, bunchtwissanalysis))
output.addParameter('dpp_rms', lambda: get_dpp(bunch, bunchtwissanalysis))
if os.path.exists(output_file):
	output.import_from_matfile(output_file)
	
#-----------------------------------------------------------------------
# Track
#-----------------------------------------------------------------------

for turn in range(p['turns_max']):
	print 'turn number: ', turn
	
    # keep particles within circumference
	for i in xrange(bunch.getSize()):
		bunch.z(i,-Lattice.getLength()/2.+(bunch.z(i)+Lattice.getLength()/2.)%Lattice.getLength())
		
	Lattice.trackBunch(bunch, paramsDict)
	readScriptPTC("ptc/update-twiss.ptc")
	updateParamsPTC(Lattice,bunch)
	
	bunchtwissanalysis.analyzeBunch(bunch)  # analyze twiss and emittance	
	output.update()
	if turn in p['turns_print']:
		saveBunchAsMatfile(bunch, "bunch_output/mainbunch_%s"%(str(turn).zfill(6)))
		output.save_to_matfile(output_file)
		# readScriptPTC('ptc/write_FINAL_SETTINGS.ptc')

