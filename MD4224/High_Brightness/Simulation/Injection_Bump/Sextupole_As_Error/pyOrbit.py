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

# plotting 
import matplotlib.pylab as plt
import matplotlib.cm as cm

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
from spacecharge import SpaceChargeCalcSliceBySlice2D
	
from orbit.space_charge.sc2p5d import scAccNodes, scLatticeModifications
from spacecharge import SpaceChargeCalcAnalyticGaussian
from spacecharge import InterpolatedLineDensityProfile

# User libs
from lib.pyOrbit_PrintLatticeFunctionsFromPTC import *
from lib.pyOrbit_PTCLatticeFunctionsDictionary import *
from lib.output_dictionary import *
from lib.pyOrbit_GenerateInitialDistribution import *
from lib.save_bunch_as_matfile import *
from lib.pyOrbit_Tunespread_Calculator import *
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
mpi_mkdir_p('Plots')
mpi_mkdir_p('input')
mpi_mkdir_p('bunch_output')
mpi_mkdir_p('output')
mpi_mkdir_p('lost')
mpi_mkdir_p('PTC_Twiss')

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
if not rank:
	# ~ os.system("./Create_FF_and_Tables.sh")
	if os.path.exists('PTC-PyORBIT_flat_file.flt'):
		pass
	else:
		os.system("./Create_FF_and_Tables.sh")
	# ~ if os.path.exists('PTC-PyORBIT_flat_file.flt'):
		# ~ pass
	# ~ else:
		# ~ os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < Flat_file.madx")
orbit_mpi.MPI_Barrier(comm)

# Print Tunespread data
#-----------------------------------------------------------------------
from simulation_parameters import tunespread as ts
if not rank:
	if os.path.exists('madx_twiss.tfs'):
		TunespreadCalculator(ts, 'madx_twiss.tfs')

# Generate PTC RF table
#-----------------------------------------------------------------------
print '\nstart RF file on MPI process: ', rank
from lib.write_ptc_table import write_RFtable
from simulation_parameters import RFparameters as RF 
write_RFtable('Tables/RF_table.ptc', *[RF[k] for k in ['harmonic_factors','time','Ekin_GeV','voltage_MV','phase']])

# Initialize a Teapot-Style PTC lattice
#-----------------------------------------------------------------------
print '\nstart PTC Flat file on MPI process: ', rank
PTC_File = "PTC-PyORBIT_flat_file.flt"
Lattice = PTC_Lattice("PS")
Lattice.readPTC(PTC_File)

readScriptPTC_noSTDOUT('PTC/fringe.ptc')
readScriptPTC_noSTDOUT('PTC/time.ptc')
readScriptPTC_noSTDOUT('PTC/ramp_magnet.ptc')
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

# Make a bunch and import relevant parameters for it
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
	# ~ p['bunch_length'] = p['sig_z']/speed_of_light/bunch.getSyncParticle().beta()*4
	p['bunch_length'] = p['bunch_length']
	kin_Energy = bunch.getSyncParticle().kinEnergy()

	print '\nbunch_orbit_to_pyorbit on MPI process: ', rank
	for i in p:
		print '\t', i, '\t = \t', p[i]

	if s['CreateDistn']:
# Create the initial distribution 
#-----------------------------------------------------------------------

# Statistical TWISS for vertical scan
#-----------------------------------------------------------------------
		Qy = [6.1, 6.11, 6.12, 6.13, 6.14, 6.15, 6.16, 6.17, 6.18, 6.19, 6.2, 6.21, 6.22, 6.23, 6.24]
		beta_x = [11.49778505297269, 11.561142423712235, 11.621563324253549, 11.685935519233954, 11.751842101341309, 11.814969760172527, 11.881700649427966, 11.95004290783458, 12.019275059276143, 12.088030476076925, 12.155710632377403, 12.221621917895586, 12.286487536379424, 12.351762866387576, 12.417282383224189]
		beta_y = [28.75775445834396, 27.90144543045776, 27.212978421993824, 26.553042781979897, 25.951033704906294, 25.466970667392626, 24.98572526966874, 24.5426713186873, 24.14864962809185, 23.812528441798015, 23.52879541212273, 23.279974969296187, 23.06731554922815, 22.898782875976057, 22.76466764380734]
		alpha_x = [0.02014978739106865, 0.01884353267781308, 0.0176321165229806, 0.01632333418125009, 0.014992854402007878, 0.013722998740755193, 0.012370060599780954, 0.010974386278459366, 0.009550692532226783, 0.008136163625900179, 0.006746557075054912, 0.005404514030477649, 0.004084683524410341, 0.002744221041003115, 0.0014013797790392067]
		alpha_y = [-0.07598190386654523, -0.06027204495860171, -0.04710560230957663, -0.0343755121739445, -0.022682599980032053, -0.012833165361499773, -0.003150414126168016, 0.0057881913916622545, 0.013799265862888191, 0.020722423649612087, 0.026638655754386516, 0.03178723390800505, 0.03618752176467799, 0.03980909595245627, 0.042823804527384185]
		D_x = [2.7232670487812256, 2.7116367856049948, 2.699599403210768, 2.6866790770377817, 2.673327070935468, 2.6599658661567056, 2.6455621037343575, 2.6305947070915603, 2.6152952481238847, 2.5997619799223886, 2.5841333492637544, 2.568298718241905, 2.5524105212520656, 2.536511996336176, 2.5204240966552374]
		D_y = [0.0003049303533906463, -0.00021647828752590061, 2.2236469376601038e-05, -0.00018742393285385114, 0.0009018831296542939, 0.0001287717460281074, -0.0002843418052139658, -5.639666617722505e-05, -5.102220215645195e-05, -8.77117650922447e-05, -6.350368017957502e-05, 1.1645739917172323e-05, -2.6525086555896508e-05, -1.0174844481937915e-05, -9.055730919930321e-06]

		index = Qy.index(s['Qy'])

		twiss_dict = dict()
		twiss_dict['alpha_x'] 			= alpha_x[index]
		twiss_dict['alpha_y'] 			= alpha_y[index]
		twiss_dict['beta_x'] 			= beta_x[index]
		twiss_dict['beta_y'] 			= beta_y[index]
		twiss_dict['D_x'] 				= D_x[index]
		twiss_dict['D_y'] 				= D_y[index]
		twiss_dict['D_xp'] 				= 0.
		twiss_dict['D_yp'] 				= 0.
		twiss_dict['x0'] 				= 0.
		twiss_dict['xp0'] 				= 0.
		twiss_dict['y0'] 				= 0.
		twiss_dict['yp0'] 				= 0.
		twiss_dict['gamma_transition'] 	= Lattice.gammaT
		twiss_dict['circumference']    	= Lattice.getLength()
		twiss_dict['length'] 			= Lattice.getLength()/Lattice.nHarm

		if not rank:
			for i in twiss_dict:
				print '\t', str(i), '\t = \t', twiss_dict[i]
	
		print '\ngenerate_initial_distribution on MPI process: ', rank
		if s['ImportFromTomo']:
			Particle_distribution_file = generate_initial_distribution_from_tomo_manual_Twiss(p, twiss_dict, 1, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')
		else:
			Particle_distribution_file = generate_initial_distribution(p, Lattice, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')

		print '\bunch_orbit_to_pyorbit on MPI process: ', rank
		bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution_file, bunch, p['n_macroparticles'] + 1) #read in only first N_mp particles.

	else:
# OR load bunch from file
#-----------------------------------------------------------------------
		path_to_distn = p['input_distn_dir']
		bunch = bunch_from_matfile(path_to_distn)			
		
# Add Macrosize to bunch
#-----------------------------------------------------------------------
	bunch.addPartAttr("macrosize")
	map(lambda i: bunch.partAttrValue("macrosize", i, 0, p['macrosize']), range(bunch.getSize()))
	ParticleIdNumber().addParticleIdNumbers(bunch) # Give them unique number IDs

# Dump and save as Matfile
#-----------------------------------------------------------------------
	# ~ bunch.dumpBunch("input/mainbunch_start.dat")
	print 'Save bunch in bunch_output/mainbunch_-000001.mat'
	saveBunchAsMatfile(bunch, "bunch_output/mainbunch_-000001")
	print 'Save bunch in input/mainbunch.mat'
	saveBunchAsMatfile(bunch, "input/mainbunch")
	sts['mainbunch_file'] = "input/mainbunch"

# Create empty lost bunch
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

bunch = bunch_from_matfile(sts['mainbunch_file'])
lostbunch = bunch_from_matfile(sts['lostbunch_file'])
paramsDict["lostbunch"]=lostbunch
paramsDict["bunch"]= bunch

#############################-------------------########################
#############################	SPACE CHARGE	########################
#############################-------------------########################

# Add space charge nodes
#----------------------------------------------------
if s['SliceBySlice']:
	print '\nAdding slice-by-slice space charge nodes on MPI process: ', rank
	# Make a SC solver
	calcsbs = SpaceChargeCalcSliceBySlice2D(s['GridSizeX'], s['GridSizeY'], s['GridSizeZ'], useLongitudinalKick=s['LongitudinalKick'])
	sc_path_length_min = 1E-8
	# Add the space charge solver to the lattice as child nodes
	sc_nodes = scLatticeModifications.setSC2p5DAccNodes(Lattice, sc_path_length_min, calcsbs)
	print '  Installed', len(sc_nodes), 'space charge nodes ...'


# Add tune analysis child node
#-----------------------------------------------------
parentnode_number = 97
parentnode = Lattice.getNodes()[parentnode_number]
Twiss_at_parentnode_entrance = Lattice.getNodes()[parentnode_number-1].getParamsDict()
tunes = TeapotTuneAnalysisNode("tune_analysis")

tunes.assignTwiss(*[Twiss_at_parentnode_entrance[k] for k in ['betax','alphax','etax','etapx','betay','alphay','etay','etapy']])
tunes.assignClosedOrbit(*[Twiss_at_parentnode_entrance[k] for k in ['orbitx','orbitpx','orbity','orbitpy']])
addTeapotDiagnosticsNodeAsChild(Lattice, parentnode, tunes)

# Define twiss analysis and output dictionary
#-----------------------------------------------------------------------
print '\nTWISS on MPI process: ', rank
bunchtwissanalysis = BunchTwissAnalysis() #Prepare the analysis class that will look at emittances, etc.
get_dpp = lambda b, bta: np.sqrt(bta.getCorrelation(5,5)) / (b.getSyncParticle().gamma()*b.mass()*b.getSyncParticle().beta()**2)
get_bunch_length = lambda b, bta: 4 * np.sqrt(bta.getCorrelation(4,4)) / (speed_of_light*b.getSyncParticle().beta())
get_eps_z = lambda b, bta: 1e9 * 4 * pi * bta.getEmittance(2) / (speed_of_light*b.getSyncParticle().beta())

# Function to open TWISS_PTC_table.OUT and return fractional tunes
def GetTunesFromPTC():
	readScriptPTC_noSTDOUT('PTC/twiss_script.ptc')
	with open('TWISS_PTC_table.OUT') as f:
		first_line = f.readline()
		Qx = (float(first_line.split()[2]))
		Qy = (float(first_line.split()[3]))
	os.system('rm TWISS_PTC_table.OUT')
	return Qx, Qy
	
output_file = 'output/output.mat'
output = Output_dictionary()
output.addParameter('turn', lambda: turn)
output.addParameter('Qx', lambda: GetTunesFromPTC()[0])
output.addParameter('Qy', lambda: GetTunesFromPTC()[1])
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
output.addParameter('beta_x', lambda: bunchtwissanalysis.getBeta(0))
output.addParameter('beta_y', lambda: bunchtwissanalysis.getBeta(1))
output.addParameter('alpha_x', lambda: bunchtwissanalysis.getAlpha(0))
output.addParameter('alpha_y', lambda: bunchtwissanalysis.getAlpha(1))
output.addParameter('D_x', lambda: bunchtwissanalysis.getDispersion(0))
output.addParameter('D_y', lambda: bunchtwissanalysis.getDispersion(1))
output.addParameter('eff_beta_x', lambda: bunchtwissanalysis.getEffectiveBeta(0))
output.addParameter('eff_beta_y', lambda: bunchtwissanalysis.getEffectiveBeta(1))
output.addParameter('eff_epsn_x', lambda: bunchtwissanalysis.getEffectiveEmittance(0))
output.addParameter('eff_epsn_y', lambda: bunchtwissanalysis.getEffectiveEmittance(1))
output.addParameter('eff_alpha_x', lambda: bunchtwissanalysis.getEffectiveAlpha(0))
output.addParameter('eff_alpha_y', lambda: bunchtwissanalysis.getEffectiveAlpha(1))

if os.path.exists(output_file):
	output.import_from_matfile(output_file)
	
# Lattice function dictionary to print closed orbit
#-----------------------------------------------------------------------
PTC_Twiss = PTCLatticeFunctionsDictionary()

# Track
#-----------------------------------------------------------------------
print '\nTracking on MPI process: ', rank
start_time = time.time()
last_time = time.time()


for turn in range(sts['turn']+1, sts['turns_max']):
	
	if not rank: 
		PTC_Twiss.UpdatePTCTwiss(Lattice, turn)
		#readScriptPTC_noSTDOUT('PTC/twiss_script.ptc')
		#rename_command = 'mv TWISS_PTC_table.OUT TWISS_' + str(turn) + '.tfs'
		#os.system(rename_command)
		last_time = time.time()
	
	if turn == 0:		
		output.addParameter('turn_time', lambda: time.strftime("%H:%M:%S"))
		output.addParameter('turn_duration', lambda: (time.time() - last_time))
		output.addParameter('cumulative_time', lambda: (time.time() - start_time))
		start_time = time.time()
		print 'start time = ', start_time
		
	Lattice.trackBunch(bunch, paramsDict)
	bunchtwissanalysis.analyzeBunch(bunch)  # analyze twiss and emittance	
	
	if turn in sts['turns_update']:	sts['turn'] = turn

	output.update()
	
	if turn in sts['turns_print']:
		saveBunchAsMatfile(bunch, "input/mainbunch")
		saveBunchAsMatfile(bunch, "bunch_output/mainbunch_%s"%(str(turn).zfill(6)))
		saveBunchAsMatfile(lostbunch, "lost/lostbunch_%s"%(str(turn).zfill(6)))
		output.save_to_matfile(output_file)		        
		if not rank:
			with open(status_file, 'w') as fid:
				pickle.dump(sts, fid)

# make sure simulation terminates properly
orbit_mpi.MPI_Barrier(comm)

# Plotting
#-----------------------------------------------------------------------
if not rank:

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
	savename = str('Plots/closedOrbit_evolution_' + str(sts['turns_max']) + '_turns.png')
	plt.savefig(savename, dpi=400)


	i2plot = range(len(s))
	for i in [134,135,235,236,305,306,358,359]: i2plot.remove(i)


	f, ax = plt.subplots()
	for t in TurnList:
		ax.plot(s[i2plot], np.array(TwissDict[t]['beta_x'])[i2plot], color=colors[t])
	ax.set_xlabel('s (m)')
	ax.set_ylabel('beta_x (m)')
	ax.set_ylim(bottom=0)
	savename = str('Plots/betax_evolution_' + str(sts['turns_max']) + '_turns.png')
	plt.savefig(savename, dpi=400)


	f, ax = plt.subplots()
	for t in TurnList:
		ax.plot(s[i2plot], np.array(TwissDict[t]['beta_x'])[i2plot], color=colors[t])
	ax.set_xlabel('s (m)')
	ax.set_ylabel('beta_y (m)')
	ax.set_ylim(bottom=0)
	savename = str('Plots/betay_evolution_' + str(sts['turns_max']) + '_turns.png')
	plt.savefig(savename, dpi=400)


	f, ax = plt.subplots()
	for t in TurnList:
		beta_y_ref = np.array(TwissDict[TurnList[-1]]['beta_y'])
		beta_y = np.array(TwissDict[t]['beta_y'])
		ax.plot(s[i2plot], 100*((beta_y - beta_y_ref)/beta_y_ref)[i2plot], color=colors[t])
	ax.set_xlabel('s (m)')
	ax.set_ylabel('beta_y (m)')
	savename = str('Plots/betay_beating_evolution_' + str(sts['turns_max']) + '_turns.png')
	plt.savefig(savename, dpi=400)


	f, ax = plt.subplots()
	for t in TurnList:
		beta_x_ref = np.array(TwissDict[TurnList[-1]]['beta_x'])
		beta_x = np.array(TwissDict[t]['beta_x'])
		ax.plot(s[i2plot], 100*((beta_x - beta_x_ref)/beta_x_ref)[i2plot], color=colors[t])
	ax.set_xlabel('s (m)')
	ax.set_ylabel('beta_y (m)')
	savename = str('Plots/betax_beating_evolution_' + str(sts['turns_max']) + '_turns.png')
	plt.savefig(savename, dpi=400)


	plt.close('all')
