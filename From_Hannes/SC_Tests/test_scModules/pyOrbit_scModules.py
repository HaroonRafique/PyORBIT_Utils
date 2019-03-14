from math import sqrt
import sys
import numpy as np

from orbit.utils.orbit_mpi_utils import bunch_orbit_to_pyorbit, bunch_pyorbit_to_orbit
from bunch import Bunch
from bunch import BunchTwissAnalysis, BunchTuneAnalysis
from orbit.utils.consts import mass_proton, speed_of_light, pi
from orbit.bunch_generators import TwissContainer
from orbit.bunch_generators import WaterBagDist1D, GaussDist1D, KVDist1D
from orbit.bunch_generators import WaterBagDist2D, GaussDist2D, KVDist2D
from orbit.injection import JohoTransverse, JohoLongitudinal
from spacecharge import SpaceChargeCalc3D
from spacecharge import SpaceChargeCalcSliceBySlice2D
from spacecharge import SpaceChargeCalc2p5D
from spacecharge import SpaceChargeCalcAnalytical
from spacecharge import GaussianLineDensityProfile
from spacecharge import InterpolatedLineDensityProfile
from spacecharge import Grid1D
from orbit_utils import BunchExtremaCalculator

print "Start."


#----------------------------------------------
# Bunch Parameters
#----------------------------------------------

Intensity = 2e+11
m0 = mass_proton 	# protons ...
N_mp = 2000000
macrosize = Intensity/N_mp
# energy = 0.000010 # GeV
energy = 10 # GeV

#----------------------------------------------
# Add the main bunch and lost particles bunch
#----------------------------------------------

print '\nAdding main bunch ...'

# Generate bunch particles
bunch = Bunch()
bunch.addPartAttr("macrosize")
bunch.getSyncParticle().kinEnergy(energy)


bunch_file = None
if bunch_file:
	bunch.readBunch(bunch_file)
else:
	# twissX = TwissContainer(alpha = 0., beta = 54., emittance = 1e-6/bunch.getSyncParticle().gamma()/bunch.getSyncParticle().beta())
	# twissY = TwissContainer(alpha = 0., beta = 40., emittance = 1e-6/bunch.getSyncParticle().gamma()/bunch.getSyncParticle().beta())
	twissX = TwissContainer(alpha = 0., beta = 1., emittance = 1e-2)
	twissY = TwissContainer(alpha = 0., beta = 1., emittance = 1e-2)
	# Gauss 2D distribution function
	dist2D = GaussDist2D(twissX,twissY)
	# Uniform 2D distribution
# 	dist2D = KVDist2D(twissX,twissY)
	
	# Longitudinal distribution function
	order = 1.5 #.5 #1 #1.5 #2
	zlim = 0.5*10
	dElim = 0.001
	nlongbunches = 1
	deltazbunch = 0.5
	deltaznotch = 0.
	ltailfrac = 0
	ltailfac = 0
	dist1D = JohoLongitudinal(order, zlim, dElim, nlongbunches, deltazbunch, deltaznotch, ltailfrac, ltailfac)

	for i in xrange(N_mp):
		(x,xp,y,yp) = dist2D.getCoordinates()
		(z, dE) = dist1D.getCoordinates()
		bunch.addParticle(x,xp,y,yp,z,dE)
		bunch.partAttrValue("macrosize", i, 0, macrosize)
	# add test particles
	bunch_extrema_cal = BunchExtremaCalculator()
	x_min, x_max, y_min, y_max, z_min, z_max = bunch_extrema_cal.extremaXYZ(bunch)
	x_center = (x_max+x_min)/2
	x_size = x_max-x_min
	x_test = np.linspace(x_center - 1.5*x_size/2, x_center + 1.5*x_size/2, 300)
	y_center = (y_max+y_min)/2
	y_size = y_max-y_min
	y_test = np.linspace(y_center - 1.5*y_size/2, y_center + 1.5*y_size/2, 300)
	z_center = (z_max+z_min)/2
	z_size = z_max-z_min
	z_test = np.linspace(z_center - 1.0*z_size/2, z_center + 1.0*z_size/2, 300)
	for i in xrange(len(x_test)):
		bunch.addParticle(x_test[i],0,0,0,0,0)
	for i in xrange(len(y_test)):
		bunch.addParticle(0,0,y_test[i],0,0,0)
	for i in xrange(len(z_test)):
		bunch.addParticle(x_center+x_size/10.,0,y_center-y_size/10.,0,z_test[i],0)
	# bunch.dumpBunch('bunch.dat')

print 'Momentum: \t', bunch.getSyncParticle().momentum(), 'GeV'
print 'Ekin: \t\t', bunch.getSyncParticle().kinEnergy(), 'GeV' 
print 'Gamma: \t\t',bunch.getSyncParticle().gamma(),  'GeV'
print 'Beta: \t\t', bunch.getSyncParticle().beta()
print 'Charge: \t', bunch.charge(), 'e'
print 'Mass: \t\t', bunch.mass(), 'GeV'

# give horizontal offset to the bunch
for i in range(bunch.getSize()):
	x = bunch.x(i)
	bunch.x(i, x+0.0)
	y = bunch.y(i)
	bunch.y(i, y-0.0)

TwissAnalysis = BunchTwissAnalysis()
TwissAnalysis.analyzeBunch(bunch)
sigma_x = sqrt(TwissAnalysis.getCorrelation(0,0))
sigma_y = sqrt(TwissAnalysis.getCorrelation(2,2))
sigma_z = sqrt(TwissAnalysis.getCorrelation(4,4))

print '\nsigma_x=', sigma_x
print 'sigma_y=', sigma_y
print 'sigma_z=', sigma_z

	
#----------------------------------------------
# Create SC solvers
#----------------------------------------------

integration_length = 1.
sizeX = 128*2
sizeY = 128*2
nBinsZ = 32*2

# 2p5D solver ####
sc_calc_2p5d = SpaceChargeCalc2p5D(sizeX, sizeY, nBinsZ)

# slice-by-slice solver
sc_CalcSliceBySlice = SpaceChargeCalcSliceBySlice2D(sizeX,sizeY,nBinsZ)

# 3D solver
sc_3Dsolver = SpaceChargeCalc3D(sizeX,sizeY,nBinsZ)

# Analytical solver ####
# with Gaussian Line Density ####
# LineDensity = GaussianLineDensityProfile(sigma_z)
# with LineDensity from bunch distribution (remember: we give normalized number of particles per meter!) ####
bunch_extrema_cal = BunchExtremaCalculator()
z_min, z_max = bunch_extrema_cal.extremaZ(bunch)
LongitudinalGrid = Grid1D(nBinsZ)
LongitudinalGrid.setGridZ(z_min, z_max)
LongitudinalGrid.binBunch(bunch)
lambda_arr = []
Grid_sum = LongitudinalGrid.getSum()
for i in xrange(nBinsZ+1):
	lambda_arr.append(LongitudinalGrid.getValue(z_min+i*LongitudinalGrid.getStepZ())/Grid_sum/LongitudinalGrid.getStepZ())
LineDensity = InterpolatedLineDensityProfile(z_min, z_max, lambda_arr)
dpp_rms = sqrt(TwissAnalysis.getCorrelation(5,5))/(bunch.getSyncParticle().kinEnergy()+bunch.getSyncParticle().mass() / bunch.getSyncParticle().beta()**2)
sc_analytical = SpaceChargeCalcAnalytical(Intensity, TwissAnalysis.getEmittanceNormalized(0), TwissAnalysis.getEmittanceNormalized(1), dpp_rms, LineDensity)
sc_analytical.setLatticeParameters(TwissAnalysis.getBeta(0), TwissAnalysis.getBeta(1), TwissAnalysis.getDispersion(0), TwissAnalysis.getDispersion(1), TwissAnalysis.getAverage(0), TwissAnalysis.getAverage(2))

#----------------------------------------------
# Compare the kicks of the SC solvers
#----------------------------------------------

def reset_bunch_momenta(bunch):
	for i in xrange(bunch.getSize()):
		bunch.xp(i, 0)
		bunch.yp(i, 0)
		bunch.dE(i, 0)

x = np.array(map(bunch.x, xrange(bunch.getTotalCount())))
y = np.array(map(bunch.y, xrange(bunch.getTotalCount())))
z = np.array(map(bunch.z, xrange(bunch.getTotalCount())))

# fx = open('scAnalytical.txt', 'w')
reset_bunch_momenta(bunch)
sc_analytical.trackBunch(bunch, integration_length)
xp_Analytical = np.array(map(bunch.xp, xrange(bunch.getTotalCount())))
yp_Analytical = np.array(map(bunch.yp, xrange(bunch.getTotalCount())))
dE_Analytical = np.array(map(bunch.dE, xrange(bunch.getTotalCount())))
# for i in xrange(len(z)):
# 	fx.write(str(x[i]) + ', ' + str(y[i]) + ', ' + str(z[i]) + ', ' + str(xp_Analytical[i]) + ', ' + str(yp_Analytical[i]) + ', ' + str(dE_Analytical[i])+'\n')
# fx.close()

# fx = open('sc2p5D.txt', 'w')
reset_bunch_momenta(bunch)
sc_calc_2p5d.trackBunch(bunch, integration_length)
xp_2p5D = np.array(map(bunch.xp, xrange(bunch.getTotalCount())))
yp_2p5D = np.array(map(bunch.yp, xrange(bunch.getTotalCount())))
dE_2p5D = np.array(map(bunch.dE, xrange(bunch.getTotalCount())))
# for i in xrange(len(z)):
# 	fx.write(str(x[i]) + ', ' + str(y[i]) + ', ' + str(z[i]) + ', ' + str(xp_2p5D[i]) + ', ' + str(yp_2p5D[i]) + ', ' + str(dE_2p5D[i])+'\n')
# fx.close()
mean_xpRatio = np.mean(xp_2p5D[:N_mp]/xp_Analytical[:N_mp])
mean_ypRatio = np.mean(yp_2p5D[:N_mp]/yp_Analytical[:N_mp])
print "\naverage ratio of horizontal kicks (2p5d/analytical):", mean_xpRatio
print "average ratio of vertical kicks (2p5d/analytical):  ", mean_ypRatio


# fx = open('scSliceBySlice2D.txt', 'w')
reset_bunch_momenta(bunch)
sc_CalcSliceBySlice.trackBunch(bunch, integration_length)
xp_SliceBySlice2D = np.array(map(bunch.xp, xrange(bunch.getTotalCount())))
yp_SliceBySlice2D = np.array(map(bunch.yp, xrange(bunch.getTotalCount())))
dE_SliceBySlice2D = np.array(map(bunch.dE, xrange(bunch.getTotalCount())))
# for i in xrange(len(z)):
# 	fx.write(str(x[i]) + ', ' + str(y[i]) + ', ' + str(z[i]) + ', ' + str(xp_SliceBySlice2D[i]) + ', ' + str(yp_SliceBySlice2D[i]) + ', ' + str(dE_SliceBySlice2D[i])+'\n')
# fx.close()
mean_xpRatio = np.mean(xp_SliceBySlice2D[:N_mp]/xp_Analytical[:N_mp])
mean_ypRatio = np.mean(yp_SliceBySlice2D[:N_mp]/yp_Analytical[:N_mp])
print "\naverage ratio of horizontal kicks (SliceBySlice2D/analytical):", mean_xpRatio
print "average ratio of vertical kicks (SliceBySlice2D/analytical):  ", mean_ypRatio


# fx = open('sc3D.txt', 'w')
reset_bunch_momenta(bunch)
sc_3Dsolver.trackBunch(bunch, integration_length)
xp_3D = np.array(map(bunch.xp, xrange(bunch.getTotalCount())))
yp_3D = np.array(map(bunch.yp, xrange(bunch.getTotalCount())))
dE_3D = np.array(map(bunch.dE, xrange(bunch.getTotalCount())))
# for i in xrange(len(z)):
# 	fx.write(str(x[i]) + ', ' + str(y[i]) + ', ' + str(z[i]) + ', ' + str(xp_3D[i]) + ', ' + str(yp_3D[i]) + ', ' + str(dE_3D[i])+'\n')
# fx.close()
mean_xpRatio = np.mean(xp_3D[:N_mp]/xp_Analytical[:N_mp])
mean_ypRatio = np.mean(yp_3D[:N_mp]/yp_Analytical[:N_mp])
print "\naverage ratio of horizontal kicks (3D/analytical):", mean_xpRatio
print "average ratio of vertical kicks (3D/analytical):  ", mean_ypRatio


import scipy.io as sio
strt = N_mp
stop = len(x)
sio.savemat("output",{'x': x[strt:stop], 'y': y[strt:stop], 'z': z[strt:stop], 'xp_Analytical': xp_Analytical[strt:stop], 'yp_Analytical': yp_Analytical[strt:stop], \
			'xp_2p5D': xp_2p5D[strt:stop], 'yp_2p5D': yp_2p5D[strt:stop], 'xp_SliceBySlice2D': xp_SliceBySlice2D[strt:stop], 'yp_SliceBySlice2D': yp_SliceBySlice2D[strt:stop], \
			'xp_3D': xp_3D[strt:stop], 'yp_3D': yp_3D[strt:stop], 'N_mp_test_x': len(x_test), 'N_mp_test_y': len(y_test), 'N_mp_test_z': len(z_test)},oned_as='row')

