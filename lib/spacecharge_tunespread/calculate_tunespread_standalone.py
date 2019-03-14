# Standalone example of how to use Adrian Oeftiger's (CERN BE-ABP-HSC)
# Tunespread calculator using PS MD4224 parameters (High Brightness)
from tunespread import *

# Commented out parameters are for output comparison only
deltap =	0.000981
#lshape =	1.0
#coasting =	False
#beta =	0.9159915293877255
#n_charges_per_part = 1
#emit_geom_x = 8.917531408835412e-07
#emit_geom_y = 9.745337615254807e-07
#bunch_length = 210.0
sig_z =	14.416885985372089
n_part = 7.5e+11
#Ekin = 1.40040597015
#machine	= PS
#mass = 0.938272
#deltaE = 0.0008230987127537733
emit_x = 2.036e-06
gamma = 2.49253731343
emit_y = 2.225e-06

# Tunespreads given with these parameters:
#dQx = 0.100
#dQy = 0.116

# TWISS file is provided
twissfile = ['madx_twiss_PS_tunespread_example.tfs']

params = {
	'n_part': n_part,
	'emit_norm_x': emit_x,
	'emit_norm_y': emit_y,
	'gamma': gamma,
	'deltap': deltap,
	'n_charges_per_part': 1,
	'lshape':1.,
	'sig_z': sig_z,
	'coasting': False} 
	
data, inputs = ext.get_inputs(twissfile, params, False, False)
dQ = calc_tune_spread(data, inputs)

print inputs
ext.print_verbose_output(inputs, data, dQ[0], dQ[1])
print "dQx = %2.3f, dQy = %2.3f"%(dQ[0], dQ[1])

