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
file_1p3='1.3.mainbunch_000999.mat'
file_1p6='1.6.mainbunch_000999.mat'
file_1p9='1.9.mainbunch_000999.mat'
file_2p3='2.3.mainbunch_000999.mat'
file_2p6='2.6.mainbunch_000999.mat'

particles_1p3=dict()
particles_1p6=dict()
particles_1p9=dict()
particles_2p3=dict()
particles_2p6=dict()

sio.loadmat(file_1p3, mdict=particles_1p3)
sio.loadmat(file_1p6, mdict=particles_1p6)
sio.loadmat(file_1p9, mdict=particles_1p9)
sio.loadmat(file_2p3, mdict=particles_2p3)
sio.loadmat(file_2p6, mdict=particles_2p6)

print particles_1p3['bunchparameters'].dtype.names
# ~ print dir(particles_1p3['bunchparameters'])
exit()
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

ax1.scatter(particles_2p6['particles']['x'][0][0][0], particles_2p6['particles']['y'][0][0][0], color='m', label='2.6 eVs');
ax1.scatter(particles_2p3['particles']['x'][0][0][0], particles_2p3['particles']['y'][0][0][0], color='k', label='2.3 eVs');
ax1.scatter(particles_1p9['particles']['x'][0][0][0], particles_1p9['particles']['y'][0][0][0], color='c', label='1.9 eVs');
ax1.scatter(particles_1p6['particles']['x'][0][0][0], particles_1p6['particles']['y'][0][0][0], color='b', label='1.6 eVs');
ax1.scatter(particles_1p3['particles']['x'][0][0][0], particles_1p3['particles']['y'][0][0][0], color='g', label='1.3 eVs');

# ~ ax1.legend();
ax1.set_xlabel('x [m]');
ax1.set_ylabel('y [m]');
ax1.set_title('Particle Distribution: Real space');
ax1.grid(True);

ax2.scatter(particles_2p6['particles']['xp'][0][0][0], particles_2p6['particles']['yp'][0][0][0], color='m', label='2.6 eVs');
ax2.scatter(particles_2p3['particles']['xp'][0][0][0], particles_2p3['particles']['yp'][0][0][0], color='k', label='2.3 eVs');
ax2.scatter(particles_1p9['particles']['xp'][0][0][0], particles_1p9['particles']['yp'][0][0][0], color='c', label='1.9 eVs');
ax2.scatter(particles_1p6['particles']['xp'][0][0][0], particles_1p6['particles']['yp'][0][0][0], color='b', label='1.6 eVs');
ax2.scatter(particles_1p3['particles']['xp'][0][0][0], particles_1p3['particles']['yp'][0][0][0], color='g', label='1.3 eVs');

ax2.set_xlabel('xp []');
ax2.set_ylabel('yp []');
ax2.set_title('Particle Distribution: xp yp');
ax2.grid(True);

ax3.scatter(particles_2p6['particles']['x'][0][0][0], particles_2p6['particles']['xp'][0][0][0], color='m', label='2.6 eVs');
ax3.scatter(particles_2p3['particles']['x'][0][0][0], particles_2p3['particles']['xp'][0][0][0], color='k', label='2.3 eVs');
ax3.scatter(particles_1p9['particles']['x'][0][0][0], particles_1p9['particles']['xp'][0][0][0], color='c', label='1.9 eVs');
ax3.scatter(particles_1p6['particles']['x'][0][0][0], particles_1p6['particles']['xp'][0][0][0], color='b', label='1.6 eVs');
ax3.scatter(particles_1p3['particles']['x'][0][0][0], particles_1p3['particles']['xp'][0][0][0], color='g', label='1.3 eVs');

ax3.set_xlabel('x [m]');
ax3.set_ylabel('xp []');
ax3.set_title('Particle Distribution: Horizontal phase space');
ax3.grid(True);

ax4.scatter(particles_2p6['particles']['y'][0][0][0], particles_2p6['particles']['yp'][0][0][0], color='m', label='2.6 eVs');
ax4.scatter(particles_2p3['particles']['y'][0][0][0], particles_2p3['particles']['yp'][0][0][0], color='k', label='2.3 eVs');
ax4.scatter(particles_1p9['particles']['y'][0][0][0], particles_1p9['particles']['yp'][0][0][0], color='c', label='1.9 eVs');
ax4.scatter(particles_1p6['particles']['y'][0][0][0], particles_1p6['particles']['yp'][0][0][0], color='b', label='1.6 eVs');
ax4.scatter(particles_1p3['particles']['y'][0][0][0], particles_1p3['particles']['yp'][0][0][0], color='g', label='1.3 eVs');

ax4.set_xlabel('y [m]');
ax4.set_ylabel('yp []');
ax4.set_title('Particle Distribution: Vertical phase space');
ax4.grid(True);


ax5.scatter(particles_2p6['particles']['z'][0][0][0], particles_2p6['particles']['dE'][0][0][0], color='m', label='2.6 eVs');
ax5.scatter(particles_2p3['particles']['z'][0][0][0], particles_2p3['particles']['dE'][0][0][0], color='k', label='2.3 eVs');
ax5.scatter(particles_1p9['particles']['z'][0][0][0], particles_1p9['particles']['dE'][0][0][0], color='c', label='1.9 eVs');
ax5.scatter(particles_1p6['particles']['z'][0][0][0], particles_1p6['particles']['dE'][0][0][0], color='b', label='1.6 eVs');
ax5.scatter(particles_1p3['particles']['z'][0][0][0], particles_1p3['particles']['dE'][0][0][0], color='g', label='1.3 eVs');

ax5.set_xlabel('z [m]');
ax5.set_ylabel('dE [GeV]');
ax5.set_title('Particle Distribution: Longitudinal');
ax5.grid(True);

ax6.scatter(0,0,color='m', label='2.6 eVs')
ax6.scatter(0,0,color='k', label='2.3 eVs')
ax6.scatter(0,0,color='c', label='1.9 eVs')
ax6.scatter(0,0,color='b', label='1.6 eVs')
ax6.scatter(0,0,color='g', label='1.3 eVs')

legend_elements = [Line2D([0], [0], marker='o', color='w', label='2.6 eVs', markerfacecolor='m', markersize=15),
                   Line2D([0], [0], marker='o', color='w', label='2.3 eVs', markerfacecolor='k', markersize=15),
                   Line2D([0], [0], marker='o', color='w', label='1.9 eVs', markerfacecolor='c', markersize=15),
                   Line2D([0], [0], marker='o', color='w', label='1.6 eVs', markerfacecolor='b', markersize=15),
                   Line2D([0], [0], marker='o', color='w', label='1.3 eVs', markerfacecolor='g', markersize=15)]

ax6.legend(handles=legend_elements, loc='center')


# ~ plt.show();
# ~ fig1.savefig('Emittance_y.png', transparent=True);
fig1.savefig('Distribution_Turn_1000.png');
