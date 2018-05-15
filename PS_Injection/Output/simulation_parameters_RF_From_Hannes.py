import numpy as np

# z_max, m = 0.73, 4.29 # fitted from measured profile for single RF
# z_max, m = 0.77, 4.18 # fitted from measured profile for double RF
z_max, m = 0.72, 3.06 # fitted from measured profile for double RF
intensity = 1.3e11 #[0.83*1.5e+11, 0.17*1.5e+11]
epsn_x = 1.72e-6 #[1.30e-6, 5.0e-6]
epsn_y = 1.69e-6 #[1.41e-6, 4.3e-6]
TransverseCut = 15
n_macroparticles = 5000
macrosize = np.sum(intensity)/float(n_macroparticles)

turns_max = 60000 #130000
turns_update = range(-1, turns_max, 100)
turns_print = turns_update[::10]

parameters = {
	'LongitudinalJohoParameter': m,
	'LongitudinalDistribution_z_max': z_max,
	'n_macroparticles': n_macroparticles,
	'intensity': intensity,
	'epsn_x': epsn_x,
	'epsn_y': epsn_y,
	'TransverseCut': TransverseCut,
	'macrosize': macrosize,
	'turns_max': turns_max,
	'turns_update': turns_update,
	'turns_print': turns_print
}

# these are the paramters for the PTC RF table
harmonic_factors = [1,4] #this times the base harmonic defines the RF harmonics (for SPS = 4620)
time = np.array([0,10,20])
ones = np.ones_like(time)
Ekin_GeV = 25.0786523715676*ones
RF_voltage_MV = np.array([3.0/4620*ones, 0.0*ones]).T # in MV
RF_phase = np.array([0.0*ones, 0.0*ones]).T

RFparameters = {
	'harmonic_factors': harmonic_factors,
	'time': time,
	'Ekin_GeV': Ekin_GeV,
	'voltage_MV': RF_voltage_MV,
	'phase': RF_phase
}
