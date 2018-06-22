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

# Open file
filename = 'x=0.0045_single_particle_emittance.txt'
print filename
tit = filename.replace('=','_')
title = tit.split('_')[1]
print title
fin=open(filename,'r').readlines()[1:]

turn = []
emittance = []

for l in fin:
    turn.append(float(l.split()[0]))
    emittance.append(float(l.split()[1]))

initial_emittance = emittance[0]

emittance_n=[]

for i in range (0, len(emittance)):
	emittance_n.append(emittance[i]/initial_emittance)

# Plot
fig, ax1 = plt.subplots();

plt.title(title);
ax1.plot(turn, emittance_n, 'm', linewidth=0.5);

savename = str('Particle_trapping_z_1000synch_F=-4.4038e-09_x='+ title + 'm_1000turns.png')
plt.savefig(savename, dpi = 800);
print '\nJust saving this bad boy, in case you forgot the filename is: '
print savename
fig.savefig(savename);
print '\n\n\nALL DONE! PEACE OUT'
