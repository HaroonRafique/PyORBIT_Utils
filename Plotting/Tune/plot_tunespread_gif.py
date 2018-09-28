# Plots a gif of the particle phase which gives a rough indication of 
# the tunespread.
# Uses all files in a directory with a .mat extension
# This includes subdirectories so please be careful
# Note that the initial distribution in PyOrbit has no phase attributes
# and so should not be included in the directory (turn -1)

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


###################
# Loop over files #
###################

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

rootdir = os.getcwd()		# Get current working directory
os.mkdir('Gif_all')
os.mkdir('Gif_Qx_Qy')
extensions = ('.mat')		# All outputs are .mat files
d = dict()
b = dict()

iterators = []				# Integers (turn) used to iterate over files

max_file_no = 0
min_file_no = 1E6
min_file = str()
max_file = str()

fileno = int(1)
filenames_all = []				# Saved figure names used for GIF
filenames_z_dE = []				# Saved figure names used for GIF

xphase_max = 0.
xphase_min = 0.
yphase_max = 0.
yphase_min = 0.

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
			b[fileno] = d[fileno]['particles'].flatten()[0]
            
            # Find Max and Min values for plots
			if max(b[fileno]['ParticlePhaseAttributes'][2]) > xphase_max : xphase_max = max(b[fileno]['ParticlePhaseAttributes'][2])
			if min(b[fileno]['ParticlePhaseAttributes'][2]) < xphase_min : xphase_min = min(b[fileno]['ParticlePhaseAttributes'][2])
			if max(b[fileno]['ParticlePhaseAttributes'][3]) > yphase_max : yphase_max = max(b[fileno]['ParticlePhaseAttributes'][3])
			if min(b[fileno]['ParticlePhaseAttributes'][3]) < yphase_min : yphase_min = min(b[fileno]['ParticlePhaseAttributes'][3])
            # ~ if max(d[fileno]['particles'][0][0]['ParticlePhaseAttributes'][2]) > xphase_max : xphase_max = max(d[fileno]['particles'][0][0]['ParticlePhaseAttributes'][2])                  
            # ~ if max(d[fileno]['particles'][0][0]['ParticlePhaseAttributes'][3]) > yphase_max : yphase_max = max(d[fileno]['particles'][0][0]['ParticlePhaseAttributes'][3])  
            # ~ if min(d[fileno]['particles'][0][0]['ParticlePhaseAttributes'][2]) < xphase_min : xphase_min = min(d[fileno]['particles'][0][0]['ParticlePhaseAttributes'][2])                
            # ~ if min(d[fileno]['particles'][0][0]['ParticlePhaseAttributes'][3]) < yphase_min : yphase_min = min(d[fileno]['particles'][0][0]['ParticlePhaseAttributes'][3])  
            
print '\nThe first turn recorded is turn ', min_file_no, ' in file ', min_file
print '\nThe last turn recorded is turn ', max_file_no, ' in file ', max_file

# ~ xphase_max = 1.1* xphase_max
# ~ yphase_max = 1.1* yphase_max
# ~ xphase_min = 1.1* xphase_min
# ~ yphase_min = 1.1* yphase_min

# Manually set phase limits

xphase_max = 0.3
yphase_max = 0.3
xphase_min = 0.0
yphase_min = 0.0



print '\nxphase_max = ', xphase_max, ', xphase_min = ', xphase_min
print '\nyphase_max = ', yphase_max, ', yphase_min = ', yphase_min

bin_size_x = 128
bin_size_y = 128


# Loop Over turns, output one file for each turn
for t in sorted(iterators):
	
	print 'Plotting turn ', t

	# ~ fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row')
	fig2 = plt.figure(1)
	gridspec.GridSpec(3,3)				# Create grid to resize subplots
	fig2.subplots_adjust(hspace = 0)	# Horizontal spacing between subplots
	fig2.subplots_adjust(wspace = 0)	# Vertical spacing between subplots
	tit1 = 'Particle Phase Turn = ' + str(t)
	
	plt.subplot2grid((3,3), (0,0), colspan=2, rowspan=1)
	plt.hist(b[t]['ParticlePhaseAttributes'][2], bins = bin_size_x,  range = [xphase_min, xphase_max], density=True)
	plt.ylabel('Frequency')
	plt.title(tit1)
	
	plt.subplot2grid((3,3), (1,0), colspan=2, rowspan=2)
	plt.hist2d(b[t]['ParticlePhaseAttributes'][2], b[t]['ParticlePhaseAttributes'][3], bin_size_x, range=[[xphase_min, xphase_max],[yphase_min, yphase_max]])
	plt.xlabel('Qx [-]')
	plt.ylabel('Qy [-]')
	
	plt.subplot2grid((3,3), (1,2), colspan=1, rowspan=2)
	plt.hist(b[t]['ParticlePhaseAttributes'][3], bins = bin_size_y,  range = [yphase_min, yphase_max], density=True, orientation=u'horizontal')
	plt.xlabel('Frequency')
	current_axis = plt.gca()
	current_axis.axes.get_yaxis().set_visible(False)

	figname = 'Gif_Qx_Qy/Qx_Qy_'+ str(t) + '.png'
	fig2.savefig(figname);
	filenames_z_dE.append(figname)
	plt.close()	
	
# Make GIFs
print 'Creating Qx Qy GIF'
images = []
for filename in filenames_z_dE:
    images.append(imageio.imread(filename))
imageio.mimsave('Gif_all/Qx_Qy.gif', images, duration=1)	
