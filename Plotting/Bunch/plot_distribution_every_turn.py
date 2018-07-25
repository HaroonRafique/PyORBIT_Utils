# Plots the particle distributions in 5 phase spaces
# x-y x-xp y-yp xp-yp z-dE
# Comparing them at two turns

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import numpy as np
import scipy.io as sio 

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'large'
plt.rcParams['legend.handlelength'] = 5

plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['lines.markersize'] = 0.25

# Open File
file_0='mainbunch_-000001.mat'
file_1='mainbunch_000000.mat'
file_2='mainbunch_000001.mat'
file_3='mainbunch_000002.mat'
file_4='mainbunch_000003.mat'
file_5='mainbunch_000004.mat'
file_6='mainbunch_000005.mat'
file_7='mainbunch_000006.mat'
file_8='mainbunch_000007.mat'
file_9='mainbunch_000008.mat'
file_10='mainbunch_000009.mat'

particles_0=dict()
particles_1=dict()
particles_2=dict()
particles_3=dict()
particles_4=dict()
particles_5=dict()
particles_6=dict()
particles_7=dict()
particles_8=dict()
particles_9=dict()
particles_10=dict()

sio.loadmat(file_0, mdict=particles_0)
sio.loadmat(file_1, mdict=particles_1)
sio.loadmat(file_2, mdict=particles_2)
sio.loadmat(file_3, mdict=particles_3)
sio.loadmat(file_4, mdict=particles_4)
sio.loadmat(file_5, mdict=particles_5)
sio.loadmat(file_6, mdict=particles_6)
sio.loadmat(file_7, mdict=particles_7)
sio.loadmat(file_8, mdict=particles_8)
sio.loadmat(file_9, mdict=particles_9)
sio.loadmat(file_10, mdict=particles_10)

# ~ print particles_1p3['bunchparameters'].dtype.names
# ~ print dir(particles_1p3['bunchparameters'])
# ~ exit()
# ~ print particles_1p3['particles']['x'][0][0]
# ~ print np.asarray(particles_1p3['particles']['x'][0][0][0])
# ~ print np.squeeze(np.asarray(particles_1p3['particles']['x'][0][0][0]))

# Parameters
	# ~ x  = d['particles']['x'][()]
	# ~ xp = d['particles']['xp'][()]
	# ~ y  = d['particles']['y'][()]
	# ~ yp = d['particles']['yp'][()]
	# ~ z  = d['particles']['z'][()]
	# ~ dE = d['particles']['dE'][()]

#####################
#   x,y,xp,yp,z,dE  #
#####################

# ~ fig1=plt.figure(figsize=(6,10),constrained_layout=True)
fig, ax1 = plt.subplots()
# ~ fig1=plt.figure(figsize=(6,10))


ax1.scatter(particles_10['particles']['z'][0][0][0], particles_10['particles']['dE'][0][0][0], color='r', label='10');
ax1.scatter(particles_9['particles']['z'][0][0][0], particles_9['particles']['dE'][0][0][0], color='C1', label='9');
ax1.scatter(particles_8['particles']['z'][0][0][0], particles_8['particles']['dE'][0][0][0], color='C2', label='8');
ax1.scatter(particles_7['particles']['z'][0][0][0], particles_7['particles']['dE'][0][0][0], color='C3', label='7');
ax1.scatter(particles_6['particles']['z'][0][0][0], particles_6['particles']['dE'][0][0][0], color='C4', label='6');
ax1.scatter(particles_5['particles']['z'][0][0][0], particles_5['particles']['dE'][0][0][0], color='C5', label='5');
ax1.scatter(particles_4['particles']['z'][0][0][0], particles_4['particles']['dE'][0][0][0], color='C6', label='4');
ax1.scatter(particles_3['particles']['z'][0][0][0], particles_3['particles']['dE'][0][0][0], color='C7', label='3');
ax1.scatter(particles_2['particles']['z'][0][0][0], particles_2['particles']['dE'][0][0][0], color='C8', label='2');
ax1.scatter(particles_1['particles']['z'][0][0][0], particles_1['particles']['dE'][0][0][0], color='C9', label='1');
ax1.scatter(particles_0['particles']['z'][0][0][0], particles_0['particles']['dE'][0][0][0], color='k', label='0');

ax1.set_xlabel('z [m]');
ax1.set_ylabel('dE [GeV]');
ax1.set_title('Particle Distribution: Longitudinal');
ax1.grid(True);
ax1.legend();

fig.savefig('Filamentation_SC.png');
