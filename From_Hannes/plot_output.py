import os
import numpy as np
import scipy.io as sio
import pylab as plt
import glob

plt.close('all')

filename = 'Output/output.mat'
data = sio.loadmat(filename, squeeze_me=True)

gamma = data['gamma']
beta = np.sqrt(1.-1./gamma**2)
C = 50*np.pi
c = 3e8
time = np.cumsum(C/(beta*c)) * 1e6

'''
f, ax = plt.subplots(1,figsize=(5,4))
ax.plot(data['turn'], 1e3*data['CO_x'], label='x')
ax.plot(data['turn'], 1e3*data['CO_y'], label='y')
ax.set_xlabel('turn')
ax.set_ylabel('CO (mm)')
ax.legend()
plt.tight_layout()

f, ax = plt.subplots(1,figsize=(5,4))
ax.plot(data['turn'], (data['gamma']-1)*938)
ax.set_xlabel('turn')
ax.set_ylabel('Ekin (MeV)')
plt.tight_layout()
'''

f, axs = plt.subplots(2,figsize=(6,6), sharex=True)
ax = axs[0]
# ax.plot(data['turn'], 1e6*data['epsn_x']/gamma/beta)
# ax.plot(data['turn'], 1e6*data['epsn_y']/gamma/beta)
# ax.set_ylabel('physical emittance (um)')
ax.plot(data['turn'], 1e6*data['epsn_x'], label='x')
ax.plot(data['turn'], 1e6*data['epsn_y'], label='y')
ax.plot(data['turn'], 1e6*(data['epsn_x']+data['epsn_y'])/2, label='(x+y)/2')
# ax.plot(time, 1e6*data['epsn_x'], label='x')
# ax.plot(time, 1e6*data['epsn_y'], label='y')
# ax.set_xlabel('time (us)')
ax.set_ylabel('normalized emittance (um)')
ax.legend()
ax = axs[1]
ax.plot(data['turn'], data['intensity'], 'k')
ax.set_xlabel('turn')
ax.set_ylabel('intensity')
plt.tight_layout()
plt.savefig('png/emittance_evolution.png', dpi=400)
plt.show()

