# Script to read multiple PTC twiss files and plot the closed orbit
# Expects a PTC twiss created with the following command:
# select, flag=ptc_twiss, column=name, s, betx, px, bety, py, disp3, disp3p, disp1, disp1p, x, y;
# 26.08.19 Haroon Rafique CERN BE-ABP-HSI 

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.cm as cm
import numpy as np
import os
import scipy.io as sio

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 12
plt.rcParams['legend.fontsize'] = 'small'
plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 0.5


ptc_extensions = ('.ptc')		# All outputs are .ptc files
ptc_iterators = []				# Integers (turn) used to iterate over files

# Search from current directory
print '\nFind PTC Twiss files\n'
for subdir, dirs, files in os.walk('PTC_Twiss'):
	# Iterate over all files
    for file in files:
		# Find files with required extension
		ext = os.path.splitext(file)[-1].lower()
		if ext in ptc_extensions:
			# Print full file path
			# ~ print (os.path.join(subdir, file))		# full path to file
			fileno = int(file.split('.')[0])	# use turn number as a key
			ptc_iterators.append(fileno)

ptc_data = dict()

# iterate over files (turns)
print '\nRead s, x ptc_data from files\n'
ptc_last_s = 0

for turn in sorted(ptc_iterators):
	s = []
	x = []

	# Open file
	infile = 'PTC_Twiss/' + str(turn) + '.ptc'
	fin = open(infile,'r').readlines()[90:]

	# Save s, x
	for l in fin:
		if ptc_last_s == float(l.split()[1]):
			pass
		else:
			ptc_last_s =float(l.split()[1])
			s.append(float(l.split()[1]))
			x.append(float(l.split()[-2]))

	# Add to dictionary as dict[turn] = (s, x)
	ptc_data[turn] = [s, x]
	ptc_last_s = 0
	

madx_extensions = ('.tfs')		# All outputs are .ptc files
madx_iterators = []				# Integers (turn) used to iterate over files

# Search from current directory
print '\nFind MADX Twiss files\n'
for subdir, dirs, files in os.walk('MADX_Twiss'):
	# Iterate over all files
    for file in files:
		# Find files with required extension
		ext = os.path.splitext(file)[-1].lower()
		if ext in madx_extensions:
			# Print full file path
			# ~ print (os.path.join(subdir, file))		# full path to file
			fileno = int(file.split('.')[0])	# use turn number as a key
			madx_iterators.append(fileno)

madx_data = dict()


# iterate over files (turns)
print '\nRead s, x madx_data from files\n'
last_s = 0

for turn in sorted(madx_iterators):	
	s = []
	x = []

	# Open file
	infile = 'MADX_Twiss/' + str(turn) + '.tfs'
	fin=open(infile,'r').readlines()[47:]

	# Save s, x
	for l in fin:
		if last_s == float(l.split()[2]):
			pass
		else:
			last_s =float(l.split()[2])
			s.append(float(l.split()[2]))
			x.append(float(l.split()[-2]))

	# Add to dictionary as dict[turn] = (s, x)
	madx_data[turn] = [s, x]
	last_s = 0


# Access turn 0, s column
# ptc_data[0][0]
# Access turn 25, x column, first value
# ~ print ptc_data[25][1][0]

print 'length of ptc_data = ', len(ptc_data[25][0])
print 'max x ptc_data = ', max(ptc_data[25][1])
print 'min x of ptc_data = ', min(ptc_data[25][1])


#-----------------------------------------------------------------------
#------------------------------PLOTTING---------------------------------
#-----------------------------------------------------------------------

case = '03_SBEND'

print '\n\tStart Plotting\n'

fig, ax1 = plt.subplots();
plt.title("PTC vs MADX Injection Closure Tune Swing");

# colormap 
colors = cm.rainbow(np.linspace(0, 1, len(ptc_iterators)))

ax1.set_xlabel("S [m]");
ax1.set_ylabel("x [m]");

c_it = int(0)
for turn in sorted(ptc_iterators):
	print 'Plotting PTC turn ', turn
	plt.plot(ptc_data[turn][0], ptc_data[turn][1], color=colors[c_it])
	# For each turn plot s,x in a new colour
	c_it += 1

c_it = int(0)
for turn in sorted(madx_iterators):
	print 'Plotting MADX turn ', turn
	plt.plot(madx_data[turn][0], madx_data[turn][1], color=colors[c_it])
	# For each turn plot s,x in a new colour
	c_it += 1

ax1.grid()

savename = 'PTC_cf_MADX_Closed_Orbit' + case + '.png'
plt.savefig(savename, dpi = 800);

print '\n\tPlot 1 done\n'


fig, ax1 = plt.subplots();
plt.title("PTC vs MADX Injection Closure Tune Swing");

# colormap 
colors = cm.rainbow(np.linspace(0, 1, len(ptc_iterators)))

ax1.set_xlim(470.0, 510.0)

ax1.set_xlabel("S [m]");
ax1.set_ylabel("x [m]");

test  = [1]

# ~ plt.plot(ptc_data[1][0], ptc_data[1][1], color=colors[c_it])

c_it = int(0)
for turn in sorted(ptc_iterators):
	print 'Plotting PTC turn ', turn
	plt.plot(ptc_data[turn][0], ptc_data[turn][1], color=colors[c_it])
	# For each turn plot s,x in a new colour
	c_it += 1

c_it = int(0)
for turn in sorted(madx_iterators):
	print 'Plotting MADX turn ', turn
	plt.plot(madx_data[turn][0], madx_data[turn][1], color=colors[c_it])
	# For each turn plot s,x in a new colour
	c_it += 1
ax1.grid()

savename = 'PTC_cf_MADX_Closed_Orbit' + case + '_zoom.png'
plt.savefig(savename, dpi = 800);

print '\n\tPlot 2 done\n'


fig, ax1 = plt.subplots();
plt.title("MADX Injection Closure Tune Swing");

# colormap 
colors = cm.rainbow(np.linspace(0, 1, len(ptc_iterators)))

ax1.set_xlim(470.0, 510.0)

ax1.set_xlabel("S [m]");
ax1.set_ylabel("x [m]");

c_it = int(0)
for turn in sorted(madx_iterators):
	print 'Plotting MADX turn ', turn
	plt.plot(madx_data[turn][0], madx_data[turn][1], color=colors[c_it])
	# For each turn plot s,x in a new colour
	c_it += 1

ax1.grid()

savename = 'MADX_Closed_Orbit' + case + '.png'
plt.savefig(savename, dpi = 800);

print '\n\tPlot 3 done\n'


fig, ax1 = plt.subplots();
plt.title("PTC Injection Closure Tune Swing");

# colormap 
colors = cm.rainbow(np.linspace(0, 1, len(ptc_iterators)))

ax1.set_xlim(470.0, 510.0)

ax1.set_xlabel("S [m]");
ax1.set_ylabel("x [m]");

test  = [1]

# ~ plt.plot(ptc_data[1][0], ptc_data[1][1], color=colors[c_it])

c_it = int(0)
for turn in sorted(ptc_iterators):
	print 'Plotting PTC turn ', turn
	plt.plot(ptc_data[turn][0], ptc_data[turn][1], color=colors[c_it])
	# For each turn plot s,x in a new colour
	c_it += 1

ax1.grid()

savename = 'PTC_Closed_Orbit' + case + '_zoom.png'
plt.savefig(savename, dpi = 800);

print '\n\tPlot 4 done\n'

