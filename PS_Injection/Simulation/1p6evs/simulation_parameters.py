import numpy as np

#z_max = 0.77
m = 1.2
intensity =2e+12
epsn_x=2.26e-6 
epsn_y=2.134e-6 
TransverseCut = 5
# ~ n_macroparticles = int(500e3)
n_macroparticles = int(50e3)
macrosize = intensity/float(n_macroparticles)
#~ blength_rms = 5.96
blength_rms = (0.91*299792458*210e-9)/4.
#~ dpp_rms = 0.573e-3*0.91
dpp_rms = 1.08e-03*0.91
circumference= 2*np.pi*100
rf_voltage=0.0261e6
turns_max = int(1E4)	#
# ~ turns_max = 2			# Tune Footprint
turns_update = range(-1, turns_max, 100)
turns_print =  range(-1, turns_max, 100)

parameters = {
	'LongitudinalJohoParameter': m,
	'LongitudinalCut': 2.4,
	#'LongitudinalDistribution_z_max': z_max,
	'blength_rms': blength_rms,
	'n_macroparticles': n_macroparticles,
	'intensity': intensity,
	'epsn_x': epsn_x,
	'epsn_y': epsn_y,
	'dpp_rms': dpp_rms,
	'TransverseCut': TransverseCut,
	'macrosize': macrosize,
	'turns_max': turns_max,
	'turns_update': turns_update,
	'turns_print': turns_print,
	'rf_voltage': rf_voltage,
	'circumference':circumference
}

switches = {
	'Horizontal': 1,
	'SliceBySlice': 0,
	'Frozen': 0
}

# these are the paramters for the PTC RF table
harmonic_factors = [1] #this times the base harmonic defines the RF harmonics (for SPS = 4620, PS 10MHz 7, 8, or 9)
#time = np.array([0,10,20])
time = np.array([0,1,2])
ones = np.ones_like(time)
Ekin_GeV = 1.4*ones
RF_voltage_MV = np.array([0.0261*ones]).T # in MV
RF_phase = np.array([np.pi*ones]).T

RFparameters = {
	'harmonic_factors': harmonic_factors,
	'time': time,
	'Ekin_GeV': Ekin_GeV,
	'voltage_MV': RF_voltage_MV,
	'phase': RF_phase
}
