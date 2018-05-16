import os
import numpy as np
import scipy.io as sio
import pylab as plt
import glob
from SUSSIX.PySussix2 import *
from tune_diagram import resonance_lines
from mpl_toolkits.mplot3d import proj3d


ripple_Frequency = 1200
case = 'klse10602-0.08_Qripple%dHz_A2e-4_Q20.36_QDcompensated'%ripple_Frequency
# case = 'klse10602-0.02'
source_dir = 'Output_phasespace_%s/'%case

filename = 'mainbunch'
files = glob.glob(source_dir + filename + '*.mat')
files.sort()

x, xp = [], []
y, yp = [], []
z, dE = [], []
particleIDreference = sio.loadmat(files[0])['particles'][0][0]['ParticleIdNumber'].flatten()
for i, file in enumerate(files):
	print file
	if i != np.int(file.split('_')[-1].split('.')[0]):
		print 'ERROR: the files are not sorted or there are turns missing: ', i, ' is not ', np.int(file.split('_')[-1].split('.')[0])
		raise SystemExit
	particles = sio.loadmat(file)
	if np.array_equal(particles['particles'][0][0]['ParticleIdNumber'].flatten(), particleIDreference):
		x.append(particles['particles'][0][0]['x'].flatten())
		xp.append(particles['particles'][0][0]['xp'].flatten())
		y.append(particles['particles'][0][0]['y'].flatten())
		yp.append(particles['particles'][0][0]['yp'].flatten())
		z.append(particles['particles'][0][0]['z'].flatten())
		dE.append(particles['particles'][0][0]['dE'].flatten())
	else:
		print 'ERROR: some particles were lost. this cannot be handled yet ...'
		raise SystemExit


x = np.array(x)
xp = np.array(xp)
y = np.array(y)
yp = np.array(yp)
z = np.array(z)
dE = np.array(dE)

# find surviving particles
j = np.where(~np.isnan(np.sum(x, axis=0)))[0]

# calculate dispersion 
Dx = np.mean(x[:,j]*dE[:,j])/np.mean(dE[:,j]*dE[:,j])
Dpx = np.mean(xp[:,j]*dE[:,j])/np.mean(dE[:,j]*dE[:,j])
x -= Dx*dE
xp -= Dpx*dE

# SUSSIX analysis
Qx0 = 20.34
Qy0 = 20.15
turns_half = int(np.floor(len(x)/2))
tunes_x1, tunes_y1 = [], []
tunes_x2, tunes_y2 = [], []
SX = Sussix()
SX.sussix_inp(nt1=1, nt2=turns_half, idam=2, ir=0, tunex=Qx0%1.0 , tuney=Qy0%1.0, narm=10, istun = (1, 0.25, 0.25, 0.25))

for i in range(len(x.T)):
	SX.sussix(x[:turns_half,i], xp[:turns_half,i], y[:turns_half,i], yp[:turns_half,i], z[:turns_half,i], dE[:turns_half,i])
	tunes_x1.append(SX.ox)
	tunes_y1.append(SX.oy)	

	SX.sussix(x[turns_half:,i], xp[turns_half:,i], y[turns_half:,i], yp[turns_half:,i], z[turns_half:,i], dE[turns_half:,i])
	tunes_x2.append(SX.ox)
	tunes_y2.append(SX.oy)	

tunes_x1 = np.abs(np.array(tunes_x1))
tunes_y1 = np.abs(np.array(tunes_y1))
tunes_x2 = np.abs(np.array(tunes_x2))
tunes_y2 = np.abs(np.array(tunes_y2))
d = np.log(np.sqrt( (tunes_x2[:,0]-tunes_x1[:,0])**2 + (tunes_y2[:,0]-tunes_y1[:,0])**2 ))



lattice = sio.loadmat('lattice_params.mat', squeeze_me=True)
frev = 3e8/2200./np.pi

f, ax = plt.subplots(1, figsize=(5,5))
for i in xrange(-15,15):
	ax.axhline(1./3.+i*ripple_Frequency/frev/3., c='g', lw=0.5)
ax.axhline(1./3., c='r')
ax.plot(x[0,:], tunes_x1[:,0], 'k')
ax.set_xlabel('x0 [m]')
ax.set_ylabel('Qx')
ax.set_ylim(0.28,0.36)
plt.tight_layout()
plt.savefig('png/tune_vs_x_%s.png'%case, dpi=500)


si = 1
st = 0#x.shape[1]/2
f, ax = plt.subplots(1, figsize=(5,5))
ax.plot(x[::,st::si], lattice['betax0']*(xp[:,st::si]+lattice['alphax0']/lattice['betax0']*x[:,st::si]), '.', ms=1.0)
# ax.plot(x[:,::si], xp[:,::si], 'k.', ms=0.5)
ax.set_xlabel('x [m]')
ax.set_ylabel('px [m]')
ax.set_xlim(-0.022,0.022)
ax.set_ylim(-0.022,0.022)
plt.tight_layout()
plt.savefig('png/phasespace_%s.png'%case, dpi=500)

# for i in xrange(len(xp[0,:])):
# 	f, ax = plt.subplots(1, figsize=(5,5))
# 	ax.plot(x[:,i], lattice['betax0']*(xp[:,i]+lattice['alphax0']/lattice['betax0']*x[:,i]), '.', ms=1.0)
# 	ax.set_xlabel('x [m]')
# 	ax.set_ylabel('px [m]')
# 	ax.set_xlim(-0.022,0.022)
# 	ax.set_ylim(-0.022,0.022)
# 	plt.tight_layout()
# 	plt.savefig('png/phasespace_%s_particle%d.png'%(case,i), dpi=500)



plt.show()

