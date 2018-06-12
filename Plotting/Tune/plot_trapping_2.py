# Plots the poincare sections in 5 phase spaces
# x-y x-xp y-yp xp-yp z-dE
# Over many turns.
# Uses all files in a directory with a .mat extension

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import FormatStrFormatter
from matplotlib.lines import Line2D
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


print '\nThe first turn recorded is turn ', min_file_no, ' in file ', min_file
print '\nThe last turn recorded is turn ', max_file_no, ' in file ', max_file

# ~ sys.exit("Stopped after loop")

#######################
# Make plots in loops #
#######################

# NORMALISATION
beta = 0.15448
gamma = 1.012149995

bety0=13.47433765
alfy0=0.4264503497
gamy0 = (1+alfy0*alfy0)/bety0
en_y = (9.3e-6)/4
eg_y = en_y / (beta * gamma)
sig_y = np.sqrt(eg_y * bety0)

betx0=12.79426135
alfx0=1.283306757 
gamx0 = (1+alfx0*alfx0)/betx0
eg_x =  (12.57e-6)/4
# ~ eg_x = en_x / (beta*gamma)
sig_x = np.sqrt(eg_x * betx0)

# e_x = bet_x px^2 + 2 a_x x px + gamma_x x^2 
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
fig, ax1 = plt.subplots();

emit_x0=[]

for j in range(0, len(d[0]['particles']['x'][0][0][0])):
    emit_x0.append( betx0*d[0]['particles']['xp'][0][0][0][j]*d[0]['particles']['xp'][0][0][0][j] + 2*alfx0*d[0]['particles']['x'][0][0][0][j]*d[0]['particles']['xp'][0][0][0][j] + gamx0*d[0]['particles']['x'][0][0][0][j]*d[0]['particles']['x'][0][0][0][j] )

for i in iterators:
    emit_x=[]
    for j in range(0, len(d[i]['particles']['x'][0][0][0])):
        e_x = ( betx0*d[i]['particles']['xp'][0][0][0][j]*d[i]['particles']['xp'][0][0][0][j] + 2*alfx0*d[i]['particles']['x'][0][0][0][j]*d[i]['particles']['xp'][0][0][0][j] + gamx0*d[i]['particles']['x'][0][0][0][j]*d[i]['particles']['x'][0][0][0][j] )
        e_xn = (e_x/emit_x0[j])
        print i
        print e_xn
        ax1.scatter(i, e_xn, color='m', label='2.6 eVs');
        
# ~ ax1.legend();
ax1.set_xlabel('x [m]');
ax1.set_ylabel('y [m]');
ax1.set_title('Particle Distribution: Real space');
ax1.grid(True);


savename = str('Particle_trapping.png')
# ~ fig1.savefig('Emittance_y.png', transparent=True);
print '\nJust saving this bad boy, in case you forgot the filename is: '
print savename
print ' and the full path + filename is: '
print (os.path.join(subdir, savename))
fig.savefig(savename);
print '\n\n\nALL DONE! PEACE OUT'
