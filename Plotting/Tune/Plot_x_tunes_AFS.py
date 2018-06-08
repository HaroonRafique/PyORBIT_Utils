import os
import sys
import numpy as np
import scipy.io as sio
import glob
import pandas as pd
from matplotlib import cm
from scipy.interpolate import griddata
import numpy.ma as ma
import pylab as plt
import sys
sys.path.append("/eos/user/n/nkarast/SWAN/PyNAFF/")
from PyNAFF import naff
import matplotlib.pyplot as plt

intensity = 'I=1.9E11'
step = '2'
plane = 'x'
extra = 'dpp*beta'
case = 'Step' + step + '_' + plane + '_' + intensity
if len(extra) > 0:
    case = case + '_' + extra
#Qx = 4.3504
Qx = 4.338
Qy = 3.2

filename = 'mainbunch'
n_part = 100
n_turns = 1024
files = glob.glob(filename + '*.mat')
files.sort()
df_data=pd.DataFrame({})
for i, file in enumerate(files):
    print i
    particles = sio.loadmat(file)
    data=(zip(particles['particles'][0][0]['x'].flatten().tolist(),particles['particles'][0][0]['xp'].flatten().tolist(),particles['particles'][0][0]['y'].flatten().tolist(),particles['particles'][0][0]['yp'].flatten().tolist(),particles['particles'][0][0]['z'].flatten().tolist(),particles['particles'][0][0]['dE'].flatten().tolist(),particles['particles'][0][0]['ParticleIdNumber'].flatten().tolist(),particles['particles'][0][0]['macrosize'].flatten().tolist()))
    data=np.array(sorted(data, key=lambda x:x[-1]))
    df=pd.DataFrame(np.array(data)[:,:7],index=np.array(data).astype('int64')[:,6], columns=['x','xp','y','yp','z','dE','macrosize'])
    df_data=df_data.append(df)

n_turns = 1024
min_particle = 3
if min_particle%2:
    turns_half=(n_turns/2)-(min_particle+1)
else:
    turns_half=n_turns/2-(min_particle)
naff(data=np.array(df_data['x'].iloc[3::n_part]), turns=turns_half, nterms=1)

# Make an array of the tunes
tunes=[]
for i in xrange(min_particle,n_part):
    tunes.append(naff(data=np.array(df_data['x'].iloc[i::n_part]), turns=turns_half, nterms=1)[0][1])

# Ways to access particle data etc
n=3
#df_data['x'].iloc[n::n_part]               #Raw particle 3
max(df_data['x'].iloc[n::n_part])          #Maximum amplitude in x for particle n
#np.array(df_data['x'].iloc[n::n_part])     #Iterable
#turn=5
#np.array(df_data['x'].iloc[n::n_part])[turn]  #Index

# Find 'Maxmimum' amplitude
# one particle (of n_part) for each turn
# df_data['x'].iloc[:n_part:]
max_turn=1023
max_amps_y=[]
max_amps_x=[]

print df_data['x'].iloc[1::n_part]

    # Plot using maximum amplitude in sigma
betx0=12.79426135
alfx0=1.283306757 
gamx0 = (1+alfx0*alfx0)/betx0
en_x = (12.57e-6)/4
sig_x = np.sqrt(en_x * betx0)
const = np.sqrt(betx0 / gamx0)

for i in xrange(min_particle,n_part):

    # ~ max_amps_y.append(max(df_data['y'].iloc[i::n_part]))   
    # ~ max_amps_x.append(max(df_data['x'].iloc[i::n_part]))

    print np.array(df_data['x'].iloc[i:(i+1):n_part])[0]
    max_amps_x.append(const* np.array(df_data['x'].iloc[i::n_part])[0])

# ~ print max_amps_x


#xx=[]
#xx = np.array(df_data['x'].iloc[min_particle:n_part:])/(np.sqrt(betx0/gamx0))

# ~ xn = max_amps_x/sig_x
# ~ xn = max_amps_x*const
# ~ xn = max_amps_x

print len(xn)
print len(tunes)

fig, ax = plt.subplots()
plot_title = 'SIS18 X Distn Qx = ' + str(Qx) + '_' + case
ax.set(xlabel='x [sigma_x]', ylabel='Qx', title=plot_title)
ax.grid()
ax.scatter(xn,tunes, marker='.')
plot_name = 'SIS18_' + case + '_Qx.png'
fig.savefig(plot_name, dpi=600)

# Plot using maximum amplitude in sigma
bety0=13.47433765
alfy0=0.4264503497
gamy0 = (1+alfy0*alfy0)/bety0
en_y = (12.57e-6)/4
sig_y = np.sqrt(en_y * bety0)

# ~ yn = max_amps_y/sig_y

# ~ fig2, ax2 = plt.subplots()

# ~ plot_name = 'SIS18_' + case + 'Qy.png'
# ~ ax.set(xlabel='y [sigma_y]', ylabel='Qy', title=plot_title)
# ~ ax2.grid()
# ~ ax2.scatter(yn,tunes, marker='.')
# ~ fig2.savefig(plot_name, dpi=600)

# Save file
outfile_name = 'SIS18_' + case + '_Tunes.txt'
np.savetxt(outfile_name, zip(xn,tunes), fmt="%3.6e %3.6e")
print 'done'
