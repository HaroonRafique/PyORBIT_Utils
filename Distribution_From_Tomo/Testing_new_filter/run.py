'''
This script takes an output from the tomo (.dat format), and runs
the file through the executable tomo_vo.intelmp, thus generating a 
.mat file to be read by a PyORBIT distribution generator (written by
CERN BE-ABP-HSI members) which generates the longitudinal distribution
based on the measured tomo data.

This script is based on the work of:
Simon Albright (BE-RF)
Andrea Santamaria Garcia (BE-OP)
Eirini Koukovini-Platia (BE-ABP-HSC)

and is made available by Haroon Rafique (CERN BE-ABP-HSI) as is.
'''

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import re
from scipy.io import savemat
import sys

# 1.3 eVs
# ~ input_file_name='2017.11.28.12.09.05.117_tomo185.dat'

# 1.6 eVs
# ~ input_file_name='2017.11.28.11.35.25.636_tomo185.dat'

# 1.9 eVs
# ~ input_file_name='2017.11.24.17.17.20.458_tomo185.dat'

# 2.3 eVs
input_file_name='2017.11.24.18.16.50.800_tomo185.dat'

# 2.6 eVs
# ~ input_file_name='2017.11.24.16.07.17.081_tomo185.dat'

input_file_path=str('./'+input_file_name)

# Run the executable using the input file
result = subprocess.Popen(['./tomo_vo.intelmp'], stdin=open(input_file_path, 'r'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = result.communicate()
out = out.splitlines()

# ~ sys.exit()

# Read created image data
dat = np.loadtxt("image002.data")

# reshape from one column to a square
var = (int(np.sqrt(dat.shape[0])), int(np.sqrt(dat.shape[0])))
dat = dat.reshape(var).T

# formatter for output (out) binsizes
regexp = re.compile("\\d+\\.?\\d*E?[-+]?\\d*")

print(out[7])
print(out[9])

# output data looks like this:
# dtbin = 2.5000E-09
# dEbin = 9.6494E+04
# turn above into numbers in ns and GeV
# ~ dt = float(regexp.findall(out[7])[0])/1E-9
# ~ dE = float(regexp.findall(out[9])[0])/1E9

# Save in units of nanoseconds and mega electron volts
dt = float(regexp.findall(out[7])[0])/1E-9 # ns
dE = float(regexp.findall(out[9])[0])/1E6  # MeV
 
# make bins
tAxis = np.arange(dat.shape[0])*dt
EAxis = np.arange(dat.shape[0])*dE

# centre on (0,0) - not exact
tAxis -= np.mean(tAxis)
EAxis -= np.mean(EAxis)

# Manual shift
# ~ tAxis -= 13									# 1.3 eVs
# ~ EAxis -= .05								# 1.3 eVs

# ~ tAxis -= 7									# 1.6 eVs

# ~ tAxis -= 5									# 1.9 eVs

tAxis -= 5									# 2.3 eVs
EAxis -= 0.1								# 2.3 eVs

# ~ tAxis -= 1									# 2.6 eVs

for x,y in np.ndindex(dat.shape):
	if dat[x,y] < 0.00004:					# 1.3 eVs
		dat[x,y] = 0.0	
		
# This filters any pixel where surrounding pixels are 0
# may need to be modified if your phase space isn't a bunch but
# contains some sort of lines / filamentation that is wanted
for x in range (0, dat.shape[0], 1):
	for y in range( 0, dat.shape[1], 1):
		if x == 0 or y == 0 or x == (dat.shape[0]-1) or y == (dat.shape[1]-1) or dat[x,y] == 0.0:
			pass
		else: 
			if dat[x, y-1] == 0.0 and dat[x, y+1] == 0.0:
				print 'outlier removed at [',x, ',' ,y, ']'
				dat[x,y] = 0.0			

# 1.9 eV s outliers - used for check
# ~ dat[65, 3]  =  0.0
# ~ dat[67, 127]  =  0.0
# ~ dat[82, 112]  =  0.0
# ~ dat[85, 23]  =  0.0
# ~ dat[88, 105]  =  0.0
# ~ dat[95, 36]  =  0.0
# ~ dat[102, 49]  =  0.0
# ~ dat[103, 80]  =  0.0
# ~ dat[105, 72]  =  0.0
						
# plot to check
fig, ax = plt.subplots()
ax.pcolor(tAxis, EAxis, dat)
ax.set(xlabel='dt [ns]', ylabel='dE [MeV]', title='Longitudinal distribution from tomo data')
ax.grid(True)
plot_name = input_file_name + '.png'
fig.savefig(plot_name, dpi=600)

# Save file for PyORBIT - Format 1 (untested)
thefile = open("PyORBIT_Tomo_file.txt","w+")

# First line: Minimum dt, maximum dt, binsize, bins
thefile.write("%f\t%f\t%f\t%i" % (min(tAxis), max(tAxis), dt, len(tAxis)))

# Second line: Minimum dE, maximum dE, binsize, bins
thefile.write("\n%f\t%f\t%f\t%i" % (min(EAxis), max(EAxis), dE, len(EAxis)))

# Write density as grid
thefile.write("\n")
data = dat.tolist()

# ~ for i in data:
	# ~ thefile.write("%s" % (i))
for i in range (0, (var[0]-1), 1):
	for j in range (0, (var[1]-1), 1):
		thefile.write("%1.10f\t" % (data[i][j]))
	thefile.write("\n")
	
thefile.close()

# Save file for PyORBIT - Format 2 (tested)

# ~ data = np.ndarray(shape=(profilelength, profilelength), buffer=np.array(np.loadtxt("image002.data")))
# ~ data = np.transpose(data)

# Make time and energy vector
# ~ time_in_bins = np.arange(0, profilelength)
# ~ time_in_nsec = (time_in_bins - x) * dt * 1e9

# ~ energy_in_bins = np.arange(0, profilelength)
# ~ energy_in_MeV = (energy_in_bins - y) * dEbin * 1e-6

# ~ xx, yy = np.meshgrid(tAxis, EAxis)
# ~ plt.pcolormesh(xx, yy, dat)
# ~ plt.xlabel('Time (ns)')
# ~ plt.ylabel('Energy (MeV)')
# ~ plt.show()

data_dict = {'time_nsec': tAxis, 'energy_MeV': EAxis, 'density_array': dat}
savemat('PyORBIT_Tomo_file.mat', data_dict)
