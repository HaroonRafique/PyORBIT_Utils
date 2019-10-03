import math
import sys
import time
import orbit_mpi
import timeit
import numpy as np
import scipy.io as sio
from scipy.stats import moment
from scipy.optimize import curve_fit
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Use switches in simulation_parameters.py in current folder
#-------------------------------------------------------------
from simulation_parameters import switches as s

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

from lib.output_dictionary import *
from lib.pyOrbit_GenerateInitialDistribution import *
from lib.save_bunch_as_matfile import *
from lib.pyOrbit_Tunespread_Calculator import *
from lib.suppress_stdout import suppress_STDOUT
readScriptPTC_noSTDOUT = suppress_STDOUT(readScriptPTC)

# FUNCTION DEFINITIONS
#-----------------------------------------------------------------------
def gaussian_3_parameters(x, A, mu, sig):
	return A/np.sqrt(2*np.pi)/sig*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def filtered(a):
	try:
		b=(scipy.signal.savgol_filter(a,15,1))
	except:
		b=a
	return b

def peakfinder (x_dat, y_dat, tolerance = 1, verbose=False):

	# Find maximum
	max_y = max(y_dat)
	if verbose: print '\n\tMAX(y_dat) = ', max_y   

	# Assume peak as centre
	print np.where(y_dat == max_y)
	index = np.where(y_dat == max_y)[0]

	# Check if centre is near 0.0
	if abs(x_dat[index]) < tolerance:
		if verbose: print '\tx_dat[index] = ', x_dat[index]

	# Manually find 0 index
	else:
		if verbose: print '\tindex from y_dat peak not within tolerance of',tolerance,'mm. \n\ttry manual search'
		
		index = -1
		final_index = -1
		for i in xrange(len(x_dat)):
			index = index + 1
			if x_dat[i] < 0.0:
				final_index = index
				break
				
		index = final_index
		if verbose: print '\tindex = ', index       
	   
	if verbose: print '\tindex of x_dat = ', x_dat[index],' is ', index
		
	# Take y=0 +/- 3 points and find mean 
	mean_dat = [y_dat[index-3],  y_dat[index-2],  y_dat[index-1], y_dat[index],  y_dat[index+1],  y_dat[index+2],  y_dat[index+3]]
	mean_7 = np.mean(mean_dat)
	if verbose: print '\tMean of peak point +/- 3 points = ', mean_7   

	if abs( abs(mean_7 - max_y) / mean_7 ) > 0.2:
		print '\tWARNING: difference between mean and max_y > 20% = ', abs( abs(mean_7 - max_y) / mean_7 )
		print '\t using peak value'
		mean_7 = max_y
	return mean_7

def GetBunchSigmas(b, smooth=True):
	window = 40

	# MPI stuff to run on a single node
	rank = 0
	numprocs = 1

	mpi_init = orbit_mpi.MPI_Initialized()
	comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
	orbit_mpi.MPI_Barrier(comm)

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

# Arrays to hold x and y data
	x = []
	y = []

	for i in range(b.getSize()):
		x.append(b.x(i))
		y.append(b.y(i))

# Calculate moments of the bunch
	return moment(x, 2), moment(y, 2)



	# ~ x_, bins_x, p = plt.hist(x, bins = 1000, density=True, histtype=u'step', lw=0)
	# ~ y_, bins_y, p = plt.hist(y, bins = 1000, density=True, histtype=u'step', lw=0)

	# ~ print x_
	# ~ print y_

	# ~ posx = np.array(bins_x[:-1]) + (abs(bins_x[0]-bins_x[1])/2)
	# ~ posy = np.array(bins_y[:-1]) + (abs(bins_y[0]-bins_y[1])/2)

	# ~ data_x = []
	# ~ data_y = []

	# ~ if smooth:
		# ~ data_x = filtered(x_)
		# ~ data_y = filtered(y_)
	# ~ else:
		# ~ data_x = x_
		# ~ data_y = y_

	# ~ indx_max_x = np.argmax(data_x)
	# ~ indx_max_y = np.argmax(data_y)

	# ~ mu0_x = data_x[indx_max_x]
	# ~ mu0_y = data_y[indx_max_y]

	# ~ offs0_x = min(data_x)
	# ~ ampl_x = max(data_x) - offs0_x
	# ~ x1 = data_x[np.searchsorted(data_x[:window], offs0_x + ampl_x/2)]
	# ~ x2 = data_x[np.searchsorted(-data_x[window:], -offs0_x + ampl_x/2)]
	# ~ FWHM_x = x2-x1
	# ~ sigma0_x = np.abs(2*FWHM_x/2.355)
	# ~ ampl_x *= np.sqrt(2*np.pi)*sigma0_x
	# ~ slope_x = 0

	# ~ offs0_y = min(data_y)
	# ~ ampl_y = max(data_y) - offs0_y
	# ~ y1 = data_y[np.searchsorted(data_y[:window], offs0_y + ampl_y/2)]
	# ~ y2 = data_y[np.searchsorted(-data_y[window:], -offs0_y + ampl_y/2)]
	# ~ FWHM_y = y2-y1
	# ~ sigma0_y = np.abs(2*FWHM_y/2.355)
	# ~ ampl_y *= np.sqrt(2*np.pi)*sigma0_y
	# ~ slope_y = 0

	# ~ ampl_x = peakfinder(np.array(bins_x[:-1]), np.array(data_x))
	# ~ ampl_y = peakfinder(np.array(bins_y[:-1]), np.array(data_y))
	
	# ~ print data_x
	# ~ print data_y
	
	# ~ poptx, pcovx = curve_fit(gaussian_3_parameters, posx, data_x, p0 =[ampl_x, mu0_x, sigma0_x])
	# ~ resultx = gaussian_3_parameters(bins_x, poptx[0], poptx[1], poptx[2])

	# ~ popty, pcovy = curve_fit(gaussian_3_parameters, posy, data_y, p0 =[ampl_y, mu0_y, sigma0_y])
	# ~ resultx = gaussian_3_parameters(bins_y, popty[0], popty[1], popty[2])

	# ~ return poptx[2], popty[2]


# Function to check that a file isn't empty (common PTC file bug)
def is_non_zero_file(fpath):  
	print 'Checking file ', fpath
	print 'File exists = ', os.path.isfile(fpath)
	print 'Size > 3 bytes = ', os.path.getsize(fpath)
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 3

# Function to check and read PTC file
def CheckAndReadPTCFile(f):
	if is_non_zero_file(f): 
		readScriptPTC_noSTDOUT(f)
	else:
		print 'ERROR: PTC file ', f, ' is empty or does not exist, exiting'
		exit(0)

# Function to open TWISS_PTC_table.OUT and return fractional tunes
def GetTunesFromPTC():
	readScriptPTC_noSTDOUT('PTC/twiss_script.ptc')
	with open('TWISS_PTC_table.OUT') as f:
		first_line = f.readline()
		Qx = (float(first_line.split()[2]))
		Qy = (float(first_line.split()[3]))
	os.system('rm TWISS_PTC_table.OUT')
	return Qx, Qy

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
if not rank:
	os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < Flat_file.madx")
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
write_RFtable('input/RF_table.ptc', *[RF[k] for k in ['harmonic_factors','time','Ekin_GeV','voltage_MV','phase']])

# Initialize a Teapot-Style PTC lattice
#-----------------------------------------------------------------------
print '\nstart PTC Flat file on MPI process: ', rank
PTC_File = "PTC-PyORBIT_flat_file.flt"
Lattice = PTC_Lattice("PS")
Lattice.readPTC(PTC_File)

CheckAndReadPTCFile('PTC/fringe.ptc')
CheckAndReadPTCFile('PTC/time.ptc')
CheckAndReadPTCFile('PTC/ramp_cavities.ptc')

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

	for i in p:
		print '\t', i, '\t = \t', p[i]

	if s['CreateDistn']:
		print '\nCreating initial distribution'
# Create the initial distribution 

		twiss_dict = dict()
		twiss_dict['alpha_x'] 			= Lattice.alphax0
		twiss_dict['alpha_y'] 			= Lattice.alphay0
		twiss_dict['beta_x'] 			= Lattice.betax0
		twiss_dict['beta_y'] 			= Lattice.betay0
		twiss_dict['D_x'] 				= Lattice.etax0
		if s['Mismatch']: twiss_dict['D_x'] *= s['MismatchFactor']
		twiss_dict['D_y'] 				= Lattice.etay0
		twiss_dict['D_xp'] 				= Lattice.etapx0
		twiss_dict['D_yp'] 				= Lattice.etapy0
		twiss_dict['x0'] 				= Lattice.orbitx0
		twiss_dict['xp0'] 				= Lattice.orbitpx0
		twiss_dict['y0'] 				= Lattice.orbity0
		twiss_dict['yp0'] 				= Lattice.orbitpy0
		twiss_dict['gamma_transition'] 	= Lattice.gammaT
		twiss_dict['circumference']    	= Lattice.getLength()
		twiss_dict['length'] 			= Lattice.getLength()/Lattice.nHarm
		
		print '\ntwiss_dict:'
		print twiss_dict

		print '\ngenerate_initial_distribution on MPI process: ', rank
		Particle_distribution_file = generate_initial_distribution_from_tomo_manual_Twiss(p, twiss_dict, matfile=1, output_file='input/ParticleDistribution.in', summary_file='input/ParticleDistribution_summary.txt')

		print '\bunch_orbit_to_pyorbit on MPI process: ', rank
		bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution_file, bunch, p['n_macroparticles'] + 1) #read in only first N_mp particles.

	else:
		print '\Loading initial distribution from file: ', p['input_distn_dir']
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
output.addParameter('01', lambda: bunchtwissanalysis.getBunchMoment(0,1))
output.addParameter('10', lambda: bunchtwissanalysis.getBunchMoment(1,0))
output.addParameter('02', lambda: bunchtwissanalysis.getBunchMoment(0,2))
output.addParameter('20', lambda: bunchtwissanalysis.getBunchMoment(2,0))
output.addParameter('11', lambda: bunchtwissanalysis.getBunchMoment(1,1))
output.addParameter('22', lambda: bunchtwissanalysis.getBunchMoment(2,2))
output.addParameter('sigma_x', lambda: GetBunchSigmas(bunch)[0])
output.addParameter('sigma_y', lambda: GetBunchSigmas(bunch)[1])

if os.path.exists(output_file):
	output.import_from_matfile(output_file)

# Track
#-----------------------------------------------------------------------
print '\nTracking on MPI process: ', rank
start_time = time.time()
last_time = time.time()

for turn in range(sts['turn']+1, sts['turns_max']):
	if not rank:	last_time = time.time()
	
	if turn == 0:
		output.addParameter('turn_time', lambda: time.strftime("%H:%M:%S"))
		output.addParameter('turn_duration', lambda: (time.time() - last_time))
		output.addParameter('cumulative_time', lambda: (time.time() - start_time))
		start_time = time.time()
		print 'start time = ', start_time

	Lattice.trackBunch(bunch, paramsDict)
	bunchtwissanalysis.analyzeBunch(bunch)  # analyze twiss and emittance
	# ~ void computeBunchMoments(Bunch* bunch, int order, int dispersionflag, int emitnormflag);
	bunchtwissanalysis.computeBunchMoments(bunch, 3, 1, 1)
	
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
