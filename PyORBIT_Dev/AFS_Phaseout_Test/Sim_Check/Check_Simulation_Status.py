#!/usr/bin/python
import glob
import os, os.path
import numpy as np
import scipy.io as sio 
from simulation_parameters import parameters as p

print '\nCheck_Simulation_Status: Python script to check if a PyORBIT simulation completes the expected number of turns'

def add_input_file(dd, filename, label, verbose = False):	
	exists = os.path.isfile(filename)
	if exists:
		f = filename
		p = dict()
		sio.loadmat(f, mdict=p)
		dd[label] = p	
		if verbose: print '\n\tadd_input_file::Added output data from ', filename, '\t dictionary key: ', label
	else:
		if verbose: print '\tadd_input_file::File ', filename, 'not found'		
	
	return dd
	
def check_last_turn(dd, key, expected, verbose = True):
	complete = False
	
	if verbose: print '\n\tTurns completed ', (dd[key]['turn'][0][-1]+1), '.\n\tTurns expected ', expected
	
	# Note python indices start at 0 so our expected number of turns will be one less
	if dd[key]['turn'][0][-1] == (expected-1):
		complete = True
	return complete	

def check_bunch_output_files(verbose = True):
	complete = False
	expected_files = len(p['turns_print'])
	matCounter = len(glob.glob1('./bunch_output/',"*.mat"))
	
	if verbose: print '\n\tBunch dumped ', matCounter ,' times, expected ', expected_files ,' files'
	
	if(matCounter == expected_files):
		complete = True
	return complete	

# Create dd dictionary
dd = dict()
key = 'Test'
dd = add_input_file(dd, './output/output.mat', key)

expected_turns = p['turns_max']

bunch_output = check_bunch_output_files()
tracking = check_last_turn(dd, key, expected_turns)

finished = False
if bunch_output and tracking: finished = True

if finished:
	print '\n\tPyORBIT simulation completed successfully'
else:
	print '\n\tPyORBIT simulation NOT COMPLETE'
	
