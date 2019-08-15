import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

plt.rcParams['figure.figsize'] = [8.0, 6.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

plt.rcParams['font.size'] = 6
plt.rcParams['legend.fontsize'] = 'small'
plt.rcParams['figure.titlesize'] = 'medium'

plt.rcParams['lines.linewidth'] = 0.5

def FileToDict(f):
	results=dict()

	# Open file and skip header line
	fin = open(f,'r').readlines()[1:]

	# Iterate over lines and add 4-value array to dict using turn as key
	for l in fin:
		results[int(l.split()[0])] = [float(l.split()[1]), float(l.split()[2]), float(l.split()[3]), float(l.split()[4])]

	return results

inputs = ['00_original_method/All_Twiss/Orbit_Extrema.dat', '01_multipole/All_Twiss/Orbit_Extrema.dat', '02_quadrupole/All_Twiss/Orbit_Extrema.dat', '03_sbend/All_Twiss/Orbit_Extrema.dat']

dicts=[]

for i in inputs:
	dicts.append(FileToDict(i))
	print 'File ', i, ' added, Turns = ', len(dicts[-1])



# Access like dicts[method][turn][n]
# n = 0 : x_min
# n = 1 : x_max
# n = 2 : y_min
# n = 3 : y_max
# For example: method 01_multipole turn 40 y_max: dicts[1][40][3]
# ~ print dicts[1][40][3]

fig, ax1 = plt.subplots();

plt.title("PS Injection Bump Methods Comparison: Minimum and Maximum Horizontal Closed Orbit");

for i in xrange(len(dicts[0])):
	ax1.scatter(i, dicts[0][i][0], color='b', marker='.');
	ax1.scatter(i, dicts[0][i][1], color='b', marker='.');

for i in xrange(len(dicts[1])):
	ax1.scatter(i, dicts[1][i][0], color='k', marker='.');
	ax1.scatter(i, dicts[1][i][1], color='k', marker='.');

for i in xrange(len(dicts[2])):
	ax1.scatter(i, dicts[2][i][0], color='r', marker='.');
	ax1.scatter(i, dicts[2][i][1], color='r', marker='.');

for i in xrange(len(dicts[3])):
	ax1.scatter(i, dicts[3][i][0], color='m', marker='.');
	ax1.scatter(i, dicts[3][i][1], color='m', marker='.');

ax1.set_xlabel("Turn [-]");
ax1.set_ylabel("x [m]");

custom_lines = [Line2D([0], [0], color='b', lw=4),
                Line2D([0], [0], color='k', lw=4),
                Line2D([0], [0], color='r', lw=4),
                Line2D([0], [0], color='m', lw=4)]

ax1.legend(custom_lines, ['Split Kicker + Multipole', 'Multipole', 'Quadrupole as Errors', 'Sbend as Errors'])

plt.savefig('Orbit_Extrema_Comparison_H.png', dpi = 800);

fig, ax2 = plt.subplots();

plt.title("PS Injection Bump Methods Comparison: Minimum and Maximum Vertical Closed Orbit");

for i in xrange(len(dicts[0])):
	ax2.scatter(i, dicts[0][i][2], color='b', marker='.');
	ax2.scatter(i, dicts[0][i][3], color='b', marker='.');

for i in xrange(len(dicts[1])):
	ax2.scatter(i, dicts[1][i][2], color='k', marker='.');
	ax2.scatter(i, dicts[1][i][3], color='k', marker='.');

for i in xrange(len(dicts[2])):
	ax2.scatter(i, dicts[2][i][2], color='r', marker='.');
	ax2.scatter(i, dicts[2][i][3], color='r', marker='.');

for i in xrange(len(dicts[3])):
	ax2.scatter(i, dicts[3][i][2], color='m', marker='.');
	ax2.scatter(i, dicts[3][i][3], color='m', marker='.');

ax2.set_xlabel("Turn [-]");
ax2.set_ylabel("x [m]");

custom_lines = [Line2D([0], [0], color='b', lw=4),
                Line2D([0], [0], color='k', lw=4),
                Line2D([0], [0], color='r', lw=4),
                Line2D([0], [0], color='m', lw=4)]

ax2.legend(custom_lines, ['Split Kicker + Multipole', 'Multipole', 'Quadrupole as Errors', 'Sbend as Errors'])

plt.savefig('Orbit_Extrema_Comparison_V.png', dpi = 800);
