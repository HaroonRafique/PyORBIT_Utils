from tunespread import *

gamma = 2.492104532
beta = np.sqrt(gamma**2-1)/gamma
emit_x = 2.7e-6
emit_y = 2.3e-6
blength = 210
q = 1
n_part = 2e+12
harmonic = 7
bunching_factor = 0.356
l_shape = harmonic/bunching_factor

# 1.3 eVs
deltap =  9.81e-04



twissfile = ['ptc_twiss.tfs']
params = {'n_part': n_part, 'emit_norm_x': emit_x, 'emit_norm_y': emit_y, 'gamma': gamma, 'deltap': deltap, 'n_charges_per_part': q, 'lshape':1., 'bunch_length': blength, 'coasting': False} 
#params = {'n_part': n_part, 'emit_norm_x': emit_x, 'emit_norm_y': emit_y, 'gamma': gamma, 'deltap': deltap, 'n_charges_per_part': q, 'lshape':l_shape, 'bunch_length': blength, 'coasting': False} 
data, inputs = ext.get_inputs(twissfile, params, False, False)
dQ = calc_tune_spread(data, inputs)
print inputs
ext.print_verbose_output(inputs, data, dQ[0], dQ[1])
print "dQx = %2.3f, dQy = %2.3f"%(dQ[0], dQ[1])

