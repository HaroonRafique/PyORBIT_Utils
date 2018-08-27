# Plots a gif of the distribution evolutions
# x-y x-xp y-yp z-dE
# Over many turns.
# Uses all files in a directory with a .mat extension
# This includes subdirectories so please be careful

# TODO:
# Fix axes according to max values
# plot heatmap

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import FormatStrFormatter
from matplotlib.lines import Line2D
import numpy as np
import scipy.io as sio 
import os
import sys
from mpl_toolkits.mplot3d import axes3d

###################
# Figure settings #
###################

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'large'
plt.rcParams['legend.handlelength'] = 5

# Crashes on HPC-Batch
# ~ plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['lines.markersize'] = 0.25

###################
# Loop over files #
###################

rootdir = os.getcwd()		# Get current working directory
os.mkdir('Gif_all')
os.mkdir('Gif_z_dE')
extensions = ('.mat')		# All outputs are .mat files
d = dict()
	
iterators = []				# Integers (turn) used to iterate over files

max_file_no = 0
min_file_no = 1E6
min_file = str()
max_file = str()

fileno = int(1)
filenames_all = []				# Saved figure names used for GIF
filenames_z_dE = []				# Saved figure names used for GIF

x_max = 0.
xp_max = 0.
y_max = 0.
yp_max = 0.
z_max = 0.
dE_max = 0.
x_min = 0.
xp_min = 0.
y_min = 0.
yp_min = 0.
z_min = 0.
dE_min = 0.

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            print (os.path.join(subdir, file))        # full path to file
            filename = file.replace('_','.')            # replace _ with a .
            # ~ print filename
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
            
            # Find Max and Min values for plots
            if max(d[fileno]['particles']['x'][0][0][0]) > x_max : x_max = max(d[fileno]['particles']['x'][0][0][0])            
            if max(d[fileno]['particles']['xp'][0][0][0]) > xp_max : xp_max = max(d[fileno]['particles']['xp'][0][0][0])            
            if max(d[fileno]['particles']['y'][0][0][0]) > y_max : y_max = max(d[fileno]['particles']['y'][0][0][0])            
            if max(d[fileno]['particles']['yp'][0][0][0]) > yp_max : yp_max = max(d[fileno]['particles']['yp'][0][0][0])            
            if max(d[fileno]['particles']['z'][0][0][0]) > z_max : z_max = max(d[fileno]['particles']['z'][0][0][0])            
            if max(d[fileno]['particles']['dE'][0][0][0]) > dE_max : dE_max = max(d[fileno]['particles']['dE'][0][0][0])
            if min(d[fileno]['particles']['x'][0][0][0]) < x_min : x_min = min(d[fileno]['particles']['x'][0][0][0])            
            if min(d[fileno]['particles']['xp'][0][0][0]) < xp_min : xp_min = min(d[fileno]['particles']['xp'][0][0][0])            
            if min(d[fileno]['particles']['y'][0][0][0]) < y_min : y_min = min(d[fileno]['particles']['y'][0][0][0])            
            if min(d[fileno]['particles']['yp'][0][0][0]) < yp_min : yp_min = min(d[fileno]['particles']['yp'][0][0][0])            
            if min(d[fileno]['particles']['z'][0][0][0]) < z_min : z_min = min(d[fileno]['particles']['z'][0][0][0])            
            if min(d[fileno]['particles']['dE'][0][0][0]) < dE_min : dE_min = min(d[fileno]['particles']['dE'][0][0][0])
            
print '\nThe first turn recorded is turn ', min_file_no, ' in file ', min_file
print '\nThe last turn recorded is turn ', max_file_no, ' in file ', max_file

print '\nz_max = ', z_max, ', z_min = ', z_min
print '\ndE_max = ', dE_max, ', dE_min = ', dE_min

z_max = 50.
z_min = -50.

x_max = 1.1* x_max
xp_max = 1.1* xp_max
y_max = 1.1* y_max
yp_max = 1.1* yp_max
z_max = 1.1* z_max
dE_max = 1.1* dE_max
x_min = 1.1* x_min
xp_min = 1.1* xp_min
y_min = 1.1* y_min
yp_min = 1.1* yp_min
z_min = 1.1* z_min
dE_min = 1.1* dE_min

bin_size_x = 128
bin_size_y = 128

# ~ sys.exit("Stopped after loop")

# Loop Over turns, output one file for each turn
for t in sorted(iterators):
	
	print 'Plotting turn ', t

	fig1=plt.figure(figsize=(6,10),constrained_layout=True)
	# ~ fig1=plt.figure(figsize=(6,10))
	plt.clf()
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

	# ~ ax1.scatter(d[t]['particles']['x'][0][0][0], d[t]['particles']['y'][0][0][0], color='g', label='1.3 eVs');
	# ~ a = np.array([d[t]['particles']['x'][0][0][0], d[t]['particles']['y'][0][0][0]])
	# ~ ax1.imshow(a, cmap='hot', interpolation='nearest')
	
	# Create heatmap
	heatmap, xedges, yedges = np.histogram2d(d[t]['particles']['x'][0][0][0], d[t]['particles']['y'][0][0][0], bins=(bin_size_x, bin_size_y), range=[[x_min, x_max],[y_min, y_max]])
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
	ax1.imshow(heatmap, extent=extent, aspect=( (x_min - x_max)/(y_min - y_max) ) )

	# ~ ax1.legend();
	ax1.set_xlabel('x [m]');
	ax1.set_ylabel('y [m]');
	# ~ ax1.set_xlim(x_min, x_max)
	# ~ ax1.set_ylim(y_min, y_max)
	tit1 = 'X Y Turn = ' + str(t)
	ax1.set_title(tit1);
	ax1.grid(True);

	# ~ ax2.scatter(d[t]['particles']['xp'][0][0][0], d[t]['particles']['yp'][0][0][0], color='g', label='1.3 eVs');
	heatmap2, xedges2, yedges2 = np.histogram2d(d[t]['particles']['xp'][0][0][0], d[t]['particles']['yp'][0][0][0], bins=(bin_size_x, bin_size_y), range=[[xp_min, xp_max],[yp_min, yp_max]])
	extent2 = [xedges2[0], xedges2[-1], yedges2[0], yedges2[-1]]
	ax2.imshow(heatmap2, extent=extent2, aspect=( (xp_min - xp_max)/(yp_min - yp_max) ))

	ax2.set_xlabel('xp []');
	ax2.set_ylabel('yp []');
	# ~ ax2.set_xlim(xp_min, xp_max)
	# ~ ax2.set_ylim(yp_min, yp_max)
	tit2 = 'XP YP Turn = ' + str(t)
	ax2.set_title(tit2);
	ax2.grid(True);

	# ~ ax3.scatter(d[t]['particles']['x'][0][0][0], d[t]['particles']['xp'][0][0][0], color='g', label='1.3 eVs');
	heatmap3, xedges3, yedges3 = np.histogram2d(d[t]['particles']['x'][0][0][0], d[t]['particles']['xp'][0][0][0], bins=(bin_size_x, bin_size_y), range=[[x_min, x_max],[xp_min, xp_max]])
	extent3 = [xedges3[0], xedges3[-1], yedges3[0], yedges3[-1]]
	ax3.imshow(heatmap3, extent=extent3, aspect=( (x_min - x_max)/(xp_min - xp_max) ))
	
	ax3.set_xlabel('x [m]');
	ax3.set_ylabel('xp []');	
	# ~ ax3.set_xlim(x_min, x_max)
	# ~ ax3.set_ylim(xp_min, xp_max)
	tit3 = 'X XP Turn = ' + str(t)
	ax3.set_title(tit3);
	ax3.grid(True);

	# ~ ax4.scatter(d[t]['particles']['y'][0][0][0], d[t]['particles']['yp'][0][0][0], color='g', label='1.3 eVs');
	heatmap4, xedges4, yedges4 = np.histogram2d(d[t]['particles']['y'][0][0][0], d[t]['particles']['yp'][0][0][0], bins=(bin_size_x, bin_size_y), range=[[y_min, y_max],[yp_min, yp_max]])
	extent4 = [xedges4[0], xedges4[-1], yedges4[0], yedges4[-1]]
	ax4.imshow(heatmap4, extent=extent4, aspect=( (y_min - y_max)/(yp_min - yp_max) ))

	ax4.set_xlabel('y [m]');
	ax4.set_ylabel('yp []');
	# ~ ax4.set_xlim(y_min, y_max)
	# ~ ax4.set_ylim(yp_min, yp_max)	
	tit4 = 'Y YP Turn = ' + str(t)
	ax4.set_title(tit4);
	ax4.grid(True);

	# ~ ax5.scatter(d[t]['particles']['z'][0][0][0], d[t]['particles']['dE'][0][0][0], color='g', label='1.3 eVs');
	heatmap5, xedges5, yedges5 = np.histogram2d(d[t]['particles']['z'][0][0][0], d[t]['particles']['dE'][0][0][0], bins=(bin_size_x, bin_size_y), range=[[z_min, z_max],[dE_min, dE_max]])
	extent5 = [xedges5[0], xedges5[-1], yedges5[0], yedges5[-1]]
	ax5.imshow(heatmap5, extent=extent5, aspect=( (z_min - z_max)/(dE_min - dE_max) ))

	ax5.set_xlabel('z [m]');
	ax5.set_ylabel('dE [GeV]');
	# ~ ax5.set_xlim(z_min, z_max)
	# ~ ax5.set_ylim(dE_min, dE_max)
	tit5 = 'Z dE Turn = ' + str(t)
	ax5.set_title(tit5);
	ax5.grid(True);

	ax6.scatter(0,0,color='m')

	lab = 'TURN = ' + str(t)
	legend_elements = [Line2D([0], [0], marker='o', color='w', label=lab, markerfacecolor='m', markersize=15)]

	ax6.legend(handles=legend_elements, loc='center')


	# ~ plt.show();
	# ~ fig1.savefig('Emittance_y.png', transparent=True);
	figname = 'Gif_all/all_'+ str(t) + '.png'
	fig1.savefig(figname);
	filenames_all.append(figname)
	plt.close()
	
#######################
# 2nd plot for z - dE #
#######################
	fig2 = plt.figure(figsize=(5,5),constrained_layout=True)
	plt.clf()
	ax1 = fig2.add_subplot(111) 
	
	heatmap6, xedges6, yedges6 = np.histogram2d(d[t]['particles']['z'][0][0][0], d[t]['particles']['dE'][0][0][0], bins=(bin_size_x, bin_size_y), range=[[z_min, z_max],[dE_min, dE_max]])
	# ~ heatmap6, xedges6, yedges6 = np.histogram2d(d[t]['particles']['z'][0][0][0], d[t]['particles']['dE'][0][0][0], bins=(bin_size_x, bin_size_y))
	extent6 = [xedges6[0], xedges6[-1], yedges6[0], yedges6[-1]]
	ax1.imshow(heatmap6, extent=extent6, aspect=( (z_min - z_max)/(dE_min - dE_max) ))

	ax1.set_xlabel('z [m]');
	ax1.set_ylabel('dE [GeV]');
	
	tit1 = 'Z dE Turn = ' + str(t)
	ax1.set_title(tit1);
	ax1.grid(True);

	figname = 'Gif_z_dE/z_dE_'+ str(t) + '.png'
	fig2.savefig(figname);
	filenames_z_dE.append(figname)
	plt.close()	
	
# Make GIFs

print 'Creating first GIF'
import imageio
images = []
for filename in filenames_all:
    images.append(imageio.imread(filename))
imageio.mimsave('Gif_all/all.gif', images)	

print 'Creating second GIF'
images = []
for filename in filenames_z_dE:
    images.append(imageio.imread(filename))
imageio.mimsave('Gif_z_dE/z_dE.gif', images)	


print 'All Done! Peace out'
