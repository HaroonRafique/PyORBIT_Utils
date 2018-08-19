# Plots the poincare sections in 5 phase spaces
# x-y x-xp y-yp xp-yp z-dE
# Over many turns.
# Uses all files in a directory with a .mat extension

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import numpy as np
import scipy.io as sio 
import os
import sys

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'large'
plt.rcParams['legend.handlelength'] = 5

plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['lines.markersize'] = 0.25

###################
# Loop over files #
###################

rootdir = os.getcwd()
extensions = ('.mat')
d = dict()
grid=''

iterators = []

max_file_no = 0
min_file_no = 1E2
min_file=str()
max_file=str()

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            print (os.path.join(subdir, file))          # full path to file
            filename = file.replace('_','.')            # replace _ with a .
            nodeno = int(filename.split('.')[0])        # use node number as a key
            grid = str(filename.split('.')[1])          # SC gridsize
            iterators.append(nodeno)
            if (nodeno <= min_file_no):                  # find min turn
                min_file_no = nodeno
                min_file = file
            elif (nodeno >= max_file_no):                # find max turn
                max_file_no = nodeno
                max_file = file
            
            d[nodeno]={}                                # append empty turn to dictionary
            sio.loadmat(file, mdict=d[nodeno])          # load the data from file  


iterators = sorted(iterators)
print iterators

print '\nThe lowest number of nodes is ', min_file_no, ' in file ', min_file
print '\nThe highest number of nodes is ', max_file_no, ' in file ', max_file
print '\nNode files present:', iterators



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
fig1.subplots_adjust(wspace=0.1, hspace=0.3, left=0.15, right=0.99, top=0.9, bottom=0.1)
#fig.tight_layout()                            

# Plot raw
# ~ ax1.plot(particles_1p3['turn'][0], particles_1p3['epsn_x'][0], 'g', label='1.3 eVs');
# Plot change
# ~ ax1.plot(particles_1p3['turn'][0], (particles_1p3['epsn_x'][0]/particles_1p3['epsn_x'][0][0])*100, 'g', label='1.3 eVs');
# Plot percentage change

for i in iterators:
    labelin = str(i)
    ax1.plot(d[i]['turn'][0], ((d[i]['epsn_x'][0]/d[i]['epsn_x'][0][0])*100)-100, label=i);
    ax2.plot(d[i]['turn'][0], ((d[i]['epsn_y'][0]/d[i]['epsn_y'][0][0])*100)-100, label=i);
    ax3.plot(d[i]['turn'][0], ((d[i]['eps_z'][0]/d[i]['eps_z'][0][0])*100)-100, label=i);

ax1.legend();

# ~ sys.exit()

# ~ ax1.set(title='PS Emittance Horizontal', ylabel='Emittance_x [mm mrad]', xlabel='Turn [-]');
ax1.set_xlabel('Turn [-]');
ax1.set_ylabel('Horizontal Emittance Change [%]');
ax1.set_title('PS Emittance Horizontal');
ax1.grid(True);

ax2.legend();
ax2.set_xlabel('Turn [-]');
ax2.set_ylabel('Vertical Emittance Change [%]');
ax2.set_title('PS Emittance Vertical');
ax2.grid(True);

ax3.legend();
ax3.set_xlabel('Turn [-]');
ax3.set_ylabel('Longitudinal Emittance Change [%]');
ax3.set_title('PS Emittance Longitudinal');
ax3.grid(True);

# ~ plt.show();
# ~ fig1.savefig('Emittance_y.png', dpi = 1600, transparent=True);
# ~ fig1.savefig('Emittances.png', dpi = 800);
figname = 'Emittances_'+grid+'.png'
fig1.savefig(figname);

sys.exit()

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
# ~ ax3.plot(particles_1p6['turn'][0], ((particles_1p6['mean_x'][0]/particles_1p6['mean_x'][0][0])*100)-100, 'b', label='1.6 eVs', linewidth=0.5);
# ~ ax3.plot(particles_1p9['turn'][0], ((particles_1p9['mean_x'][0]/particles_1p9['mean_x'][0][0])*100)-100, 'c', label='1.9 eVs', linewidth=0.5);
# ~ ax3.plot(particles_2p3['turn'][0], ((particles_2p3['mean_x'][0]/particles_2p3['mean_x'][0][0])*100)-100, 'k', label='2.3 eVs', linewidth=0.5);
# ~ ax3.plot(particles_2p6['turn'][0], ((particles_2p6['mean_x'][0]/particles_2p6['mean_x'][0][0])*100)-100, 'm', label='2.6 eVs', linewidth=0.5);
# Plot percentage change
ax3.plot(particles_2p6['turn'][0], particles_2p6['mean_x'][0], 'm', label='2.6 eVs', linewidth=0.5);
ax3.plot(particles_2p3['turn'][0], particles_2p3['mean_x'][0], 'k', label='2.3 eVs', linewidth=0.5);
ax3.plot(particles_1p9['turn'][0], particles_1p9['mean_x'][0], 'c', label='1.9 eVs', linewidth=0.5);
ax3.plot(particles_1p6['turn'][0], particles_1p6['mean_x'][0], 'b', label='1.6 eVs', linewidth=0.5);
ax3.plot(particles_1p3['turn'][0], particles_1p3['mean_x'][0], 'g', label='1.3 eVs', linewidth=0.5);

ax3.legend();

# ~ ax1.set(title='PS Emittance Horizontal', ylabel='Emittance_x [mm mrad]', xlabel='Turn [-]');
ax3.set_xlabel('Turn [-]');
# ~ ax3.set_ylabel('Mean X Change [%]');
ax3.set_ylabel('Mean X [m]');
ax3.set_title('PS Mean Position Horizontal');
ax3.grid(True);

# ~ plt.show();
# ~ plt.savefig('Emittance_x.png', dpi = 1600);


ax4.plot(particles_2p6['turn'][0], particles_2p6['mean_y'][0], 'm', label='2.6 eVs', linewidth=0.5);
ax4.plot(particles_2p3['turn'][0], particles_2p3['mean_y'][0], 'k', label='2.3 eVs', linewidth=0.5);
ax4.plot(particles_1p9['turn'][0], particles_1p9['mean_y'][0], 'c', label='1.9 eVs', linewidth=0.5);
ax4.plot(particles_1p6['turn'][0], particles_1p6['mean_y'][0], 'b', label='1.6 eVs', linewidth=0.5);
ax4.plot(particles_1p3['turn'][0], particles_1p3['mean_y'][0], 'g', label='1.3 eVs', linewidth=0.5);

ax4.legend();
ax4.set_xlabel('Turn [-]');
# ~ ax4.set_ylabel('Mean Y Change [%]');
ax4.set_ylabel('Mean Y [m]');
ax4.set_title('PS Mean Position Vertical');
ax4.grid(True);


ax5.plot(particles_2p6['turn'][0], particles_2p6['mean_z'][0], 'm', label='2.6 eVs', linewidth=0.5);
ax5.plot(particles_2p3['turn'][0], particles_2p3['mean_z'][0], 'k', label='2.3 eVs', linewidth=0.5);
ax5.plot(particles_1p9['turn'][0], particles_1p9['mean_z'][0], 'c', label='1.9 eVs', linewidth=0.5);
ax5.plot(particles_1p6['turn'][0], particles_1p6['mean_z'][0], 'b', label='1.6 eVs', linewidth=0.5);
ax5.plot(particles_1p3['turn'][0], particles_1p3['mean_z'][0], 'g', label='1.3 eVs', linewidth=0.5);

ax5.legend();
ax5.set_xlabel('Turn [-]');
# ~ ax4.set_ylabel('Mean Y Change [%]');
ax5.set_ylabel('Mean Z [m]');
ax5.set_title('PS Mean Position Longitudinal');
ax5.grid(True);
# ~ plt.show();
# ~ fig1.savefig('Emittance_y.png', dpi = 1600, transparent=True);
fig2.savefig('Means.png');
