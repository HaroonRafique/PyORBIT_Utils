import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
import glob
import os

path = 'output/'
fontsize = 14

# load the output dictionary
output_dict = scipy.io.loadmat(path + 'output.mat')

# Variables to plot
meany = output_dict['mean_y'].flatten()
gamma = output_dict['gamma'].flatten()
emitNy = output_dict['epsn_y'].flatten()
emity = output_dict['eps_y'].flatten()
emitz = output_dict['eps_z'].flatten()
sigma = output_dict['bunchlength'].flatten()
intens = output_dict['intensity'].flatten()

#Plot
fig = plt.figure(figsize=(13,13))
ax1 = fig.add_subplot(711)
ax2 = fig.add_subplot(712, sharex=ax1)
ax3 = fig.add_subplot(713, sharex=ax1)
ax4 = fig.add_subplot(714, sharex=ax1)
ax5 = fig.add_subplot(715, sharex=ax1)
ax6 = fig.add_subplot(716, sharex=ax1)
ax7 = fig.add_subplot(717, sharex=ax1)

ax1.plot(gamma,'k')
ax2.plot(meany,'r')
ax3.plot(emitNy,'b')
ax4.plot(emity,'b--')
ax5.plot(intens,'c--')
ax6.plot(emitz,'g')
ax7.plot(sigma,'m')

#ax1.set_xlim(0.)
ax1.set_ylabel('$\gamma$', fontsize=fontsize)
ax2.set_ylabel('<y> (m)', fontsize=fontsize)
ax3.set_ylabel('$\epsilon_{y,N}$', fontsize=fontsize)
ax4.set_ylabel('$\epsilon_y$ (m.rad)',fontsize=fontsize)
ax5.set_ylabel('Intensity',fontsize=fontsize)
ax6.set_ylabel('$\epsilon_z (m.rad)$',fontsize=fontsize)
ax7.set_ylabel('$\sigma_z$ (m)',fontsize=fontsize)
ax7.set_xlabel('Turns', fontsize=fontsize)
plt.subplots_adjust(hspace=0.5)
plt.savefig('yplots.png')

'''
#zoom
fig2 = plt.figure(figsize=(13,13))
ax1 = fig2.add_subplot(711)
ax2 = fig2.add_subplot(712, sharex=ax1)
ax3 = fig2.add_subplot(713, sharex=ax1)
ax4 = fig2.add_subplot(714, sharex=ax1)
ax5 = fig2.add_subplot(715, sharex=ax1)
ax6 = fig2.add_subplot(716, sharex=ax1)
ax7 = fig2.add_subplot(717, sharex=ax1)

ax1.plot(gamma,'k')
ax2.plot(meany,'r')
ax3.plot(emitNy,'b')
ax4.plot(emity,'b--')
ax5.plot(intens,'c')
ax6.plot(emitz,'g')
ax7.plot(sigma,'m')

#ax1.set_xlim(0.)
ax1.set_ylabel('$\gamma$', fontsize=fontsize)
ax2.set_ylabel('<y>', fontsize=fontsize)
ax2.set_ylim(-0.00025, 0.00025)
ax3.set_ylabel('$\epsilon_{y,N}$', fontsize=fontsize)
ax3.set_ylim(0.000008, 0.0000098)
ax4.set_ylabel('$\epsilon_y$ (m.rad)',fontsize=fontsize)
ax4.set_ylim(0.000013, 0.0000155)
ax5.set_ylabel('Intensity',fontsize=fontsize)
ax5.set_ylim(1.3e13, 1.605e13)
ax6.set_ylabel('$\epsilon_z$ (m.rad)',fontsize=fontsize)
ax6.set_ylim(1.05, 1.45)
ax7.set_ylabel('$\sigma_z$ (m)',fontsize=fontsize)
#ax7.set_ylim(0.0000012, 0.0000013)
ax7.set_xlabel('Turns', fontsize=fontsize)

plt.subplots_adjust(hspace=0.5)
#plt.savefig('yplots_wSC_zoom.png')
'''
# Variables to plot

meanx = output_dict['mean_x'].flatten()
emitNx = output_dict['epsn_x'].flatten()
emitx = output_dict['eps_x'].flatten()

fig3 = plt.figure(figsize=(13,13))
ax1 = fig3.add_subplot(511)
ax2 = fig3.add_subplot(512, sharex=ax1)
ax3 = fig3.add_subplot(513, sharex=ax1)
ax4 = fig3.add_subplot(514, sharex=ax1)
ax5 = fig3.add_subplot(515, sharex=ax1)

ax1.plot(gamma,'k')
ax2.plot(meanx,'r')
ax3.plot(emitNx,'b')
ax4.plot(emitx,'b--')
ax5.plot(intens,'c')

ax1.set_ylabel('$\gamma$', fontsize=fontsize)
ax2.set_ylabel('<x> (m)', fontsize=fontsize)
#ax2.set_xlim(0, 150)
ax3.set_ylabel('$\epsilon_{x,N}$', fontsize=fontsize)
#ax3.set_ylim(0.0000130, 0.0000150)
ax4.set_ylabel('$\epsilon_x$ (m.rad)', fontsize=fontsize)
#ax4.set_ylim(0.000020, 0.000024)
ax5.set_ylabel('Intensity', fontsize=fontsize)
ax5.set_ylim(1.55e13, 1.605e13)
ax5.set_xlabel('Turns', fontsize=fontsize)

plt.subplots_adjust(hspace=0.5)
plt.savefig('xplots.png')

#Phasespace
fig4 = plt.figure(figsize=(10,8))
txtfile = np.loadtxt('output/mainbunch_004099', skiprows=17, usecols=(0,1,2,3,4,5))
x = txtfile[:,0]
xp = txtfile[:,1]
y = txtfile[:,2]
yp = txtfile[:,3]
z = txtfile[:,4]
pz = txtfile[:,5]

# Plot
ax1 = fig4.add_subplot(311)
ax2 = fig4.add_subplot(312)
ax3 = fig4.add_subplot(313)
ax1.plot(x, xp,'b.')
ax2.plot(y, yp,'b.')
ax3.plot(z, pz,'b.')

ax1.set_title('After tracking 4099 turns')
ax1.set_ylabel("x' (rad)", fontsize=12)
ax1.set_xlabel('x (m)', fontsize=12)
ax2.set_ylabel("y' (rad)", fontsize=12)
ax2.set_xlabel('y (m)', fontsize=12)
ax3.set_ylabel('dE (GeV)', fontsize=12)
ax3.set_xlabel('z (m)', fontsize=12)
plt.subplots_adjust(hspace=0.4)
plt.savefig('phasespace_after4099turns.png')
#plt.show()





























