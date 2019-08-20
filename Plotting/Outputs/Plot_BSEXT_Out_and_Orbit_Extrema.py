import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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

def BSEXT_Out_To_Dict(bo, directory, label, max_turn = 500):
	# Check file exists
	fpath = str(directory + '/MADX/BSEXT_Out.tfs')
	if os.path.isfile(fpath) and os.path.getsize(fpath) > 3:
		results=dict()

		# Need a sequence for turns
		num_lines = sum(1 for line in open(fpath)) - 8
		# ~ print 'Lines = ', num_lines

		turn_seq = np.linspace(start = 1, stop = max_turn, num = num_lines)
		# ~ print turn_seq

		# Open file, ignore header
		fin = open(fpath,'r').readlines()[8:]

		# Iterate over lines in file and fill dictionary
		i = 0
		for l in fin:
			results[int(turn_seq[i])] = [float(l.split()[6]), float(l.split()[7]), float(l.split()[8]), float(l.split()[9]), float(l.split()[10]), float(l.split()[11])]
			i += 1

	else:
		print 'File ', fpath, ' not found or empty, exiting'
		exit(0)

	bo[label] = results

	return bo

def Orbit_Extrema_to_Dict(oe, directory, label):
	# Check file exists
	fpath = str(directory + '/All_Twiss/Orbit_Extrema.dat')
	if os.path.isfile(fpath) and os.path.getsize(fpath) > 3:
		results=dict()

		# Open file and skip header line
		fin = open(fpath,'r').readlines()[1:]

		# Iterate over lines and add 4-value array to dict using turn as key
		for l in fin:
			results[int(l.split()[0])] = [float(l.split()[1]), float(l.split()[2]), float(l.split()[3]), float(l.split()[4])]

	else:
		print 'File ', fpath, ' not found or empty, exiting'
		exit(0)

	oe[label] = results

	return oe

def add_input_file(po, directory, label):
	# Check file exists
	fpath = str(directory + '/output/output.mat')
	if os.path.isfile(fpath) and os.path.getsize(fpath) > 3:
		p=dict()
		sio.loadmat(fpath, mdict=p)
		po[label] = p

	else:
		print 'File ', fpath, ' not found or empty, exiting'
		exit(0)

	print '\tAdded output data from ', fpath, '\t dictionary key: ', label
	return po

#---------------------------------------------------------------------
#######					No Space Charge							######
#---------------------------------------------------------------------

inputs = ['00_fullbunch', '01_fullbunch', '02_fullbunch', '03_fullbunch']
labels = ['Split_HKICKER', 'MULTIPOLE', 'QUADRUPOLE_with_errors', 'SBEND_with_errors']

####################
# READ INPUT FILES #
####################

OE = dict()	# Orbit extrema
BO = dict()	# BSEXT out
PO = dict()	# PyORBIT output

for i in range(4):
	BO = BSEXT_Out_To_Dict(BO, inputs[i], labels[i])
	OE = Orbit_Extrema_to_Dict(OE, inputs[i], labels[i])
	PO = add_input_file(PO, inputs[i], labels[i])

#########
# PLOTS #
#########

# Compare maximum orbits
print '\n\tPlotting XMAX'
for j in range(4):
	fig, ax1 = plt.subplots();
	plt.title("PS Injection Bump Methods Comparison: Maximum Horizontal Closed Orbit");

	# Plot orbit extrema
	for i in sorted(BO[labels[j]].keys()):
		ax1.scatter(i, BO[labels[j]][i][0], color='r', marker='x');
	for i in sorted(BO[labels[j]].keys()):
		ax1.scatter(i, BO[labels[j]][i][1], color='g', marker='+');
	for i in xrange(len(OE[labels[j]])):
		ax1.scatter(i, OE[labels[j]][i][1], color='b', marker='.');
	ax1.set_xlabel("Turn [-]");
	ax1.set_ylabel(r"x$_{max}$ [m]");
	
	custom_lines = [Line2D([0], [0], color='r', lw=4),
					Line2D([0], [0], color='g', lw=4),
					Line2D([0], [0], color='b', lw=4)]

	ax1.legend(custom_lines, ['MAD-X', 'PTC', 'PyORBIT'])
	savename = inputs[j] + '_Xmax.png'
	plt.savefig(savename, dpi = 800);

# Plot tunes
print '\n\tPlotting Qx'
for j in range(4):
	fig, ax1 = plt.subplots();
	plt.title("PS Injection Bump Methods Comparison: Horizontal Tune Swing");

	for i in sorted(BO[labels[j]].keys()):
		ax1.scatter(i, BO[labels[j]][i][2]-6, color='r', marker='x');

	for i in sorted(BO[labels[j]].keys()):
		ax1.scatter(i, BO[labels[j]][i][4], color='g', marker='+');

	ax1.plot(PO[labels[j]]['turn'][0], PO[labels[j]]['Qx'][0], label='PyORBIT', color='b');

	ax1.set_ylim(0.2, 0.22)

	ax1.set_xlabel("Turn [-]");
	ax1.set_ylabel(r"Q$_{x}$ [-]");

	custom_lines = [Line2D([0], [0], color='r', lw=4),
					Line2D([0], [0], color='g', lw=4),
					Line2D([0], [0], color='b', lw=4)]

	ax1.legend(custom_lines, ['MAD-X', 'PTC', 'PyORBIT'])

	savename = inputs[j] + '_Qx.png'
	plt.savefig(savename, dpi = 800);

# Plot tunes
print '\n\tPlotting Qy'
for j in range(4):
	fig, ax1 = plt.subplots();
	plt.title("PS Injection Bump Methods Comparison: Vertical Tune Swing");

	for i in sorted(BO[labels[j]].keys()):
		ax1.scatter(i, BO[labels[j]][i][3]-6, color='r', marker='x');

	for i in sorted(BO[labels[j]].keys()):
		ax1.scatter(i, BO[labels[j]][i][5], color='g', marker='+');

	ax1.plot(PO[labels[j]]['turn'][0], PO[labels[j]]['Qy'][0], label='PyORBIT', color='b');

	ax1.set_ylim(0.09, 0.11)

	ax1.set_xlabel("Turn [-]");
	ax1.set_ylabel(r"Q$_{y}$ [-]");

	custom_lines = [Line2D([0], [0], color='r', lw=4),
					Line2D([0], [0], color='g', lw=4),
					Line2D([0], [0], color='b', lw=4)]

	ax1.legend(custom_lines, ['MAD-X', 'PTC', 'PyORBIT'])
	savename = inputs[j] + '_Qy.png'
	plt.savefig(savename, dpi = 800);


#---------------------------------------------------------------------
#######					Space Charge							######
#---------------------------------------------------------------------

# ~ inputss = ['00_fullbunch_sc', '01_fullbunch_sc', '02_fullbunch_sc', '03_fullbunch_sc']
# ~ labelss = ['Split_HKICKER_SC', 'MULTIPOLE_SC', 'QUADRUPOLE_with_errors_SC', 'SBEND_with_errors_SC']

# ~ ####################
# ~ # READ INPUT FILES #
# ~ ####################

# ~ OEs = dict()	# Orbit extrema
# ~ BOs = dict()	# BSEXT out
# ~ POs = dict()	# PyORBIT output

# ~ for i in range(4):
	# ~ BOs = BSEXT_Out_To_Dict(BOs, inputss[i], labelss[i])
	# ~ OEs = Orbit_Extrema_to_Dict(OEs, inputss[i], labelss[i])
	# ~ POs = add_input_file(POs, inputss[i], labelss[i])

# ~ #########
# ~ # PLOTS #
# ~ #########

# ~ # Compare maximum orbits
# ~ print 'Plotting XMAX SC'
# ~ for j in range(4):
	# ~ fig, ax1 = plt.subplots();
	# ~ plt.title("PS Injection Bump Methods Comparison: Maximum Horizontal Closed Orbit");

	# ~ # Plot orbit extrema
	# ~ for i in sorted(BOs[labelss[j]].keys()):
		# ~ ax1.scatter(i, BOs[labelss[j]][i][0], color='r', marker='x');
	# ~ for i in sorted(BOs[labelss[j]].keys()):
		# ~ ax1.scatter(i, BOs[labelss[j]][i][1], color='g', marker='+');
	# ~ for i in xrange(len(OEs[labelss[j]])):
		# ~ ax1.scatter(i, OEs[labelss[j]][i][1], color='b', marker='.');
	# ~ ax1.set_xlabel("Turn [-]");
	# ~ ax1.set_ylabel(r"x$_{max}$ [m]");
	
	# ~ custom_lines = [Line2D([0], [0], color='r', lw=4),
					# ~ Line2D([0], [0], color='g', lw=4),
					# ~ Line2D([0], [0], color='b', lw=4)]

	# ~ ax1.legend(custom_lines, ['MAD-X', 'PTC', 'PyORBIT'])
	# ~ savename = inputss[j] + '_Xmax_SC.png'
	# ~ plt.savefig(savename, dpi = 800);
