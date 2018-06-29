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
file_in='mainbunch_000000.mat'
file_out='mainbunch_001499.mat'

particles_in=dict()
particles_out=dict()

sio.loadmat(file_in, mdict=particles_in)
sio.loadmat(file_out, mdict=particles_out)

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
fig1=plt.figure(figsize=(6,10))
ax1 = fig1.add_subplot(321) 
ax2 = fig1.add_subplot(322)
ax3 = fig1.add_subplot(323) 
ax4 = fig1.add_subplot(324)
ax5 = fig1.add_subplot(325) 
ax6 = fig1.add_subplot(326)

# ~ fig2.subplots_adjust(wspace=width between plots, hspace=height between plots, left=margin, right=margin, top=margin, bottom=margin)
# ~ fig2.subplots_adjust(wspace=0.1, hspace=0.3, left=0.15, right=0.99, top=0.95, bottom=0.1)
fig1.subplots_adjust(wspace=0.3, hspace=0.3, left=0.1, right=0.99, top=0.95, bottom=0.05)
#fig.tight_layout()                            

ax1.scatter(particles_out['particles']['x'][0][0][0], particles_out['particles']['y'][0][0][0], color='b', label='1.6 eVs');
ax1.scatter(particles_in['particles']['x'][0][0][0], particles_in['particles']['y'][0][0][0], color='g', label='1.3 eVs');

# ~ ax1.legend();
ax1.set_xlabel('x [m]');
ax1.set_ylabel('y [m]');
ax1.set_title('Particle Distribution: Real space');
ax1.grid(True);

ax2.scatter(particles_out['particles']['xp'][0][0][0], particles_out['particles']['yp'][0][0][0], color='b', label='1.6 eVs');
ax2.scatter(particles_in['particles']['xp'][0][0][0], particles_in['particles']['yp'][0][0][0], color='g', label='1.3 eVs');

ax2.set_xlabel('xp []');
ax2.set_ylabel('yp []');
ax2.set_title('Particle Distribution: xp yp');
ax2.grid(True);

ax3.scatter(particles_out['particles']['x'][0][0][0], particles_out['particles']['xp'][0][0][0], color='b', label='1.6 eVs');
ax3.scatter(particles_in['particles']['x'][0][0][0], particles_in['particles']['xp'][0][0][0], color='g', label='1.3 eVs');

ax3.set_xlabel('x [m]');
ax3.set_ylabel('xp []');
ax3.set_title('Particle Distribution: Horizontal phase space');
ax3.grid(True);

ax4.scatter(particles_out['particles']['y'][0][0][0], particles_out['particles']['yp'][0][0][0], color='b', label='1.6 eVs');
ax4.scatter(particles_in['particles']['y'][0][0][0], particles_in['particles']['yp'][0][0][0], color='g', label='1.3 eVs');

ax4.set_xlabel('y [m]');
ax4.set_ylabel('yp []');
ax4.set_title('Particle Distribution: Vertical phase space');
ax4.grid(True);


ax5.scatter(particles_out['particles']['z'][0][0][0], particles_out['particles']['dE'][0][0][0], color='b', label='1.6 eVs');
ax5.scatter(particles_in['particles']['z'][0][0][0], particles_in['particles']['dE'][0][0][0], color='g', label='1.3 eVs');

ax5.set_xlabel('z [m]');
ax5.set_ylabel('dE [GeV]');
ax5.set_title('Particle Distribution: Longitudinal');
ax5.grid(True);

ax6.scatter(0,0,color='b', label='In')
ax6.scatter(0,0,color='g', label='Out')

legend_elements = [Line2D([0], [0], marker='o', color='w', label='In', markerfacecolor='b', markersize=15),
                   Line2D([0], [0], marker='o', color='w', label='Out', markerfacecolor='g', markersize=15)]

ax6.legend(handles=legend_elements, loc='center')


# ~ plt.show();
# ~ fig1.savefig('Emittance_y.png', transparent=True);
fig1.savefig('Distribution_Turn_0_1500_4p5sig_Multipole_0p2_Matched.png');
