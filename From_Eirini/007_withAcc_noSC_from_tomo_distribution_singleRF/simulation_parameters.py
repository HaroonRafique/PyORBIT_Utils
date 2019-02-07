import numpy as np

tomo_matfile = 'tomoscope_file/tomo_data_singleRF_EKP_297.mat'
intensity = 1.6e+13 # future ISOLDE beam
epsn_x = 2e-6
epsn_y = 2e-6
TransverseCut = 15
n_macroparticles = 500000
macrosize = np.sum(intensity)/float(n_macroparticles)

turns_max = 1000#10000
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
#time = np.array([0,10,20])
time = np.arange(0.00000, 0.02100, 0.00100)
ones = np.ones_like(time)
#Ekin_GeV = 0.050*ones
#with acceleration
Ekin_GeV = np.array([0.16000000, 0.16156116, 0.16312827, 0.16470131, 0.16628024, 0.16786504, 0.16945569, 0.17105215, 0.17265442, 0.17426245, 0.17587624, 0.17749574, 0.17912094, 0.18075180, 0.18238832, 0.18403046, 0.18567819, 0.18733150, 0.18899036, 0.19065474, 0.19232462])
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
