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

from lib.output_dictionary import *
from lib.pyOrbit_GenerateInitialDistribution2 import *
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
#----------------------------------------------
# Dictionary for simulation status
#----------------------------------------------
import pickle
status_file = 'input/simulation_status.pkl'
if not os.path.exists(status_file):
	sts = {'turn': -1}
else: 
	with open(status_file) as fid:
		sts = pickle.load(fid)
	from simulation_parameters import parameters as p
	if sts['turns_max']<p['turns_max']:
		sts['turns_max'] = p['turns_max']
		sts['turns_update'] = p['turns_update']
		sts['turns_print'] = p['turns_print']
''
#----------------------------------------------
# Generate Lattice (MADX + PTC)
#----------------------------------------------
if not rank:
	os.system("/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < FODO.madx")
orbit_mpi.MPI_Barrier(comm)
''

#----------------------------------------------
# Initialize a Teapot-Style PTC lattice
#----------------------------------------------
PTC_File = "SPACE_CHARGE_STUDIES_INJECTION.flt"
Lattice = PTC_Lattice("PS")
Lattice.readPTC(PTC_File)
readScriptPTC('Input/fringe.txt')
readScriptPTC('Input/time.ptc')
readScriptPTC('Input/chrom.ptc')

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
if sts['turn'] < 0:
	bunch = Bunch()
	setBunchParamsPTC(bunch)
	
	from simulation_parameters import parameters as p
	p['harmonic_number'] = Lattice.nHarm 
	p['rf_voltage']      = 0.025e6
	p['phi_s']           = 0
	p['gamma']           = bunch.getSyncParticle().gamma()
	p['beta']            = bunch.getSyncParticle().beta()
	p['energy']          = 1e9 * bunch.mass() * bunch.getSyncParticle().gamma()
	p['bunch_length'] = p['blength_rms']/speed_of_light/bunch.getSyncParticle().beta()*4
	kin_Energy = bunch.getSyncParticle().kinEnergy()
	Particle_distribution_file = generate_initial_distribution(p, Lattice, 
								output_file='input/ParticleDistribution.in',
								summary_file='input/ParticleDistribution_summary.txt')


	bunch_orbit_to_pyorbit(paramsDict["length"], kin_Energy, Particle_distribution_file, bunch, p['n_macroparticles'] + 1) #read in only first N_mp particles.
	bunch.addPartAttr("macrosize")
	map(lambda i: bunch.partAttrValue("macrosize", i, 0, p['macrosize']), range(bunch.getSize()))
	ParticleIdNumber().addParticleIdNumbers(bunch) # Give them unique number IDs
	bunch.dumpBunch("input/mainbunch_start.dat")
	saveBunchAsMatfile(bunch, "input/mainbunch")
	sts['mainbunch_file'] = "input/mainbunch"
	lostbunch = Bunch()
	bunch.copyEmptyBunchTo(lostbunch)
	lostbunch.addPartAttr('ParticlePhaseAttributes')
	lostbunch.addPartAttr("LostParticleAttributes")
	saveBunchAsMatfile(lostbunch, "input/lostbunch")
	paramsDict["lostbunch"]=lostbunch
	paramsDict["bunch"]= bunch
	sts['turns_max'] = p['turns_max']
	sts['turns_update'] = p['turns_update']
	sts['turns_print'] = p['turns_print']
	sts['lostbunch_file'] = "input/lostbunch"
	sts['circumference'] = p['circumference']

bunch = bunch_from_matfile(sts['mainbunch_file'])
lostbunch = bunch_from_matfile(sts['lostbunch_file'])
paramsDict["lostbunch"]=lostbunch
paramsDict["bunch"]= bunch

#----------------------------------------------------
# Add space charge nodes
#----------------------------------------------------
print '\nSetting up the space charge calculations ...'
# Make a SC solver using frozen potential
density=np.loadtxt('density_2.dat', dtype=float)
sc_path_length_min = 0.00000001
#ld_profile = p['linedensity_profile']
LineDensity=InterpolatedLineDensityProfile(-12.5,12.5,density.tolist())
sc_params1 = {'intensity': p['intensity'], 'epsn_x': p['epsn_x'], 'epsn_y': p['epsn_y'], 'dpp_rms': p['dpp_rms'], 'LineDensity': LineDensity}
space_charge_solver1 = SpaceChargeCalcAnalyticGaussian(*[sc_params1[k] for k in ['intensity','epsn_x','epsn_y','dpp_rms','LineDensity']])
sc_nodes1 = scLatticeModifications.setSCanalyticalAccNodes(Lattice, sc_path_length_min, space_charge_solver1)
sc_params2 = {'intensity': 0, 'epsn_x': p['epsn_x'], 'epsn_y': p['epsn_y'], 'dpp_rms': p['dpp_rms'], 'LineDensity': LineDensity}
space_charge_solver2 = SpaceChargeCalcAnalyticGaussian(*[sc_params2[k] for k in ['intensity','epsn_x','epsn_y','dpp_rms','LineDensity']])
sc_nodes2 = scLatticeModifications.setSCanalyticalAccNodes(Lattice, sc_path_length_min, space_charge_solver2)
print '  Installed %i + %i space charge nodes'%(len(sc_nodes1), len(sc_nodes2))


#-----------------------------------------------------
# Add tune analysis child node
#-----------------------------------------------------
parentnode_number = 97
parentnode = Lattice.getNodes()[parentnode_number]
Twiss_at_parentnode_entrance = Lattice.getNodes()[parentnode_number-1].getParamsDict()
tunes = TeapotTuneAnalysisNode("tune_analysis")
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
# Grid objects to do histograms of distribution
#----------------------------------------------------
from lib.bunch_profiles import *
bunchProfiles = Bunch_Profile(100,50,24)
twiss_dict = {'betax': Lattice.betax0, 'betay': Lattice.betay0, 'etax': Lattice.etax0, 'etay': Lattice.etay0}
# use before tracking to get initial Gaussian fits
bunchProfiles.bin_bunch(bunch, twiss_dict)
Gauss_epsn, _ = bunchProfiles.transverse_emittances_Gauss()


#----------------------------------------------------
# Define twiss analysis and output dictionary
#----------------------------------------------------
bunchtwissanalysis = BunchTwissAnalysis() #Prepare the analysis class that will look at emittances, etc.
get_dpp = lambda b, bta: np.sqrt(bta.getCorrelation(5,5)) / (b.getSyncParticle().gamma()*b.mass()*b.getSyncParticle().beta()**2)
get_bunch_length = lambda b, bta: 4 * np.sqrt(bta.getCorrelation(4,4)) / (speed_of_light*b.getSyncParticle().beta())
get_eps_z = lambda b, bta: 1e9 * 4 * pi * bta.getEmittance(2) / (speed_of_light*b.getSyncParticle().beta())

output_file = 'output/output_%s.mat'%str(sts['turn'])
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
output.addParameter('BE_intensity1', lambda: sc_params1['intensity'])
output.addParameter('BE_epsn_x1', lambda: sc_params1['epsn_x'])
output.addParameter('BE_epsn_y1', lambda: sc_params1['epsn_y'])
output.addParameter('BE_dpp_rms1', lambda: sc_params1['dpp_rms'])
output.addParameter('BE_intensity2', lambda: sc_params2['intensity'])
output.addParameter('BE_epsn_x2', lambda: sc_params2['epsn_x'])
output.addParameter('BE_epsn_y2', lambda: sc_params2['epsn_y'])
output.addParameter('BE_dpp_rms2', lambda: sc_params2['dpp_rms'])
output.addParameter('Gauss_epsn_x', lambda: Gauss_epsn['x'])
output.addParameter('Gauss_epsn_y', lambda: Gauss_epsn['y'])
if os.path.exists(output_file):
	output.import_from_matfile(output_file)


#----------------------------------------------------
# Do some turns and dump particle information
#----------------------------------------------------
print '\nnow start tracking...'

for turn in range(sts['turn']+1, sts['turns_max']):
	Lattice.trackBunch(bunch, paramsDict)
	bunchtwissanalysis.analyzeBunch(bunch)  # analyze twiss and emittance	
	
	# subtract circumference each turn in order to reconstruct the turn number from loss position
	map(lambda i: lostbunch.partAttrValue("LostParticleAttributes", i, 0, 
					  lostbunch.partAttrValue("LostParticleAttributes", i, 0)-p['circumference']), xrange(lostbunch.getSize()))

	bunch.addParticlesTo(bunch_tmp)	
	if turn in p['turns_update']:
		bunchProfiles.bin_bunch(bunch_tmp, twiss_dict)
		bunchProfiles.save_bunchprofile_to_matfile('output/bunch_profile_%s.mat'%(str(turn).zfill(6)))
		Gauss_epsn, _ = bunchProfiles.transverse_emittances_Gauss()
		epsn_Gauss1, epsn_Gauss2, amplitude_Gauss1, amplitude_Gauss2 = bunchProfiles.transverse_emittances_combinedDoubleGauss()
		sc_params1['intensity'] = bunchtwissanalysis.getGlobalMacrosize() * amplitude_Gauss1
		sc_params1['epsn_x'] = epsn_Gauss1['x']
		sc_params1['epsn_y'] = epsn_Gauss1['y']
		sc_params1['dpp_rms'] = get_dpp(bunch, bunchtwissanalysis)
		sc_params2['intensity'] = bunchtwissanalysis.getGlobalMacrosize() * amplitude_Gauss2
		sc_params2['epsn_x'] = epsn_Gauss2['x']
		sc_params2['epsn_y'] = epsn_Gauss2['y']
		sc_params2['dpp_rms'] = get_dpp(bunch, bunchtwissanalysis)
		
		# # update SC solver		
		ld_profile = bunchProfiles.grid_arrs_norm_dict['z']
		LineDensity = InterpolatedLineDensityProfile(min(ld_profile[0]), max(ld_profile[0]), ld_profile[1].tolist())
		space_charge_solver1.setLineDensityProfile(LineDensity)
		space_charge_solver1.setBunchParameters(*[sc_params1[k] for k in ['intensity','epsn_x','epsn_y','dpp_rms']])
		space_charge_solver2.setLineDensityProfile(LineDensity)
		space_charge_solver2.setBunchParameters(*[sc_params2[k] for k in ['intensity','epsn_x','epsn_y','dpp_rms']])


		# reset the temp bunch 
		sts['turn']=turn
		bunch_tmp.deleteAllParticles()

	if turn in p['turns_print']:
		saveBunchAsMatfile(bunch, "output/mainbunch_%s"%(str(turn).zfill(6)))

	if turn in sts['turns_print']:
		saveBunchAsMatfile(bunch, "input/mainbunch")
		saveBunchAsMatfile(lostbunch, "input/lostbunch")
		output.save_to_matfile(output_file)
		readScriptPTC('ptc/write_FINAL_SETTINGS.ptc')
		if not rank:
			with open(status_file, 'w') as fid:
				pickle.dump(sts, fid)
	output.update()
