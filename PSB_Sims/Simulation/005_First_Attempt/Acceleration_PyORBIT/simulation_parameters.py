import numpy as np

LIU = 0	#switch for 160 MeV sim

if LIU: # 160 MeV PSB
	beta_l = 0.5198122836207495
	gamma_l = 1.17057569296

else: # 50 MeV PSB
	beta =  0.3140915111170623
	gamma =  1.05330490405

# This is a guess - need to check - not needed for tomo bunch
#blength_rms = (beta_l*299792458*150e-9)/4.

# ~ tomo_matfile = 'tomoscope_file/tomo_data_H_nomWorkPoint_ct_297_turns2.76.mat'
tomo_matfile = 'tomoscope_file/PyORBIT_Tomo_file'

intensity = 1.6e+13 # future ISOLDE beam
epsn_x = 2e-6
epsn_y = 2e-6
TransverseCut = 5

turns_max = int(10000)
n_macroparticles = int(1)

macrosize = np.sum(intensity)/float(n_macroparticles)
turns_print = range(-1, turns_max, int(100))

phase_offset = 0.0 # manual fudge for longitudinal bunch matching

parameters = {
	#'blength_rms': blength_rms,
	'tomo_file': tomo_matfile,
	'tomo_matfile': tomo_matfile,
	'n_macroparticles': n_macroparticles,
	'intensity': intensity,
	'epsn_x': epsn_x,
	'epsn_y': epsn_y,
	'TransverseCut': TransverseCut,
	'macrosize': macrosize,
	'turns_max': turns_max,
	'turns_print': turns_print,
	'phase_offset': phase_offset
}

# these are the paramters for the PTC RF table
harmonic_factors = [1,2] #this times the base harmonic defines the RF harmonics (for SPS = 4620)

#160 MeV with acceleration
if LIU:
	time = np.arange(0.00000, 0.02100, 0.00100)
	Ekin_GeV = np.array([0.16000000, 0.16156116, 0.16312827, 0.16470131, 0.16628024, 0.16786504, 0.16945569, 0.17105215, 0.17265442, 0.17426245, 0.17587624, 0.17749574, 0.17912094, 0.18075180, 0.18238832, 0.18403046, 0.18567819, 0.18733150, 0.18899036, 0.19065474, 0.19232462])
else:
# 50 MeV from Fanouria - May have to put into linear time steps
	time = np.array([0.0, 0.010000000000000009, 0.019999999999999962, 0.02999999999999997, 0.03999999999999998, 0.04999999999999999, 0.06, 0.07, 0.07999999999999996, 0.08999999999999997, 0.09999999999999998, 0.10999999999999999, 0.12, 0.13, 0.14, 0.14999999999999997, 0.15999999999999998, 0.16999999999999998, 0.18, 0.19, 0.2, 0.20999999999999996, 0.21999999999999997, 0.22999999999999998, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29000000000000004, 0.30000000000000004, 0.30999999999999994, 0.31999999999999995, 0.32999999999999996, 0.33999999999999997, 0.35, 0.36, 0.38, 0.39, 0.4, 0.41000000000000003, 0.42000000000000004, 0.42999999999999994, 0.43999999999999995, 0.44999999999999996, 0.45999999999999996, 0.47, 0.48, 0.49, 0.53])
	Ekin_GeV = np.array([0.05092657218462217, 0.05530310500295544, 0.06056773908625734, 0.06667047579103447, 0.07354673373394978, 0.08114091290566743, 0.08948358375354254, 0.09867541793534303, 0.10876766184281325, 0.11986418271897913, 0.13207915635397757, 0.1455145481327777, 0.16027313706948568, 0.17642297051820563, 0.19407235243560672, 0.21332812491140174, 0.23425765216767716, 0.2569270975331614, 0.2813932861920538, 0.30770926451866004, 0.33592429065766455, 0.3660786456968753, 0.39826115638562154, 0.43265285143539955, 0.4691937307292421, 0.5075247116503558, 0.5475850719787457, 0.5893253158718631, 0.632387228111763, 0.6765520628018611, 0.7216588788616335, 0.7675638942962394, 0.8142287077645453, 0.8616701430619514, 0.9099054807973368, 0.958527036307736, 1.0066844863875801, 1.101197498377649, 1.146914177107768, 1.1903899964202649, 1.2309511550085912, 1.2679652303508357, 1.3013823987593813, 1.331110200932921, 1.3572950184339314, 1.377403531545287, 1.3896887281436991, 1.3970637869324736, 1.4000000001685113, 1.4000000001685113])

# ~ RF_voltage_MV = np.array([.008*ones, .006*ones]).T # double harmonic 8KV 6KV
# Ekin_GeV = np.array(np.ones_like(time)*0.05) # Constant energy 50 MeV

ones = np.ones_like(time)
RF_voltage_MV = np.array([.008*ones, .0*ones]).T # single harmonic 8KV
RF_phase = np.array([(1+np.pi)*ones, 0.*ones]).T # appears to be correct

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
