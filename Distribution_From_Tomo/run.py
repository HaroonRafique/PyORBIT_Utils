import numpy as np
import matplotlib.pyplot as plt
import subprocess
import re
from scipy.io import savemat

input_file='2017.11.28.12.09.05.117_tomo185.dat'
full_input_file='./2017.11.28.12.09.05.117_tomo185.dat'

# Run the executable
result = subprocess.Popen(['./tomo_vo.intelmp'], stdin=open(full_input_file, 'r'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = result.communicate()
out = out.splitlines()
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
dt = float(regexp.findall(out[7])[0])/1E-9
dE = float(regexp.findall(out[9])[0])/1E9

# make bins
tAxis = np.arange(dat.shape[0])*dt
EAxis = np.arange(dat.shape[0])*dE

# centre on (0,0)
tAxis -= np.mean(tAxis)
EAxis -= np.mean(EAxis)

# plot
fig, ax = plt.subplots()
ax.pcolor(tAxis, EAxis, dat)
ax.set(xlabel='dt [ns]', ylabel='dE [GeV]', title='Longitudinal distribution from tomo data')
plot_name = input_file + '.png'
fig.savefig(plot_name, dpi=600)

# Save file for PyORBIT
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

# Mat file method

# ~ data = np.ndarray(shape=(profilelength, profilelength), buffer=np.array(np.loadtxt("image002.data")))
# ~ data = np.transpose(data)

# Make time and energy vector
# ~ time_in_bins = np.arange(0, profilelength)
# ~ time_in_nsec = (time_in_bins - x) * dt * 1e9

# ~ energy_in_bins = np.arange(0, profilelength)
# ~ energy_in_MeV = (energy_in_bins - y) * dEbin * 1e-6

yy, xx = np.meshgrid(EAxis, tAxis)
plt.pcolormesh(xx, yy, dat)
plt.xlabel('Time (ns)')
plt.ylabel('Energy (MeV)')
plt.show()

data_dict = {'time_nsec': tAxis, 'energy_MeV': EAxis, 'density_array': dat}
savemat('PyORBIT_Tomo_file.mat', data_dict)
