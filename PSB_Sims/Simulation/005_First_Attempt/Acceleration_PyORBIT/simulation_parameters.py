import numpy as np

# ~ tomo_matfile = 'tomoscope_file/tomo_data_H_nomWorkPoint_ct_297_turns2.76.mat'
tomo_matfile = 'tomoscope_file/PyORBIT_Tomo_file'
intensity = 1.6e+13 # future ISOLDE beam
epsn_x = 2e-6
epsn_y = 2e-6
TransverseCut = 5
n_macroparticles = int(1) #50000 #500000
macrosize = np.sum(intensity)/float(n_macroparticles)

beta_l = 0.5198122836207495
gamma_l = 1.17057569296

# This is a guess - need to check
blength_rms = (beta_l*299792458*150e-9)/4.

turns_max = int(10000) #10000
turns_print = range(-1, turns_max, int(1))

parameters = {
	'blength_rms': blength_rms,
	'tomo_file': tomo_matfile,
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
harmonic_factors = [1,2] #this times the base harmonic defines the RF harmonics (for SPS = 4620)
time = np.arange(0.00000, 0.02100, 0.00100)
ones = np.ones_like(time)
#with acceleration
Ekin_GeV = np.array([0.16000000, 0.16156116, 0.16312827, 0.16470131, 0.16628024, 0.16786504, 0.16945569, 0.17105215, 0.17265442, 0.17426245, 0.17587624, 0.17749574, 0.17912094, 0.18075180, 0.18238832, 0.18403046, 0.18567819, 0.18733150, 0.18899036, 0.19065474, 0.19232462])
RF_voltage_MV = np.array([.008*ones, .006*ones]).T # in MV
RF_phase = np.array([3.14159*ones, 0.*ones]).T

'''
RF_phase = np.zeros((21,2))
RF_phase[0,0] = 3.14159
RF_phase[1,0] = 3.14159
RF_phase[2,0] = RF_phase[1,0] + 0.1
RF_phase[3,0] = RF_phase[2,0] + 0.1
RF_phase[4,0] = RF_phase[3,0] + 0.1
RF_phase[5,0] = RF_phase[4,0] + 0.1
RF_phase[6:,0] = 3.14159 + 0.5

RF_phase[0,1] = 2.*np.pi
RF_phase[1,1] = 2.*np.pi
RF_phase[2,1] = RF_phase[1,1] + 0.1
RF_phase[3,1] = RF_phase[2,1] + 0.1
RF_phase[4,1] = RF_phase[3,1] + 0.1
RF_phase[5,1] = RF_phase[4,1] + 0.1
RF_phase[6:,1] = 2.*np.pi + 0.5
'''

RFparameters = {
	'harmonic_factors': harmonic_factors,
	'time': time,
	'Ekin_GeV': Ekin_GeV,
	'voltage_MV': RF_voltage_MV,
	'phase': RF_phase
}
