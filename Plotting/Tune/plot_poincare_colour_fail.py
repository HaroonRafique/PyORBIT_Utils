# Plots the poincare sections in 5 phase spaces
# x-y x-xp y-yp xp-yp z-dE
# Over many turns.
# Uses all files in a directory with a .mat extension

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib import colors as mcolors
import numpy as np
import scipy.io as sio 
import os
import sys

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

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

iterators = []

max_file_no = 0
min_file_no = 1E6
min_file=str()
max_file=str()

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            print (os.path.join(subdir, file))        # full path to file
            filename = file.replace('_','.')            # replace _ with a .
            fileno = int(filename.split('.')[1])        # use turn number as a key
            iterators.append(fileno)
            if (fileno <= min_file_no):                  # find min turn
                min_file_no = fileno
                min_file = file
            elif (fileno >= max_file_no):                # find max turn
                max_file_no = fileno
                max_file = file
            
            d[fileno]={}                                # append empty turn to dictionary
            sio.loadmat(file, mdict=d[fileno])          # load the data from file  


print '\nThe first turn recorded is turn ', min_file_no, ' in file ', min_file
print '\nThe last turn recorded is turn ', max_file_no, ' in file ', max_file

no_input_files = len(iterators)
points_per_file = len(d[1]['particles']['x'][0][0][0])
particles = points_per_file
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
nums=range(0,particles-1)

legend_elements=[]

for i in nums:
    lab ='particle '+`i`
    legend_elements.append(Line2D([0], [0], marker='o', color='w', label=i , markerfacecolor=colors.items()[int(d[0]['particles']['ParticleIdNumber'][0][0][0][i])], markersize=15))


# ~ print iterators

# ~ print d[0]['particles']['x'][0][0][0]

# ~ print len(d)

# ~ print d

# ~ sys.exit("Stopped after loop")

#######################
# Make plots in loops #
#######################

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

# Use iterators so that if turns recorded are not continuous
# integers, we still go through every file in the directory

points_per_plot = no_input_files * points_per_file
total_points = 5 * points_per_plot
print '\nPlotting xy, please be patient.\nRemember we\'re plotting ',points_per_file,' points, for ',no_input_files,' files!\nThats ',points_per_plot,' points in total for each of the 5 plots.\nThat\'s a grand total of ', total_points,'!!!'

ax1.set_xlabel('x [m]');
ax1.set_ylabel('y [m]');
ax1.set_title('Particle Distribution: Real space');
ax1.grid(True);
for i in iterators:
        ax1.scatter(d[i]['particles']['x'][0][0][0], d[i]['particles']['y'][0][0][0], color='m', label='2.6 eVs');
        
print '\nPlotting xp yp, we appreciate your understanding in this trying time...'
ax2.set_xlabel('xp []');
ax2.set_ylabel('yp []');
ax2.set_title('Particle Distribution: xp yp');
ax2.grid(True);
for i in iterators:
        ax2.scatter(d[i]['particles']['xp'][0][0][0], d[i]['particles']['yp'][0][0][0], color='m', label='2.6 eVs');
        
print '\nPlotting x xp, we apologise for any inconvenience...'
ax3.set_xlabel('x [m]');
ax3.set_ylabel('xp []');
# ~ ax3.set_xlim();
# ~ ax3.set_ylim();
ax3.set_title('Particle Distribution: Horizontal phase space');
ax3.grid(True);
for i in iterators:
    for j in nums:
        ax3.scatter(d[i]['particles']['x'][0][0][0][j], d[i]['particles']['xp'][0][0][0][j], color=colors.items()[int(d[i]['particles']['ParticleIdNumber'][0][0][0][j])], label='2.6 eVs', marker=',');

# ~ for i in iterators:
        # ~ ax3.scatter(d[i]['particles']['x'][0][0][0], d[i]['particles']['xp'][0][0][0], color='m', label='2.6 eVs', marker=',');


print '\nPlotting y yp, OK almost there, this is kinda taking the piss. We get it :-)'
ax4.set_xlabel('y [m]');
ax4.set_ylabel('yp []');
ax4.set_title('Particle Distribution: Vertical phase space');
ax4.grid(True);
for i in iterators:
        ax4.scatter(d[i]['particles']['y'][0][0][0], d[i]['particles']['yp'][0][0][0], color='m', label='2.6 eVs');



print '\nPlotting z dE, whoop last one. Just this and the legend plot and we are outta here!'
ax5.set_xlabel('z [m]');
ax5.set_ylabel('dE [GeV]');
ax5.set_title('Particle Distribution: Longitudinal');
ax5.grid(True);
for i in iterators:
        ax5.scatter(d[i]['particles']['z'][0][0][0], d[i]['particles']['dE'][0][0][0], color='m', label='2.6 eVs');



ax6.scatter(0,0,color='m', label='2.6 eVs')
ax6.scatter(0,0,color='k', label='2.3 eVs')
ax6.scatter(0,0,color='c', label='1.9 eVs')
ax6.scatter(0,0,color='b', label='1.6 eVs')
ax6.scatter(0,0,color='g', label='1.3 eVs')


# ~ legend_elements = [Line2D([0], [0], marker='o', color='w', label='2.6 eVs', markerfacecolor='m', markersize=15),
                   # ~ Line2D([0], [0], marker='o', color='w', label='2.3 eVs', markerfacecolor='k', markersize=15),
                   # ~ Line2D([0], [0], marker='o', color='w', label='1.9 eVs', markerfacecolor='c', markersize=15),
                   # ~ Line2D([0], [0], marker='o', color='w', label='1.6 eVs', markerfacecolor='b', markersize=15),
                   # ~ Line2D([0], [0], marker='o', color='w', label='1.3 eVs', markerfacecolor='g', markersize=15)]

# ~ ax6.legend(handles=legend_elements, loc='center')

savename = str('Poincare_Dist_0-4p5sig_Multipole_0p2_Matched.png')
# ~ fig1.savefig('Emittance_y.png', transparent=True);
print '\nJust saving this bad boy, in case you forgot the filename is: '
print savename
print ' and the full path + filename is: '
print (os.path.join(subdir, savename))
fig1.savefig(savename);
print '\n\n\nALL DONE! PEACE OUT'
