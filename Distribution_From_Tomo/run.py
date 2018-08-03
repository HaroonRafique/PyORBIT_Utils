import numpy as np
import matplotlib.pyplot as plt
import subprocess
import re

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
# ~ # First line dt bins
# ~ for item in tAxis:
	# ~ thefile.write("%f\t" % item)
  
# ~ thefile.write("\n")
# ~ # Second line dE bins
# ~ for item in EAxis:
	# ~ thefile.write("%f\t" % item)
	
	
# Third line 

