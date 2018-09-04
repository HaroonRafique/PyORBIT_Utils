# Plots a gif of the distribution evolutions
# x-y x-xp y-yp z-dE
# Over many turns.
# Uses all files in a directory with a .mat extension
# This includes subdirectories so please be careful

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import FormatStrFormatter
from matplotlib.lines import Line2D
import numpy as np
import scipy.io as sio 
import os
import sys
import matplotlib.gridspec as gridspec
import imageio

###################
# Figure settings #
###################

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 200
plt.rcParams['savefig.dpi'] = 200

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'large'
plt.rcParams['legend.handlelength'] = 5

# Crashes on HPC-Batch
# ~ plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['lines.markersize'] = 0.25

###############################################
# Function to plot individual figures and gif #
###############################################

def plot_parameter_gif(parameter1, parameter2, p1_min, p1_max, p2_min, p2_max, xlab, ylab, bin_size = 128):
	filenames = []	
	
	# Loop Over turns, output one file for each turn
	for t in sorted(iterators):

		
		fig2 = plt.figure(1)
		gridspec.GridSpec(3,3)				# Create grid to resize subplots
		fig2.subplots_adjust(hspace = 0)	# Horizontal spacing between subplots
		fig2.subplots_adjust(wspace = 0)	# Vertical spacing between subplots
		tit1 = parameter1 + ' ' + parameter2 + 'Turn = ' + str(t)
		
		plt.subplot2grid((3,3), (0,0), colspan=2, rowspan=1)
		plt.hist(d[t]['particles'][parameter1][0][0][0], bins = bin_size,  range = [p1_min, p1_max], color='#000080')
		plt.ylabel('Frequency')
		plt.title(tit1)
		
		plt.subplot2grid((3,3), (1,0), colspan=2, rowspan=2)
		plt.hist2d(d[t]['particles'][parameter1][0][0][0], d[t]['particles'][parameter2][0][0][0], bin_size, range=[[p1_min, p1_max],[p2_min, p2_max]], cmap = plt.cm.jet)
		plt.xlabel(xlab)
		plt.ylabel(ylab)
		
		plt.subplot2grid((3,3), (1,2), colspan=1, rowspan=2)
		plt.hist(d[t]['particles'][parameter2][0][0][0], bins = bin_size,  range = [p2_min, p2_max], orientation=u'horizontal', color='#000080')
		plt.xlabel('Frequency')
		current_axis = plt.gca()
		current_axis.axes.get_yaxis().set_visible(False)

		figname = 'Plots/' + parameter1 + '_' + parameter2 + '_' + str(t) + '.png'
		fig2.savefig(figname);
		filenames.append(figname)
		plt.close()		
		
	print 'Creating ', parameter1, ' ', parameter2, ' GIF'
		
	images = []
	for filename in filenames:
		images.append(imageio.imread(filename))
	gifname = 'Gifs/' + parameter1 + '_' + parameter2 + '.gif'
	imageio.mimsave(gifname, images, duration = 0.3)	

	return;
	
#################
# Read files in #
#################

rootdir = os.getcwd()		# Get current working directory
os.mkdir('Gifs')
os.mkdir('Plots')
extensions = ('.mat')		# All outputs are .mat files
d = dict()
	
iterators = []				# Integers (turn) used to iterate over files

max_file_no = 0
min_file_no = 1E6
min_file = str()
max_file = str()

fileno = int(1)

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

bin_size = 128

###############
# Create GIFs #
###############

# ~ plot_parameter_gif(parameter1, parameter2, p1_min, p1_max, p2_min, p2_max, xlab, ylab, yunit='-', xunit='-', bin_size = 128):
plot_parameter_gif('z', 'dE', z_min, z_max, dE_min, dE_max, 'z [m]', 'dE [GeV]')
plot_parameter_gif('z', 'x', z_min, z_max, x_min, x_max, 'z [m]', 'x [m]')
plot_parameter_gif('x', 'xp', x_min, x_max, xp_min, xp_max, 'x [m]', 'xp [rad]')
plot_parameter_gif('x', 'y', x_min, x_max, y_min, y_max, 'x [m]', 'y [m]')
plot_parameter_gif('y', 'yp', y_min, y_max, yp_min, yp_max, 'y [m]', 'yp [rad]')

print 'All Done! Peace out'
