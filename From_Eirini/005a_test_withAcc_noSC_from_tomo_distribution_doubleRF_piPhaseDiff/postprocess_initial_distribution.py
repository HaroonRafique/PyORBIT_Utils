import numpy as np
import matplotlib.pyplot as plt
import h5py
from matplotlib.pyplot import text
import glob

#path = '/afs/cern.ch/work/e/eirini2/private/pyorbit_env/py-orbit/examples/CERN_PSB_spacecharge/Input/'
path = 'input/'

# Read txt file used for injection
#txtfile = np.loadtxt(path + 'INITIAL-6D.dat', skiprows=17, usecols=(0,1,2,3,4,5))
#txtfiles = glob.glob(path + 'mainbunchstart.dat')

fig = plt.figure(figsize=(13,8))

#for f in [txtfiles[0]]: #1st turn injection
#for f in txtfiles: #full distribution to be trackecd
txtfile = np.loadtxt(path + 'mainbunch_start.dat', skiprows=17, usecols=(0,1,2,3,4,5))
x = txtfile[:,0]
xp = txtfile[:,1]
y = txtfile[:,2]
yp = txtfile[:,3]
z = txtfile[:,4]
pz = txtfile[:,5]

# Plot
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
ax1.plot(x, xp,'b.')
ax2.plot(y, yp,'b.')
ax3.plot(z, pz,'b.')

ax1.set_title('Initial 6D distribution')
ax1.set_ylabel("x' (mrad)", fontsize=12)
ax1.set_xlabel('x (mm)', fontsize=12)
ax2.set_ylabel("y' (mrad)", fontsize=12)
ax2.set_xlabel('y (mm)', fontsize=12)
ax3.set_ylabel('dE (GeV)', fontsize=12)
ax3.set_xlabel('z (m)', fontsize=12)
plt.subplots_adjust(hspace=0.4)

#plt.show()
plt.savefig('initial_distribution.png')
