# Plots the particle distributions in 5 phase spaces
# x-y x-xp y-yp xp-yp z-dE
# For the PS_Injection studies at different long. emittances

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
input_file='mainbunch_000099.mat'

turn_buff = input_file.replace('.','_')
print turn_buff
turn = int(turn_buff.split('_')[1])
print turn

d=dict()

a = sio.loadmat(input_file, mdict=d, squeeze_me=True)
b = d['particles'].flatten()[0]

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
	# ~ xphase = d['particles'][0][0]['ParticlePhaseAttributes'][2][0] - first xphase
	# ~ yphase = d['particles'][0][0]['ParticlePhaseAttributes'][3] - all yphases
# ~ print d['particles'][0][0]['ParticlePhaseAttributes']

#####################
#   x,y,xp,yp,z,dE  #
#####################

# ~ fig1=plt.figure(figsize=(6,10),constrained_layout=True)
# ~ fig1=plt.figure(figsize=(6,10))
fig1, ax1 = plt.subplots();
# ~ ax1 = fig1.add_subplot(321) 
# ~ ax2 = fig1.add_subplot(322)
# ~ ax3 = fig1.add_subplot(323) 
# ~ ax4 = fig1.add_subplot(324)
# ~ ax5 = fig1.add_subplot(325) 
# ~ ax6 = fig1.add_subplot(326)

# ~ fig2.subplots_adjust(wspace=width between plots, hspace=height between plots, left=margin, right=margin, top=margin, bottom=margin)
# ~ fig2.subplots_adjust(wspace=0.1, hspace=0.3, left=0.15, right=0.99, top=0.95, bottom=0.1)
fig1.subplots_adjust(wspace=0.3, hspace=0.3, left=0.1, right=0.99, top=0.95, bottom=0.05)
#fig.tight_layout()                            

ax1.scatter(b['ParticlePhaseAttributes'][2,:], b['ParticlePhaseAttributes'][3,:], color='g', label='1.3 eVs');

# ~ ax1.legend();
ax1.set_xlabel('Phase_x [-]');
ax1.set_ylabel('Pase_y [-]');
ax1.set_title('Phase Footprint');
ax1.grid(True);

output_filename = 'Tune_Footprint_turn=' + str(turn) + '.png'

fig1.savefig(output_filename);
