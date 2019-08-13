# Reads all .tfs ptc tables in folder (output from PTC-PyORBIT using: 
# readScriptPTC_noSTDOUT('PTC/twiss_script.ptc')
# and plots the tune evolution as a function of turn

import os
import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio 

data = dict()
keys = []

for filename in os.listdir('.'):
	if filename.endswith(".tfs"): 
		# print(os.path.join(directory, filename))
		file_1 = filename.split('_')[1]
		fileno = file_1.split('.')[0]
		keys.append(fileno)
		
		with open(filename) as f:
			first_line = f.readline()
			data[fileno] = (float(first_line.split()[2]), float(first_line.split()[3]))
			
# ~ print data

# Plot horizontal tunes
fig1 = plt.figure(facecolor='w', edgecolor='k')
ax1 = fig1.add_subplot(111)
ax1.set_title('Horizontal Tune');
ax1.set_ylabel(r'Q_x [-]')
ax1.set_xlabel('Turn [-]')
# ~ ax1.set_ylim(0.2094, 0.2096)
ax1.grid()

for i in sorted(keys):
	ax1.scatter(i, data[i][0], marker='.')

fig1.savefig('H_Tunes.png')
plt.close()


# Plot vertical tunes
fig1 = plt.figure(facecolor='w', edgecolor='k')
ax1 = fig1.add_subplot(111)
ax1.set_title('Vertical Tune');
ax1.set_ylabel(r'Q_y [-]')
ax1.set_xlabel('Turn [-]')
# ~ ax1.set_ylim(0.1, 0.1002)
ax1.grid()

for i in sorted(keys):
	ax1.scatter(i, data[i][1], marker='.')

fig1.savefig('V_Tunes.png')
plt.close()
