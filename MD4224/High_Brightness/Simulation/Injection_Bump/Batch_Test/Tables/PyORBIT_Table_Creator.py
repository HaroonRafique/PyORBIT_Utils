# PyORBIT Table Creator
# Creates a .dat table that is read by PTC to set magnet strengths as a function of time
# Currently works only for single multipoles (pure dipole, quad, sextupole ...)
#
# Haroon Rafique CERN BE-ABP-HSI 28.06.19
#
import numpy as np
import os
from math import log10, floor
from scipy.misc import factorial

# From Hannes Bartosik
def write_PTCtable(filename, multipole_orders, time, normal_components, skew_components):
	multipole_orders = np.atleast_1d(multipole_orders)
	factors = 1./factorial(multipole_orders-1) # the factorial factor is needed to be consistent with MADX
	normal_components = (factors.T * np.atleast_2d(normal_components).T)
	skew_components   = (factors.T * np.atleast_2d(skew_components).T)
	arr = np.empty((normal_components.shape[0], 1+normal_components.shape[1]*2), dtype=normal_components.dtype)
	arr[:,0] = time
	arr[:,1::2] = normal_components
	arr[:,2::2] = skew_components
	n_lines = len(time)
	n_multipoles = len(multipole_orders) # number of multipole orders to be changed
	with open(filename, 'w') as fid:
		fid.write('%d  1  %d\n'%(n_lines, n_multipoles))
		fid.write(' '.join(map(lambda i: '%d'%i, multipole_orders)) + '\n')
		for j in xrange(n_lines):
			fid.write('\t'.join(map(lambda i: '%+1.11f'%i, arr[j, :]))+'\n')
	return

def round_sig(x, sig=5):
	return round(x, sig-int(floor(log10(abs(x))))-1)

# For each element, create a PTC table - Note for some reason this doesn't work - use above function
def Create_PTC_Table(name, multipole_order, time, normal, skew):

	f = open(name, 'w')
	
	n_lines = len(time)
	
	f.write('%i  1  %i\n' % (n_lines, multipole_order))
	f.write('%i\n' % (multipole_order))
	
	for i in xrange(len(time)):
		f.write('%+1.11f\t%+1.11f\t%+1.11f\n' % (time[i], normal[i], skew[i]))	
	
	return

# Read TFS table to obtain our dipole kick or quadrupole gradient
# We ignore the time column
def Read_TFS_Return_Data(file_in):
	fi = open(file_in, 'r')
	contents = fi.readlines()

	data = []
	for l in contents:
		if ('@' in l) or ('$' in l) or ('*' in l):
			pass
		else:
			data.append(float(l.split()[1]))

	return data
	

# Function takes the data, creates the correct timing for each value in
# seconds, then appends the required number of intervals with zeroes
def Create_Timing(ramp_stop_time, simulation_stop_time, data):
	data_2 = data
	
	# create sequence for time
	d_len = len(data)
	time = np.linspace(0, ramp_stop_time, d_len)
	
	# Calculate interval to complete data until the end of the simulation
	interval = ramp_stop_time / (d_len-1)
	
	# Append zeroes (bump is closed)
	steps = int((simulation_stop_time - ramp_stop_time)	/ interval) + 5
	
	for i in xrange(steps):
		if i is 0:
			pass
		else:
			time = np.append(time, (ramp_stop_time + (i*interval)))
			data_2.append(0.0)
				
	return time, data_2

# Simple Test
# ~ Create_PTC_Table('TEST', 2, [0,1,2], [11.32161, 12.1321564, 13.555555855555555], [0,0,0])

# Create the input files for the closure (2nd half) of the injection bump

# Table time is in seconds
# 1 turn = 2.287E-6 seconds
# We want a full bump of 1E-3 seconds, or a half bump of 5E-4 seconds
# 2200 turns = 5.0314E-3 s
# Bump on for 5E-4 seconds
# zeroes from 5E-4 - 5.0314E-3 s

print '\n Reading ../MADX/BSEXT40.tfs'
B_40 = Read_TFS_Return_Data('../MADX/BSEXT40.tfs')
print '\n Create timing for ../MADX/BSEXT40.tfs'
B_40_final = Create_Timing(5E-3, 5.0314E-2, B_40)
print '\n Create table ../Tables/BSEXT40.dat'
# ~ Create_PTC_Table('../Tables/BSEXT40.dat', 3, B_40_final[0], B_40_final[1], np.zeros(len(B_40_final[0])))
write_PTCtable('../Tables/BSEXT40.dat',  3, B_40_final[0], B_40_final[1], np.zeros(len(B_40_final[0])))

print '\n Reading ../MADX/BSEXT42.tfs'
B_42 = Read_TFS_Return_Data('../MADX/BSEXT42.tfs')
print '\n Create timing for ../MADX/BSEXT42.tfs'
B_42_final = Create_Timing(5E-3, 5.0314E-2, B_42)
print '\n Create table ../Tables/BSEXT42.dat'
# ~ Create_PTC_Table('../Tables/BSEXT42.dat', 3, B_42_final[0], B_42_final[1], np.zeros(len(B_42_final[0])))
write_PTCtable('../Tables/BSEXT42.dat',  3, B_42_final[0], B_42_final[1], np.zeros(len(B_42_final[0])))

print '\n Reading ../MADX/BSEXT43.tfs'
B_43 = Read_TFS_Return_Data('../MADX/BSEXT43.tfs')
print '\n Create timing for ../MADX/BSEXT43.tfs'
B_43_final = Create_Timing(5E-3, 5.0314E-2, B_43)
print '\n Create table ../Tables/BSEXT43.dat'
# ~ Create_PTC_Table('../Tables/BSEXT43.dat', 3, B_43_final[0], B_43_final[1], np.zeros(len(B_43_final[0])))
write_PTCtable('../Tables/BSEXT43.dat',  3, B_43_final[0], B_43_final[1], np.zeros(len(B_43_final[0])))

print '\n Reading ../MADX/BSEXT44.tfs'
B_44 = Read_TFS_Return_Data('../MADX/BSEXT44.tfs')
print '\n Create timing for ../MADX/BSEXT44.tfs'
B_44_final = Create_Timing(5E-3, 5.0314E-2, B_44)
print '\n Create table ../Tables/BSEXT44.dat'
# ~ Create_PTC_Table('../Tables/BSEXT44.dat', 3, B_44_final[0], B_44_final[1], np.zeros(len(B_44_final[0])))
write_PTCtable('../Tables/BSEXT44.dat',  3, B_44_final[0], B_44_final[1], np.zeros(len(B_44_final[0])))

print '\n Reading ../MADX/PI.BSM40.1.tfs'
BSM40 = Read_TFS_Return_Data('../MADX/PI.BSM40.1.tfs')
print '\n Create timing for ../MADX/PI.BSM40.1.tfs'
BSM40_final = Create_Timing(5E-3, 5.0314E-2, BSM40)
print '\n Create table ../Tables/BSM40.da'
# ~ Create_PTC_Table('../Tables/BSM40.dat', 2, BSM40_final[0], BSM40_final[1], np.zeros(len(BSM40_final[0])))
write_PTCtable('../Tables/BSM40.dat',  2, BSM40_final[0], BSM40_final[1], np.zeros(len(BSM40_final[0])))































