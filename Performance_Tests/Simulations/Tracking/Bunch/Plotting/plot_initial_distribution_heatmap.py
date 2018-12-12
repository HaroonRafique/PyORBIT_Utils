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
from mpl_toolkits.mplot3d import axes3d
import matplotlib.gridspec as gridspec
#import imageio

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
#os.mkdir('Gif_z_dE')
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
x_max = 0.
y_max = 0.
x_min = 0.
xp_min = 0.
y_min = 0.
yp_min = 0.
x_min = 0.
y_min = 0.

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
            if max(d[fileno]['particles']['x'][0][0][0]) > x_max : x_max = max(d[fileno]['particles']['x'][0][0][0])            
            if max(d[fileno]['particles']['y'][0][0][0]) > y_max : y_max = max(d[fileno]['particles']['y'][0][0][0])
            if min(d[fileno]['particles']['x'][0][0][0]) < x_min : x_min = min(d[fileno]['particles']['x'][0][0][0])            
            if min(d[fileno]['particles']['xp'][0][0][0]) < xp_min : xp_min = min(d[fileno]['particles']['xp'][0][0][0])            
            if min(d[fileno]['particles']['y'][0][0][0]) < y_min : y_min = min(d[fileno]['particles']['y'][0][0][0])            
            if min(d[fileno]['particles']['yp'][0][0][0]) < yp_min : yp_min = min(d[fileno]['particles']['yp'][0][0][0])            
            if min(d[fileno]['particles']['x'][0][0][0]) < x_min : x_min = min(d[fileno]['particles']['x'][0][0][0])            
            if min(d[fileno]['particles']['y'][0][0][0]) < y_min : y_min = min(d[fileno]['particles']['y'][0][0][0])
            
print '\nThe first turn recorded is turn ', min_file_no, ' in file ', min_file
print '\nThe last turn recorded is turn ', max_file_no, ' in file ', max_file

print '\nx_max = ', x_max, ', x_min = ', x_min
print '\ny_max = ', y_max, ', y_min = ', y_min

#x_max = 50.
#x_min = -50.

# ~ x_max = 1.1* x_max
# ~ xp_max = 1.1* xp_max
# ~ y_max = 1.1* y_max
# ~ yp_max = 1.1* yp_max
# ~ x_max = 1.1* x_max
# ~ y_max = 1.1* y_max
# ~ x_min = 1.1* x_min
# ~ xp_min = 1.1* xp_min
# ~ y_min = 1.1* y_min
# ~ yp_min = 1.1* yp_min
# ~ x_min = 1.1* x_min
# ~ y_min = 1.1* y_min

bin_size_x = 128
bin_size_y = 128

# ~ sys.exit("Stopped after loop")

# Loop Over turns, output one file for each turn
for t in sorted(iterators):
	
	print 'Plotting turn ', t

	# ~ fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
	fig2 = plt.figure(1)
	gridspec.GridSpec(3,3)				# Create grid to resize subplots
	fig2.subplots_adjust(hspace = 0)	# Horizontal spacing between subplots
	fig2.subplots_adjust(wspace = 0)	# Vertical spacing between subplots
	tit1 = 'x y Turn = ' + str(t)
	
	plt.subplot2grid((3,3), (0,0), colspan=2, rowspan=1)
	plt.hist(d[t]['particles']['x'][0][0][0], bins = bin_size_x,  range = [x_min, x_max], density=True)
	plt.ylabel('Frequency')
	plt.title(tit1)
	
	plt.subplot2grid((3,3), (1,0), colspan=2, rowspan=2)
	plt.hist2d(d[t]['particles']['x'][0][0][0], d[t]['particles']['y'][0][0][0], bin_size_x, range=[[x_min, x_max],[y_min, y_max]])
	plt.xlabel('x [m]')
	plt.ylabel('y [m]')
	
	plt.subplot2grid((3,3), (1,2), colspan=1, rowspan=2)
	plt.hist(d[t]['particles']['y'][0][0][0], bins = bin_size_y,  range = [y_min, y_max], density=True, orientation=u'horizontal')
	plt.xlabel('Frequency')
	current_axis = plt.gca()
	current_axis.axes.get_yaxis().set_visible(False)

	figname = 'x_y_'+ str(t) + '.png'
	fig2.savefig(figname);
	filenames_z_dE.append(figname)
	plt.close()	
	
# Make GIFs
# ~ print 'Creating z dE GIF'
# ~ images = []
# ~ for filename in filenames_z_dE:
    # ~ images.append(imageio.imread(filename))
# ~ imageio.mimsave('Gif_z_dE/z_dE.gif', images, duration=1)	


print 'All Done! Peace out'
