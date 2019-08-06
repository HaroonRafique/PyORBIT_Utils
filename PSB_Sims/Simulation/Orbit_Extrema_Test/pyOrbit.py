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
from lib.pyOrbit_PrintLatticeFunctionsFromPTC import *
from lib.pyOrbit_PTCLatticeFunctionsDictionary import *
from lib.output_dictionary import *
from lib.save_bunch_as_matfile import *
from lib.bunch_profiles import *
from lib.suppress_stdout import suppress_STDOUT
readScriptPTC_noSTDOUT = suppress_STDOUT(readScriptPTC)

# plotting 
import matplotlib.pylab as plt
import matplotlib.cm as cm


print "Start ..."
comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
rank = orbit_mpi.MPI_Comm_rank(comm)

#----------------------------------------------
# Create folder structure
#----------------------------------------------`
from lib.mpi_helpers import mpi_mkdir_p
mpi_mkdir_p('input')
mpi_mkdir_p('output')
lattice_folder = 'lattice'
mpi_mkdir_p(lattice_folder)


#----------------------------------------------
# Dictionary for simulation status (for resume)
#----------------------------------------------
import pickle
status_file = 'input/simulation_status.pkl'
if not os.path.exists(status_file):
	sts = {'turn': -1, 'mainbunch_file': "input/mainbunch", 'lostbunch_file': "input/lostbunch"}
else: 
	with open(status_file) as fid:
		sts = pickle.load(fid)

# Lattice function dictionary to print closed orbit
#-----------------------------------------------------------------------
ptc_dictionary_file = 'input/ptc_dictionary.pkl'
if not os.path.exists(ptc_dictionary_file):        
	PTC_Twiss = PTCLatticeFunctionsDictionary()
else:
	with open(ptc_dictionary_file) as sid:
		PTC_Twiss = pickle.load(sid)

#----------------------------------------------
# Simulation Parameters
#----------------------------------------------
sts['turns_max'] = 500
# ~ sts['turns_max'] = 1000
sts['turns_print'] = xrange(-1, sts['turns_max'], 2000000)
sts['turns_injection'] = np.arange(1)


#----------------------------------------------
# Initialize a Teapot-Style PTC lattice
#----------------------------------------------
PTC_File='PSB_FLAT_Pert_r0.TXT'
Lattice = PTC_Lattice("PSB")
Lattice.readPTC(PTC_File)
readScriptPTC('ptc/fringe.txt')
readScriptPTC('ptc/time.txt')
readScriptPTC('ptc/chrom.txt')
readScriptPTC('ptc/ramp_magnet.ptc')
readScriptPTC('ptc/ramp_cavities.ptc')
if sts['turn'] >= 0:
	readScriptPTC('ptc/read_FINAL_SETTINGS.ptc')
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
position = 0
pos_start = 0
pos_stop  = Lattice.getLength()
n=0
for node in Lattice.getNodes():
	myaperturenode = TeapotApertureNode(1, 10, 18, position)
	node.addChildNode(myaperturenode, node.ENTRANCE)
	node.addChildNode(myaperturenode, node.BODY)
	node.addChildNode(myaperturenode, node.EXIT)
	position += node.getLength()
	n += 1

#-----------------------------------------------------
# Add tune analysis child node
#-----------------------------------------------------
parentnode_number = 40
parentnode = Lattice.getNodes()[parentnode_number]
Twiss_at_parentnode_entrance = Lattice.getNodes()[parentnode_number-1].getParamsDict
tunes = TeapotTuneAnalysisNode("tune_analysis")
tunes.assignTwiss(*[Twiss_at_parentnode_entrance()[k] for k in ['betax','alphax','etax','etapx','betay','alphay','etay','etapy']])
tunes.assignClosedOrbit(*[Twiss_at_parentnode_entrance()[k] for k in ['orbitx','orbitpx','orbity','orbitpy']])
addTeapotDiagnosticsNodeAsChild(Lattice, parentnode, tunes)

PrintLatticeFunctions(Lattice, -1, lattice_folder)       
#----------------------------------------------
# Add the main bunch and lost particles bunch
#----------------------------------------------
print '\nAdding main bunch ...'
Intensity = 1.6e+13
m0 = mass_proton 	# protons ...
# ~ mp_final = 500000 # total number of particles injected
mp_final = 500 # total number of particles injected

macrosize = Intensity/mp_final
bunch = Bunch()
setBunchParamsPTC(bunch)
kin_Energy = bunch.getSyncParticle().kinEnergy()
print '  Momentum: ', bunch.getSyncParticle().momentum(), 'GeV'
print '  Ekin:     ', bunch.getSyncParticle().kinEnergy(), 'GeV'
print '  Gamma:    ',bunch.getSyncParticle().gamma() 
print '  Beta:     ', bunch.getSyncParticle().beta()
print '  Charge:   ', bunch.charge(), 'e'
print '  Mass:     ', bunch.mass(), 'GeV'

ParticleIdNumber().addParticleIdNumbers(bunch) # Give particles unique number ids
bunch.addPartAttr("macrosize")

lostbunch = Bunch()
lostbunch.addPartAttr("LostParticleAttributes")

paramsDict["bunch"]= bunch
paramsDict["lostbunch"] = lostbunch

# read the particles from main bunch if the simulation resumes
if sts['turn'] >= 0:
	bunch = bunch_from_matfile(sts['mainbunch_file'])
	lostbunch = bunch_from_matfile(sts['lostbunch_file'])

'''
#----------------------------------------------------
# Add transverse potential space charge node with
# rectangular boundary
#----------------------------------------------------
print '\nAdding longitudinal space charge ...'
b_a = 1.5
nMacrosMin = 32
useSpaceCharge = 1
nBins= 64     # Number of longitudinal slices in the 1D space charge solver
position = 1   # The location in the lattice. Can be any empty place
length = Lattice.getLength() 
sc1Dnode = SC1D_AccNode(b_a,length, nMacrosMin, useSpaceCharge, nBins)
nodes = Lattice.getNodes()
AccNode = nodes[1]
addLongitudinalSpaceChargeNodeAsChild(Lattice, AccNode, sc1Dnode)

print '\nAdding transverse space charge nodes ...'
sizeX = 128
sizeY = 128
sizeZ = 64  # Number of longitudinal slies in the 2.5D solver
calc2p5d = SpaceChargeCalc2p5D(sizeX,sizeY,sizeZ)
sc_path_length_min = 0.00000001

# Add the space charge solver to the lattice as child nodes
sc_nodes = scLatticeModifications.setSC2p5DAccNodes(Lattice, sc_path_length_min, calc2p5d)
print '  Installed', len(sc_nodes), 'space charge nodes ...'
'''

#----------------------------------------------------
# Define twiss analysis and output dictionary
#----------------------------------------------------
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
# output.addParameter('mean_x', lambda: bunchtwissanalysis.getAverage(0))
# output.addParameter('mean_xp', lambda: bunchtwissanalysis.getAverage(1))
# output.addParameter('mean_y', lambda: bunchtwissanalysis.getAverage(2))
# output.addParameter('mean_yp', lambda: bunchtwissanalysis.getAverage(3))
# output.addParameter('mean_z', lambda: bunchtwissanalysis.getAverage(4))
# output.addParameter('mean_dE', lambda: bunchtwissanalysis.getAverage(5))
# output.addParameter('epsn_x', lambda: bunchtwissanalysis.getEmittanceNormalized(0))
# output.addParameter('epsn_y', lambda: bunchtwissanalysis.getEmittanceNormalized(1))
# output.addParameter('eps_z', lambda: get_eps_z(bunch, bunchtwissanalysis))
# output.addParameter('bunchlength', lambda: get_bunch_length(bunch, bunchtwissanalysis))
# output.addParameter('dpp_rms', lambda: get_dpp(bunch, bunchtwissanalysis))
# ~ output.addParameter('CO_x', lambda: Lattice.orbitx0)
# ~ output.addParameter('CO_y', lambda: Lattice.orbity0)
output.addParameter('wall_time', time.time)
if os.path.exists(output_file):
	output.import_from_matfile(output_file)

#----------------------------------------------------
# Bunch profies
#----------------------------------------------------
bunchProfiles = Bunch_Profile(50,50,50)
twiss_dict = {'betax': Lattice.betax0, 'betay': Lattice.betay0, 'etax': Lattice.etax0, 'etay': Lattice.etay0}

#----------------------------------------------------
# Tracking
#----------------------------------------------------
print '\n\n now start tracking ...'
# ~ CO_x = []
# ~ BETA_y = []

for turn in range(sts['turn']+1, sts['turns_max']):

	if turn in sts['turns_injection']:
		Particle_distribution_file = 'Distribution_at_injection_full/single_particle.dat'	# final distribution with the correct angle
		kin_Energy = bunch.getSyncParticle().kinEnergy()
		bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution_file, bunch) #read in N_mp particles. 
		for i in range(bunch.getSize()):
			bunch.partAttrValue("macrosize", i, 0, macrosize)  #main bunch has finite macrosize for space charge
	
	# keep particles within circumference
	z_lim = -65
	for i in xrange(bunch.getSize()):
		bunch.z(i, ((bunch.z(i)-z_lim)%paramsDict["length"])+z_lim)

	Lattice.trackBunch(bunch, paramsDict)
	bunchtwissanalysis.analyzeBunch(bunch)  # analyze twiss and emittance	
	readScriptPTC_noSTDOUT("ptc/update-twiss.ptc") # this is needed to correclty update the twiss functions in all lattice nodes in updateParamsPTC
	updateParamsPTC(Lattice,bunch) # to update bunch energy and twiss functions
	tunes.assignTwiss(*[Twiss_at_parentnode_entrance()[k] for k in ['betax','alphax','etax','etapx','betay','alphay','etay','etapy']])
	tunes.assignClosedOrbit(*[Twiss_at_parentnode_entrance()[k] for k in ['orbitx','orbitpx','orbity','orbitpy']])
	# ~ CO_x.append([n.getParamsDict()['orbitx'] for n in Lattice.getNodes()])
	# ~ BETA_y.append([n.getParamsDict()['betay'] for n in Lattice.getNodes()])
	
	output.update()
	sts['turn'] = turn

	if not rank:	
		# ~ PrintLatticeFunctions(Lattice, turn, lattice_folder)   # This will print one PTC lattice function file for each turn
		PTC_Twiss.UpdatePTCTwiss(Lattice, turn)

	if turn in sts['turns_print']:
		output.save_to_matfile(output_file)
		saveBunchAsMatfile(bunch, sts['mainbunch_file'])
		saveBunchAsMatfile(lostbunch, sts['lostbunch_file'])
		bunchProfiles.bin_bunch(bunch, twiss_dict)
		if not rank:			
			readScriptPTC_noSTDOUT('ptc/write_FINAL_SETTINGS.ptc')
			with open(status_file, 'w') as fid:
				pickle.dump(sts, fid)

# make sure simulation terminates properly
orbit_mpi.MPI_Barrier(comm)
# Plotting
#-----------------------------------------------------------------------
if not rank:
	PTC_Twiss.PrintOrbitExtrema('All_Twiss')
	PTC_Twiss.PrintAllPTCTwiss('All_Twiss')
	TwissDict = PTC_Twiss.ReturnTwissDict()
	TurnList = PTC_Twiss.ReturnTurnList()

	colors = cm.rainbow(np.linspace(0, 1, len(TurnList)))


	# some gymnastics to avoid plotting offset elements ...
	roll = 284
	circumference = 25*2*np.pi
	s = TwissDict[0]['s']
	s[roll:] -= circumference
	s[roll] = np.nan
	i2plot = range(len(s))
	for i in [2,3,6,7,569,570,573,574]: i2plot.remove(i) # avoid plotting elements with offset


	f, ax = plt.subplots()
	for t in TurnList:
		ax.plot(s[i2plot], 1e3*np.array(TwissDict[t]['orbit_x'])[i2plot], color=colors[t])
	ax.set_xlabel('s (m)')
	ax.set_ylabel('horizontal CO (mm)')
	ax.set_xlim(-15,15)
	savename = str('png/closedOrbit_evolution_' + str(sts['turns_max']) + '_turns.png')
	plt.savefig(savename, dpi=400)


	i2plot = range(len(s))
	for i in [134,135,235,236,305,306,358,359]: i2plot.remove(i)


	f, ax = plt.subplots()
	for t in TurnList:
		ax.plot(s[i2plot], np.array(TwissDict[t]['beta_x'])[i2plot], color=colors[t])
	ax.set_xlabel('s (m)')
	ax.set_ylabel('beta_x (m)')
	ax.set_ylim(bottom=0)
	savename = str('png/betax_evolution_' + str(sts['turns_max']) + '_turns.png')
	plt.savefig(savename, dpi=400)


	f, ax = plt.subplots()
	for t in TurnList:
		ax.plot(s[i2plot], np.array(TwissDict[t]['beta_x'])[i2plot], color=colors[t])
	ax.set_xlabel('s (m)')
	ax.set_ylabel('beta_y (m)')
	ax.set_ylim(bottom=0)
	savename = str('png/betay_evolution_' + str(sts['turns_max']) + '_turns.png')
	plt.savefig(savename, dpi=400)


	f, ax = plt.subplots()
	for t in TurnList:
		beta_y_ref = np.array(TwissDict[TurnList[-1]]['beta_y'])
		beta_y = np.array(TwissDict[t]['beta_y'])
		ax.plot(s[i2plot], 100*((beta_y - beta_y_ref)/beta_y_ref)[i2plot], color=colors[t])
	ax.set_xlabel('s (m)')
	ax.set_ylabel('beta_y (m)')
	savename = str('png/betay_beating_evolution_' + str(sts['turns_max']) + '_turns.png')
	plt.savefig(savename, dpi=400)


	f, ax = plt.subplots()
	for t in TurnList:
		beta_x_ref = np.array(TwissDict[TurnList[-1]]['beta_x'])
		beta_x = np.array(TwissDict[t]['beta_x'])
		ax.plot(s[i2plot], 100*((beta_x - beta_x_ref)/beta_x_ref)[i2plot], color=colors[t])
	ax.set_xlabel('s (m)')
	ax.set_ylabel('beta_y (m)')
	savename = str('png/betax_beating_evolution_' + str(sts['turns_max']) + '_turns.png')
	plt.savefig(savename, dpi=400)


	plt.close('all')
