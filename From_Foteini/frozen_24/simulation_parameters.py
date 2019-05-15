import numpy as np

#z_max = 0.77
m = 1.2
intensity = 4.1e+11
epsn_x=4.5e-6 
epsn_y=4e-6 
TransverseCut = 5
n_macroparticles = 3000
macrosize = intensity/float(n_macroparticles)
blength_rms = 5.96
dpp_rms = 0.573e-3*0.91
circumference= 621.

turns_max = 100000
turns_update = range(-1, turns_max, 100)
turns_print = turns_update[::10]

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
        'circumference':circumference
}

