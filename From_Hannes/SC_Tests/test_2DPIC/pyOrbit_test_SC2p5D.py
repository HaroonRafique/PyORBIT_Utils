import numpy as np
import math

from bunch import Bunch
from bunch import BunchTwissAnalysis
from spacecharge import SpaceChargeCalc2p5D, Boundary2D

# KV distribution
def generateParticle_KV(x_max, xp_max, y_max, yp_max):
	d = 4
	u = np.random.normal(size=d)
	r = np.sqrt(np.sum(u**2))
	u *= 1./r
	
	x  = u[0]*x_max
	xp = u[1]*xp_max
	y  = u[2]*y_max
	yp = u[3]*yp_max
	return  x, xp, y, yp

b = Bunch()
b.mass(0.93827231)
energy = 1.0 #Gev
b.getSyncParticle().kinEnergy(energy)
intensity = 1e10
N_mp = 400000
macrosize = intensity/N_mp
# b.macroSize(macrosize)
b.addPartAttr("macrosize")
x_max  = 1.5
xp_max = 1
y_max  = 1.5
yp_max = 1
# we set the initial xp and yp zero to determine the SC kicks afterwards
for i in xrange(N_mp):
	x, xp, y, yp = generateParticle_KV(x_max, xp_max, y_max, yp_max)
	b.addParticle(x, 0*xp, y, 0*yp, np.random.normal(0), np.random.normal(0))
	b.partAttrValue("macrosize", i, 0, macrosize)  #main bunch has finite macrosize for space charge
b.addParticle( 2*x_max, 0,  2*y_max, 0, np.random.normal(0), np.random.normal(0))
b.addParticle(-2*x_max, 0, -2*y_max, 0, np.random.normal(0), np.random.normal(0))


sizeX = 256/2
sizeY = 256
nBinsZ = 1 
sc_calc = SpaceChargeCalc2p5D(sizeX, sizeY, nBinsZ)

'''
# Make a predefined Boundary
bpoints = 12
bmodes = 1#0
pipe_diameter = 3.
boundary = Boundary2D(bpoints, bmodes, "Rectangle", pipe_diameter, pipe_diameter)
for i in xrange(bpoints):
	print boundary.getBoundaryPointX(), boundary.getBoundaryPointY()
'''
""
'''
# Make an arbitrary boundary ###################################
nBoundaryPoints = 499
bmodes = 20
boundary = Boundary2D(nBoundaryPoints,bmodes)
'''
'''
# circle
R_Boundary = 3.
for i in xrange(nBoundaryPoints):
	x = R_Boundary*math.cos((2.0*math.pi/(nBoundaryPoints-1))*i)
	y = R_Boundary*math.sin((2.0*math.pi/(nBoundaryPoints-1))*i)
	boundary.setBoundaryPoint(i,x,y)
'''
'''
# rectangle
x_Boundary = []
y_Boundary = []
xlim = (-3., 3.)
ylim = (-2., 2.)
for i in xrange(nBoundaryPoints/4):
	x = xlim[0]
	y = np.linspace(ylim[0], ylim[1], int(nBoundaryPoints/4)+1)[i]
	x_Boundary.append(x)
	y_Boundary.append(y)
for i in xrange(nBoundaryPoints/4):
	x = np.linspace(xlim[0], xlim[1], int(nBoundaryPoints/4)+1)[i]
	y = ylim[1]
	x_Boundary.append(x)
	y_Boundary.append(y)
for i in xrange(nBoundaryPoints/4):
	x = xlim[1]
	y = np.linspace(ylim[1], ylim[0], int(nBoundaryPoints/4)+1)[i]
	x_Boundary.append(x)
	y_Boundary.append(y)
for i in xrange(nBoundaryPoints - 3*int(nBoundaryPoints/4)):
	x = np.linspace(xlim[1], xlim[0], nBoundaryPoints - 3*int(nBoundaryPoints/4)+1)[i]
	y = ylim[0]
	x_Boundary.append(x)
	y_Boundary.append(y)
for i in xrange(len(x_Boundary)):
	boundary.setBoundaryPoint(i,x_Boundary[i],y_Boundary[i])
# 	print x_Boundary[i], y_Boundary[i]
""
	
boundary.initialize()
b_maxx = boundary.getMaxX()
b_minx = boundary.getMinX()
b_maxy = boundary.getMaxY()
b_miny = boundary.getMinY()
print "MaxX=",b_maxx," MinX=",b_minx," MaxY=",b_maxy," MinY=",b_miny
'''
integration_length = 1.0
sc_calc.trackBunch(b, integration_length)
# sc_calc.trackBunch(b, integration_length, boundary)

phiGrid = sc_calc.getPhiGrid()
for j in xrange(1):
	phi_grid = np.zeros((sizeX, sizeY))
	Ex_grid = np.zeros((sizeX, sizeY))
	Ey_grid = np.zeros((sizeX, sizeY))
	x_grid = np.zeros((sizeX, sizeY))
	y_grid = np.zeros((sizeX, sizeY))	
	for ix in xrange(sizeX):
		for iy in xrange(sizeY): 
			phi_grid[ix, iy] = phiGrid.getValueOnGrid(ix, iy)
			x_grid[ix, iy] = phiGrid.getGridX(ix)
			y_grid[ix, iy] = phiGrid.getGridY(iy)					
			Ex_grid[ix, iy], Ey_grid[ix, iy] = phiGrid.calcGradient(x_grid[ix, iy], y_grid[ix, iy])
			Ex_grid[ix, iy] *= -1
			Ey_grid[ix, iy] *= -1
import scipy.io as sio
sio.savemat("Phi_grid",{'phi_grid': phi_grid, 'Ex_grid': Ex_grid, 'Ey_grid': Ey_grid, 'x_grid': x_grid, 'y_grid': y_grid},oned_as='row')

twissAnalysis = BunchTwissAnalysis()
twissAnalysis.analyzeBunch(b)
print 'Intensity:', twissAnalysis.getGlobalMacrosize()
# remove the test particles
print b.getSize()
b.deleteParticle(b.getSize()-1)
b.deleteParticle(b.getSize()-1)
print b.getSize()

x = map(lambda i: b.x(i), xrange(b.getSize()))
xp = map(lambda i: b.xp(i), xrange(b.getSize()))
y = map(lambda i: b.y(i), xrange(b.getSize()))
yp = map(lambda i: b.yp(i), xrange(b.getSize()))
slope_numerical_x = np.polyfit(x, xp, 1)[0]
slope_numerical_y = np.polyfit(y, yp, 1)[0]
print 'Numerical slope xp(x): ', slope_numerical_x
print 'Numerical slope yp(y): ', slope_numerical_y

# analytical calculation for a uniform transverse distribution (will be correct in case of coasting beam, i.e. nBinsZ=1)
from orbit_utils import BunchExtremaCalculator
bunch_extrema_cal = BunchExtremaCalculator()
z_min, z_max = bunch_extrema_cal.extremaZ(b)
# print 'z_min, z_max:', z_min, z_max
linedensity = twissAnalysis.getGlobalMacrosize() / (z_max - z_min)
r0 = 1.534698e-18
ax = x_max
ay = y_max
gamma = b.getSyncParticle().gamma()
beta = b.getSyncParticle().beta()
slope_theory_x = 4*r0*linedensity/(ax*(ax+ay) * beta**2 * gamma**3) * integration_length
slope_theory_y = 4*r0*linedensity/(ay*(ax+ay) * beta**2 * gamma**3) * integration_length
print 'Theoretical slope xp(x):', slope_theory_x
print 'Theoretical slope yp(y):', slope_theory_y
print 'Ratio_x:', slope_numerical_x/slope_theory_x
print 'Ratio_y:', slope_numerical_y/slope_theory_y

sio.savemat("kicks",{'x': x[::10], 'xp': xp[::10], 'y': y[::10], 'yp': yp[::10], 'slope_theory_x': slope_theory_x, 'slope_theory_y': slope_theory_y},oned_as='row')

# b.dumpBunch('bunch_out.txt')
