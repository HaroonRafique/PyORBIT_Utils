import numpy as np

beta = 0.915961016423
m = 1.2
intensity =2e+12
epsn_x=2.26e-6 
epsn_y=2.134e-6 
TransverseCut = 5
n_macroparticles = int(10)
macrosize = intensity/float(n_macroparticles)
blength_rms = (beta*299792458*210e-9)/4.
dpp_rms = 9.08e-04
circumference= 2*np.pi*100
rf_voltage = 0.0175e6
turns_max = int(3000)
turns_update = range(-1, turns_max, 1E0)
turns_print =  range(-1, turns_max, 1E0)

parameters = {
	'LongitudinalJohoParameter': m,
	'LongitudinalCut': 2.4,
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
	'Frozen': 0,
	'SC_x_gridsize': 16,
	'SC_y_gridsize': 16,
	'SC_z_gridsize': 16
}

# these are the paramters for the PTC RF table
harmonic_factors = [1] #this times the base harmonic defines the RF harmonics (for SPS = 4620, PS 10MHz 7, 8, or 9)
#time = np.array([0,10,20])
time = np.array([0,1,2])
ones = np.ones_like(time)
Ekin_GeV = 1.4*ones
RF_voltage_MV = np.array([0.0175*ones]).T # in MV
RF_phase = np.array([np.pi*ones]).T

RFparameters = {
	'harmonic_factors': harmonic_factors,
	'time': time,
	'Ekin_GeV': Ekin_GeV,
	'voltage_MV': RF_voltage_MV,
	'phase': RF_phase
}
