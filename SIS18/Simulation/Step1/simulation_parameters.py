import numpy as np

#z_max = 0.77
m = 1.2
intensity =4e+10        #Ions?
epsn_x=(12.57e-6)/2. 
epsn_y=(9.30e-6)/2. 
TransverseCut = 5
n_macroparticles = int(20)
# ~ n_macroparticles = int(3e3)
macrosize = intensity/float(n_macroparticles)
#~ blength_rms = 5.96
# ~ blength_rms = (0.91*299792458*210e-9)/4.
blength_rms = (0.15448*299792458*3472.7e-9)/4. # = 40.206868
# ~ blength_rms = 40.35
#~ dpp_rms = 0.573e-3*0.91
dpp_rms = (2.5e-4)/3.
circumference= 216.7199935
rf_voltage=0.0

turns_max = 1500
turns_update = range(-1, turns_max, 100)
turns_print = turns_update[::100]

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

# these are the paramters for the PTC RF table
# ~ harmonic_factors = [1] #this times the base harmonic defines the RF harmonics (for SPS = 4620, PS 10MHz 7, 8, or 9)
# ~ #time = np.array([0,10,20])
# ~ time = np.array([0,1,2])
# ~ ones = np.ones_like(time)
# ~ Ekin_GeV = 1.4*ones
# ~ RF_voltage_MV = np.array([0.0175*ones]).T # in MV
# ~ RF_phase = np.array([np.pi*ones]).T

# ~ RFparameters = {
	# ~ 'harmonic_factors': harmonic_factors,
	# ~ 'time': time,
	# ~ 'Ekin_GeV': Ekin_GeV,
	# ~ 'voltage_MV': RF_voltage_MV,
	# ~ 'phase': RF_phase
# ~ }
