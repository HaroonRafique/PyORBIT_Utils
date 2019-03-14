import scipy.io as sio
import numpy as np
from spacecharge import SpaceChargeCalcAnalytical
from spacecharge import ConstantLineDensityProfile
from orbit_utils.errorfunctions import cerrf

# start the testing here ...

LineDensity = ConstantLineDensityProfile(6)
space_charge_solver = SpaceChargeCalcAnalytical(1, 1, 1, 1, LineDensity)

# x, y = 1*float(np.random.rand(1)), float(np.random.rand(1))

x = +0.0032853
y = -0.0067713
sigma_x = 0.0025809
sigma_y = 0.0025685

w = cerrf(x+1J*y)
print 'error_function:  ',w.real, w.imag

Ex, Ey = space_charge_solver.BassettiErskine(x, y, sigma_x, sigma_y)
print 'Ex, Ey:          ', Ex, Ey


x = np.linspace(-0.02, 0.02, 200)
y = np.linspace(-0.02, 0.02, 200)
xv, yv = np.meshgrid(x, y, sparse=False, indexing='ij')

Ex = np.zeros(xv.shape)
Ey = np.zeros(xv.shape)
for i in xrange(xv.shape[0]):
	for j in xrange(xv.shape[1]):
		Ex[i,j], Ey[i,j] = space_charge_solver.BassettiErskine(xv[i,j], yv[i,j], sigma_x, sigma_y)

sio.savemat('out.mat', {'Ex': Ex, 'Ey': Ey, 'xv': xv, 'yv': yv}, do_compression=True)

