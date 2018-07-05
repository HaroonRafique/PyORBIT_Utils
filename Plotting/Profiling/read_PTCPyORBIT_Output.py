# Reads the output generated by PTC-PyORBIT when using Hannes Bartosik's
# output dictionary (outputs the time of each turn)

import matplotlib.pyplot as plt
# ~ from matplotlib.patches import Patch
# ~ from matplotlib.ticker import FormatStrFormatter
# ~ from matplotlib.lines import Line2D
import numpy as np
# ~ import scipy.io as sio 
import os
import sys

# Parse arguments from command line
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename",
					help="Input filename, this is the raw output from a PTC-PyORBIT run, note that Hannes Bartosik's output dictionary is required, as well as a turn by turn output.update()", metavar="FILE")

parser.add_argument("-c", "--cores", dest="cores", metavar="CORES", type=int,
					help="Number of CPU cores used for simulation, must be an integer")

parser.add_argument("-n", "--nodes", dest="nodes", metavar="NODES", type=int,
					help="Number of nodes used for simulation, must be an integer")
					
parser.add_argument("-t", "--threads", dest="total_threads", metavar="THREADS", type=int,
					help="Number of threads used for simulation, must be an integer")
					
parser.add_argument("-tpn", "--threadspernode", dest="threads_per_node", metavar="THREADSPERNODE", type=int,
					help="Number of threads per node used for simulation, must be an integer")

args = parser.parse_args()

if args.cores:
	print 'Cores = ', cores
if args.nodes:
	print 'nodes = ', nodes
if args.cores:
	print 'total_threads = ', total_threads
if args.cores:
	print 'threads_per_node = ', threads_per_node

# Open file and find the line 'turn intensity n_mp etc'
with open(filename) as fp:
    for line in fp:

# Calculate total time and time per turn; first, last, average etc

