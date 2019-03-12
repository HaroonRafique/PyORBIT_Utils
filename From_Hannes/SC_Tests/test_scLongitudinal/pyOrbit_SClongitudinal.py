from math import sqrt
import numpy as np

from bunch import Bunch, BunchTwissAnalysis
from orbit.utils.consts import mass_proton, pi
from orbit.bunch_generators import TwissContainer
from orbit.bunch_generators import WaterBagDist1D, GaussDist1D, KVDist1D
from orbit.bunch_generators import WaterBagDist2D, GaussDist2D, KVDist2D
from orbit.injection import UniformLongDist
from orbit.injection import JohoTransverse, JohoLongitudinal

from spacecharge import LSpaceChargeCalc
from orbit.space_charge.sc1d import SC1D_AccNode
from spacecharge import SpaceChargeCalcSliceBySlice2D
from spacecharge import SpaceChargeCalc2p5Drb, Boundary2D

#===== Generate Bunch ============

b = Bunch()
b.mass(mass_proton)
b.macroSize(1.0e+5)
energy = 26 #Gev
b.getSyncParticle().kinEnergy(energy)

print '  Momentum: ', b.getSyncParticle().momentum(), 'GeV'
print '  Ekin:     ', b.getSyncParticle().kinEnergy(), 'GeV'
print '  Gamma:    ', b.getSyncParticle().gamma() 
print '  Beta:     ', b.getSyncParticle().beta()
''
#---------------------------------------------
# KV 2D  
#---------------------------------------------
twissX = TwissContainer(alpha = 0., beta = 1., emittance = 0.0025)
twissY = TwissContainer(alpha = 0., beta = 1., emittance = 0.0025)
dist2D = KVDist2D(twissX,twissY)
''
'''
#---------------------------------------------
# WaterBag 2D
#---------------------------------------------
twissX = TwissContainer(alpha = 0., beta = 1., emittance = 0.0025)
twissY = TwissContainer(alpha = 0., beta = 1., emittance = 0.0025)
dist2D = WaterBagDist2D(twissX,twissY)
'''
'''
#---------------------------------------------
# Gauss 2D
#---------------------------------------------
twissX = TwissContainer(alpha = 0., beta = 1., emittance = 0.0025)
twissY = TwissContainer(alpha = 0., beta = 1., emittance = 0.0025)
dist2D = GaussDist2D(twissX,twissY)
'''

# order = 0.5
# alphax = 0
# betax = 1
# alphay = 0
# betay = 1
# emitlim = 4 * 2*(order + 1) * 1e-4
# xcenterpos = 0.0
# xcentermom = 0.0
# ycenterpos = 0.0
# ycentermom = 0.0
# tailfrac = 0.0
# taillim = 0.0
# 
# xFunc = JohoTransverse(order, alphax, betax, emitlim, xcenterpos, xcentermom, tailfrac, taillim)
# yFunc = JohoTransverse(order, alphay, betay, emitlim, ycenterpos, ycentermom, tailfrac, taillim)      
# 
# class dist2D():
# 	def __init__(self,xFunc, yFunc):
# 		self.xFunc = xFunc
# 		self.yFunc = yFunc
# 	def getCoordinates(self):
# 		x, xp = self.xFunc.getCoordinates()
# 		y, yp = self.yFunc.getCoordinates()
# 		return x, xp, y, yp
# dist2D = dist2D(xFunc, yFunc)

'''
#---------------------------------------------
# Coasting beam 
#---------------------------------------------
zlim = 0.5
zmin = -zlim
zmax = zlim
deltaEfrac = 0.001
eoffset = 0.0
sp = b.getSyncParticle()
dist1D = UniformLongDist(zmin, zmax, sp, eoffset, deltaEfrac)
'''

#---------------------------------------------
# KV 1D  
#---------------------------------------------
# twissZ = TwissContainer(alpha = 0., beta = 1., emittance = 0.5)
# dist1D = KVDist1D(twissZ)

#---------------------------------------------
# Joho 1D  
#---------------------------------------------
order = 10#5 #2
zlim = 0.5
dElim = 0.001
nlongbunches = 1
deltazbunch = 0
deltaznotch = 0.
ltailfrac = 0
ltailfac = 0
dist1D = JohoLongitudinal(order, zlim, dElim, nlongbunches, deltazbunch, deltaznotch, ltailfrac, ltailfac)


#---------------------------------------------
# Generate bunch particles
#---------------------------------------------
N_mp = 2000000 #2000000
for i in range(N_mp):
	(x,xp,y,yp) = dist2D.getCoordinates()
	(z, dE) = dist1D.getCoordinates()
	b.addParticle(x,xp,y,yp,z,dE)

TwissAnalysis = BunchTwissAnalysis()
TwissAnalysis.analyzeBunch(b)
sigma_x = sqrt(TwissAnalysis.getCorrelation(0,0))
sigma_y = sqrt(TwissAnalysis.getCorrelation(2,2))
sigma_z = sqrt(TwissAnalysis.getCorrelation(4,4))

print '\n  sigma_x=', sigma_x
print '  sigma_y=', sigma_y
print '  sigma_z=', sigma_z


#---------------------------------------------
# setup of SC calculators
#---------------------------------------------
pipe_radius = 0.3
a = 0.1
b_a = pipe_radius/a
bpoints = 128
bmodes = 10
boundary = Boundary2D(bpoints, bmodes, "Ellipse", 2*pipe_radius, 2*pipe_radius)
length = 1.
nMacrosMin = 10
useSpaceCharge = 1
nBins = 32 #128     #number of longitudinal slices in the 1D space charge solver
sizeX = 64
sizeY = 64
sc1Dnode = SC1D_AccNode(b_a,length, nMacrosMin,useSpaceCharge,nBins)

sc2p5Drb = SpaceChargeCalc2p5Drb(sizeX, sizeY, nBins)

scSliceBySlice = SpaceChargeCalcSliceBySlice2D(sizeX,sizeY,nBins)


def reset_bunch_momenta(bunch):
	for i in xrange(bunch.getSize()):
		bunch.xp(i, 0)
		bunch.yp(i, 0)
		bunch.dE(i, 0)
x = np.array(map(b.x, xrange(b.getTotalCount())))
y = np.array(map(b.y, xrange(b.getTotalCount())))
z = np.array(map(b.z, xrange(b.getTotalCount())))

reset_bunch_momenta(b)
sc1Dnode.trackBunch(b)
sc_kick_1D = np.array(map(b.dE, xrange(b.getTotalCount())))
# fz = open('sc1D.txt', 'w')
# for i in xrange(len(z)):
#	fz.write(str(z[i]) + ', ' + str(sc_kick_1D[i])+'\n')
# fz.close()

reset_bunch_momenta(b)
sc2p5Drb.trackBunch(b, length, pipe_radius)
sc_kick_2p5Drb = np.array(map(b.dE, xrange(b.getTotalCount())))
# fz = open('sc2p5Drb.txt', 'w')
# for i in xrange(len(z)):
#	fz.write(str(z[i]) + ', ' + str(sc_kick_2p5Drb[i])+'\n')
# fz.close()

################################
# f2 = open('test.txt', 'w')
# gridValue = map(sc2p5Drb.getLongDerivativeGrid().getValueOnGrid, range(nBins))
# gridPosition = map(sc2p5Drb.getLongDerivativeGrid().getGridZ, range(nBins))
# for i in xrange(len(gridValue)):
# 	f2.write(str(gridPosition[i]) + ', ' + str(gridValue[i])+'\n')
# f2.write('\n')
# f2.close()
################################
# LongDerivativeGrid = sc2p5Drb.getLongDerivativeGrid()
# ftest = open('test.txt', 'w')
# for i in xrange(len(z)):
# 	ftest.write(str(z[i]) + ', ' + str(LongDerivativeGrid.getValueSmoothed(z[i])) + '\n')
# ftest.close()

reset_bunch_momenta(b)
# scSliceBySlice.trackBunch(b, length)
scSliceBySlice.trackBunch(b, length, boundary)
sc_kick_SliceBySlice = np.array(map(b.dE, xrange(b.getTotalCount())))
# fz = open('scSliceBySlice.txt', 'w')
# for i in xrange(len(z)):
#	fz.write(str(z[i]) + ', ' + str(sc_kick_SliceBySlice[i])+'\n')
# fz.close()


# theoretical calculation
LongitudinalGrid = sc2p5Drb.getLongGrid()
linedensity_derivative_arr = []
z_min = LongitudinalGrid.getMinZ()
z_max = LongitudinalGrid.getMaxZ()
z_test = np.linspace(z_min, z_max, 1000)
for z_i in z_test:
	linedensity_derivative_arr.append(LongitudinalGrid.calcGradientSmoothed(z_i)/LongitudinalGrid.getStepZ())

g = np.log(b_a) + 0.5
r0 = 1.534698e-18
gamma = b.getSyncParticle().gamma()
beta = b.getSyncParticle().beta()
momentum = b.getSyncParticle().momentum()
sc_kick_theory = - length * 2*r0 * mass_proton * g * np.array(linedensity_derivative_arr) / gamma**2
# fz = open('scTheory.txt', 'w')
# for i in xrange(len(z_test)):
#	fz.write(str(z_test[i]) + ', ' + str(sc_kick_theory[i])+'\n')
# fz.close()

# print sc_kick_theory

import scipy.io as sio
strt = 0
stop = N_mp #len(z)
sio.savemat("output",{'x': x[strt:stop], 'y': y[strt:stop], 'z': z[strt:stop], 'sc_kick_1D': sc_kick_1D, 'sc_kick_2p5Drb': sc_kick_2p5Drb, \
			'sc_kick_SliceBySlice': sc_kick_SliceBySlice, 'z_test': z_test, 'sc_kick_theory': sc_kick_theory},oned_as='row')

