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

# ~ plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['lines.markersize'] = 0.25

# Read file, looks like:
#ParticleID	Turn	x[m]	xp	y[m]	yp	z[m]	dE[GeV]

# Make arrays to hold everything simply - assume only 1 particle here
Pid=[]
Turn=[]
x=[]
xp=[]
y=[]
yp=[]
dE=[]
z=[]
particles=[]

filename='SC/Particle_0.dat'
fin=open(filename,'r').readlines()[1:]

for l in fin:
	
	if int(l.split()[0]) not in Pid:
		particles.append(int(l.split()[0]))
		
	Pid.append(int(l.split()[0]))
	Turn.append(int(l.split()[1]))
	x.append(float(l.split()[2]))
	xp.append(float(l.split()[3]))
	y.append(float(l.split()[4]))
	yp.append(float(l.split()[5]))
	z.append(float(l.split()[6]))
	dE.append(float(l.split()[7]))
	

print 'Number of particles in input file: ', len(particles)
print 'Number of turns in input file: ', max(Turn)+1

if len(particles) > 1:
	print 'Warning: This script is designed to take data from only a single particle'
	

#######################
# Make plots in loops #
#######################

# NORMALISATION
synch_turn=100.

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
sig_x = np.sqrt(eg_x * betx0)

emit_x=[]
emit_y=[]
e_xn=[]
e_yn=[]

# e_x = bet_x px^2 + 2 a_x x px + gamma_x x^2 
for j in range(0, len(x), 1):
    emit_x.append( betx0*xp[j]*xp[j] + 2*alfx0*x[j]*xp[j] + gamx0*x[j]*x[j] )
    e_xn.append(emit_x[j] / emit_x[0])

# ~ for j in range(0, len(y), 1):
    # ~ emit_y.append( bety0*yp[j]*yp[j] + 2*alfy0*y[j]*yp[j] + gamy0*y[j]*y[j] )
    # ~ e_yn.append(emit_y[j] / emit_y[0])

#################
#   Trapping    #
# ~ #################
fig, ax1 = plt.subplots();

ax1.plot(e_xn, color='m');
        
ax1.set_xlabel('Turn [-]');
ax1.set_ylabel('emittance_x / emittance_x0');
ax1.set_title('Normalised particle emittance as a function of turn');
ax1.grid(True);


savename = str('Particle_trapping_1000synch_F=-1.951E-11_5mm_1500turns.png')
print '\nJust saving this bad boy, in case you forgot the filename is: '
print savename
fig.savefig(savename);
print '\n\n\nALL DONE! PEACE OUT'

# ~ sys.exit("Stopped after loop")
##########
#   z    #
##########
fig, ax1 = plt.subplots();

# ~ for i in range(0,736):    
# ~ for i in particles:
    # ~ print 'plotting z, turn ', i
    # ~ for j in range(0, len(z)):
ax1.scatter(Turn, z, color='m');
        
# ~ ax1.legend();
# ~ ax1.set_xlabel('Turn / Synchrotron Period [-]');
ax1.set_xlabel('Turn [-]');
ax1.set_ylabel('z [m]');
ax1.set_title('Particle z co-ordinate as a function of turn');
ax1.grid(True);


print 'z_0 = ', z[0]
print 'z_f = ', z[-1]

print 'z_f - z_0 = ', (z[-1] - z[0])

savename = str('Particle_trapping_z_1000synch_F=-1.951E-11_5mm_1500turns.png')
# ~ fig1.savefig('Emittance_y.png', transparent=True);
print '\nJust saving this bad boy, in case you forgot the filename is: '
print savename
fig.savefig(savename);
print '\n\n\nALL DONE! PEACE OUT'
