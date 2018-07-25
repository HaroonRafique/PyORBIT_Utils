import numpy as np

tomo_matfile = 'tomoscope_file/tomo_data_singleRF_EKP_297.mat'
intensity = 1.6e+13 # future ISOLDE beam
epsn_x = 2e-6
epsn_y = 2e-6
TransverseCut = 15
n_macroparticles = 500000
macrosize = np.sum(intensity)/float(n_macroparticles)

turns_max = 10000
turns_print = range(-1, turns_max, 100)

parameters = {
	'tomo_matfile': tomo_matfile,
	'n_macroparticles': n_macroparticles,
	'intensity': intensity,
	'epsn_x': epsn_x,
	'epsn_y': epsn_y,
	'TransverseCut': TransverseCut,
	'macrosize': macrosize,
	'turns_max': turns_max,
	'turns_print': turns_print
}

# these are the paramters for the PTC RF table
harmonic_factors = [1] #this times the base harmonic defines the RF harmonics (for SPS = 4620)
time = np.array([0,10,20])
ones = np.ones_like(time)
Ekin_GeV = 0.050*ones
RF_voltage_MV = np.array([.008*ones]).T # in MV
RF_phase = np.array([3.14159*ones]).T
#RF_phase = np.array([0*ones]).T

RFparameters = {
	'harmonic_factors': harmonic_factors,
	'time': time,
	'Ekin_GeV': Ekin_GeV,
	'voltage_MV': RF_voltage_MV,
	'phase': RF_phase
}
