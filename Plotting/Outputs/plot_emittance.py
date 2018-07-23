# Plots the emittances for the PS_Injection studies at different
# longitudinal emittances

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio 

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'small'
plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 0.5

# Open File
file_in='output.mat'
main_label='Long Distn Test: Voltage'

particles=dict()

sio.loadmat(file_in, mdict=particles)

# Parameters
# ~ output.addParameter('turn', lambda: turn)
# ~ output.addParameter('intensity', lambda: bunchtwissanalysis.getGlobalMacrosize())
# ~ output.addParameter('n_mp', lambda: bunchtwissanalysis.getGlobalCount())
# ~ output.addParameter('gamma', lambda: bunch.getSyncParticle().gamma())
# ~ output.addParameter('mean_x', lambda: bunchtwissanalysis.getAverage(0))
# ~ output.addParameter('mean_xp', lambda: bunchtwissanalysis.getAverage(1))
# ~ output.addParameter('mean_y', lambda: bunchtwissanalysis.getAverage(2))
# ~ output.addParameter('mean_yp', lambda: bunchtwissanalysis.getAverage(3))
# ~ output.addParameter('mean_z', lambda: bunchtwissanalysis.getAverage(4))
# ~ output.addParameter('mean_dE', lambda: bunchtwissanalysis.getAverage(5))
# ~ output.addParameter('epsn_x', lambda: bunchtwissanalysis.getEmittanceNormalized(0))
# ~ output.addParameter('epsn_y', lambda: bunchtwissanalysis.getEmittanceNormalized(1))
# ~ output.addParameter('eps_z', lambda: get_eps_z(bunch, bunchtwissanalysis))
# ~ output.addParameter('bunchlength', lambda: get_bunch_length(bunch, bunchtwissanalysis))
# ~ output.addParameter('dpp_rms', lambda: get_dpp(bunch, bunchtwissanalysis))

#####################
#   Emittances      #
#####################

# ~ fig1=plt.figure(figsize=(6,10),constrained_layout=True)
fig1=plt.figure(figsize=(4,9))
ax1 = fig1.add_subplot(311) 
ax2 = fig1.add_subplot(312)
ax3 = fig1.add_subplot(313)

# ~ fig2.subplots_adjust(wspace=0.1, hspace=0.3, left=0.15, right=0.99, top=0.95, bottom=0.1)
fig1.subplots_adjust(wspace=0.1, hspace=0.3, left=0.1, right=0.99, top=0.9, bottom=0.1)
#fig.tight_layout()                            

# Plot raw
# ~ ax1.plot(particles_1p3['turn'][0], particles_1p3['epsn_x'][0], 'g', label='1.3 eVs');
# Plot change
# ~ ax1.plot(particles_1p3['turn'][0], (particles_1p3['epsn_x'][0]/particles_1p3['epsn_x'][0][0])*100, 'g', label='1.3 eVs');
# Plot percentage change
ax1.plot(particles['turn'][0], ((particles['epsn_x'][0]/particles['epsn_x'][0][0])*100)-100, 'g', label=main_label);

ax1.legend();

# ~ ax1.set(title='PS Emittance Horizontal', ylabel='Emittance_x [mm mrad]', xlabel='Turn [-]');
ax1.set_xlabel('Turn [-]');
ax1.set_ylabel('Horizontal Emittance Change [%]');
ax1.set_title('PS Emittance Horizontal');
ax1.grid(True);

# ~ plt.show();
# ~ plt.savefig('Emittance_x.png', dpi = 1600);

ax2.plot(particles['turn'][0], ((particles['epsn_y'][0]/particles['epsn_y'][0][0])*100)-100, 'g', label=main_label);

ax2.legend();
ax2.set_xlabel('Turn [-]');
ax2.set_ylabel('Vertical Emittance Change [%]');
ax2.set_title('PS Emittance Vertical');
ax2.grid(True);

ax3.plot(particles['turn'][0], ((particles['eps_z'][0]/particles['eps_z'][0][0])*100)-100, 'g', label=main_label);

ax3.legend();
ax3.set_xlabel('Turn [-]');
ax3.set_ylabel('Longitudinal Emittance Change [%]');
ax3.set_title('PS Emittance Vertical');
ax3.grid(True);

# ~ plt.show();
# ~ fig1.savefig('Emittance_y.png', dpi = 1600, transparent=True);
# ~ fig1.savefig('Emittances.png', dpi = 800);
fig1.savefig('Emittances_percentage.png');

#####################
#   Emittances 2    #
#####################

# ~ fig1=plt.figure(figsize=(6,10),constrained_layout=True)
fig1=plt.figure(figsize=(4,9))
ax1 = fig1.add_subplot(311) 
ax2 = fig1.add_subplot(312)
ax3 = fig1.add_subplot(313)

# ~ fig2.subplots_adjust(wspace=0.1, hspace=0.3, left=0.15, right=0.99, top=0.95, bottom=0.1)
fig1.subplots_adjust(wspace=0.1, hspace=0.3, left=0.15, right=0.99, top=0.9, bottom=0.1)
#fig.tight_layout()                            

ax1.plot(particles['turn'][0], particles['epsn_x'][0], 'g', label=main_label);

ax1.legend();

# ~ ax1.set(title='PS Emittance Horizontal', ylabel='Emittance_x [mm mrad]', xlabel='Turn [-]');
ax1.set_xlabel('Turn [-]');
ax1.set_ylabel('Horizontal Emittance [mm mrad]');
ax1.set_title('PS Emittance Horizontal');
ax1.grid(True);

# ~ plt.show();
# ~ plt.savefig('Emittance_x.png', dpi = 1600);


ax2.plot(particles['turn'][0], particles['epsn_y'][0], 'g', label=main_label);

ax2.legend();
ax2.set_xlabel('Turn [-]');
ax2.set_ylabel('Vertical Emittance [mm mrad]');
ax2.set_title('PS Emittance Vertical');
ax2.grid(True);

ax3.plot(particles['turn'][0], particles['eps_z'][0], 'g', label=main_label);

ax3.legend();
ax3.set_xlabel('Turn [-]');
ax3.set_ylabel('Longitudinal Emittance [eVs]');
ax3.set_title('PS Emittance Vertical');
ax3.grid(True);

# ~ plt.show();
# ~ fig1.savefig('Emittance_y.png', dpi = 1600, transparent=True);
# ~ fig1.savefig('Emittances.png', dpi = 800);
fig1.savefig('Emittances.png');

#####################
#   MEAN X and Y    #
#####################

fig2=plt.figure(figsize=(4,8))
ax3 = fig2.add_subplot(311) 
ax4 = fig2.add_subplot(312)
ax5 = fig2.add_subplot(313)

# ~ fig1.subplots_adjust(wspace=0.1, hspace=0.5, left=0.1, right=0.99, top=0.9, bottom=0.1)
fig2.subplots_adjust(wspace=0.1, hspace=0.3, left=0.2, right=0.99, top=0.95, bottom=0.1)
#fig.tight_layout()                            

# Plot raw
# ~ ax1.plot(particles_1p3['turn'][0], particles_1p3['epsn_x'][0], 'g', label='1.3 eVs');
# Plot change
# ~ ax1.plot(particles_1p3['turn'][0], (particles_1p3['epsn_x'][0]/particles_1p3['epsn_x'][0][0])*100, 'g', label='1.3 eVs');
# ~ # Plot percentage change
# ~ ax3.plot(particles_1p3['turn'][0], ((particles_1p3['mean_x'][0]/particles_1p3['mean_x'][0][0])*100)-100, 'g', label='1.3 eVs', linewidth=0.5);

# Plot percentage change
ax3.plot(particles['turn'][0], particles['mean_x'][0], 'g', label=main_label, linewidth=0.5);

ax3.legend();

# ~ ax1.set(title='PS Emittance Horizontal', ylabel='Emittance_x [mm mrad]', xlabel='Turn [-]');
ax3.set_xlabel('Turn [-]');
# ~ ax3.set_ylabel('Mean X Change [%]');
ax3.set_ylabel('Mean X [m]');
ax3.set_title('PS Mean Position Horizontal');
ax3.grid(True);

# ~ plt.show();
# ~ plt.savefig('Emittance_x.png', dpi = 1600);

ax4.plot(particles['turn'][0], particles['mean_y'][0], 'g', label=main_label, linewidth=0.5);

ax4.legend();
ax4.set_xlabel('Turn [-]');
# ~ ax4.set_ylabel('Mean Y Change [%]');
ax4.set_ylabel('Mean Y [m]');
ax4.set_title('PS Mean Position Vertical');
ax4.grid(True);

ax5.plot(particles['turn'][0], particles['mean_z'][0], 'g', label=main_label, linewidth=0.5);

ax5.legend();
ax5.set_xlabel('Turn [-]');
# ~ ax4.set_ylabel('Mean Y Change [%]');
ax5.set_ylabel('Mean Z [m]');
ax5.set_title('PS Mean Position Longitudinal');
ax5.grid(True);
# ~ plt.show();
# ~ fig1.savefig('Emittance_y.png', dpi = 1600, transparent=True);
fig2.savefig('Means_percentage.png');
