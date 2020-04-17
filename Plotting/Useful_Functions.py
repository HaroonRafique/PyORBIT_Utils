# Everything in Python 2.7 to be compatible with PTC-PyORBIT

import os
import glob
import imageio
import imageio
import pickle
import pandas as pd
import numpy as np
import PyNAFF as pnf
import scipy.io as sio 
import matplotlib.cm as cm
from math import log10, floor
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.optimize import curve_fit

plt.rcParams['figure.figsize'] = [5.0, 4.5]
plt.rcParams['figure.dpi'] = 200
plt.rcParams['savefig.dpi'] = 200

plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 14

plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

plt.rcParams['font.size'] = 10
plt.rcParams['legend.fontsize'] = 14

plt.rcParams['lines.linewidth'] = 1
plt.rcParams['lines.markersize'] = 5

########################################################################
# Relativistic Lorentz Factors (valid for protons)
# PSB Params:
# 50 MeV    gamma =  1.0533     beta = 0.314    SC_Tuneshift ~ 2.87 #obvs not
# 160 MeV   gamma =  1.1706     beta = 0.5198   SC_Tuneshift ~ 1.4 #obvs not
#
# PS Params:
# 1.4 GeV   gamma = 2.4921      beta = 0.91596  SC_Tuneshift ~ 0.176
# 2.0 GeV   gamma = 3.1316      beta = 0.9476   SC_Tuneshift ~ 0.108
#
# SC tuneshift proportional to 1/beta*gamma^2 gives an idea of trend
########################################################################
def LorentzGamma(E_tot, E_rest=938.27208816E6):
    return (E_tot / E_rest)
    
def LorentzGamma_from_beta(beta):
    return (1./np.sqrt(1.-beta**2))    

def LorentzBeta(Gamma):
    return np.sqrt( 1. - (1./gamma**2) )

def RelativisticMomentum(gamma, E_rest=938.27208816E6):
    return (gamma * E_rest * LorentzBeta(gamma))

def z_to_time(z, beta): 
    c = 299792458
    return z / (c * beta)
    
def E_from_gamma(gamma, E_rest=938.27208816E6):
    return (gamma*E_rest)

########################################################################
# Delta P over P from dE or vice versa
# dp_ov_p = dE_ov_E/beta^2
########################################################################
def dpp_from_dE(dE, E, beta):
    return (dE / (E * beta**2))
    
def dE_from_dpp(dpp, E, beta):
    return (dpp * E * beta**2)

########################################################################
# Check if file exists
########################################################################
def check_if_file_exists(name):
    ret_val = False
    if os.path.isfile(name):
        print name, ' already exists'
        ret_val = True
    return ret_val

########################################################################
# GIF From PNG files
########################################################################
def GIF_from_PNG(input_folder):
    input_filenames = []
    os.chdir(input_folder)

    for file in glob.glob('*.png'):
        print 'Found file: ', file
        print 'Found file: ', file.split('/')[-1]
        input_filenames.append(file.split('/')[-1])
        
    print 'Creating GIF'
    images = []
    for filename in sorted(input_filenames):
        images.append(imageio.imread(filename))
    gif_savename = input_filenames[0][:10] + '.gif'
    imageio.mimsave(gif_savename, images)
    print 'GIF Created'
    return 1

########################################################################
# Sequence centred on 0, evenly distributed 
########################################################################
def seq_even_about_start(n_vals, start, stop):
    n_mp = n_vals
    interval = 2*(stop-start)/(n_mp-1) 

    print('seq_even_about_start::interval = ', interval)

    positive = np.arange(start, stop+interval, interval)
    negative = np.arange((-1*stop), start, interval)

    positions = np.concatenate((negative, positive), axis=None)
    
    return positions

########################################################################
# Sequence evenly distributed between start and stop 
########################################################################
def seq_start_to_end(n_vals, start, stop):
    n_mp = n_vals
    interval = (stop-start)/(n_mp-1) 

    print('seq_start_to_end::interval = ', interval)

    positions = np.arange(start, stop+interval, interval)
    
    return positions

########################################################################
# Sequence evenly distributed between start and stop 
# With checks to ensure the numbe of values is not exceeded due to 
# rounding errors etc
########################################################################
def seq_start_to_end(n_vals, start, stop):
    n_mp = n_vals
    interval = (stop-start)/(n_mp-1)

    print('seq_start_to_end::interval = ', interval)

    positions = np.arange(start, stop+interval, interval)
    
    # First check - try rounding
    if len(positions) != n_vals:
        for i in sorted(range(10), reverse=True):
            interval = round_sig((stop-start)/(n_mp-1),5) 
            positions = np.arange(start, stop+interval, interval)
            
            if len(positions) == n_vals: break
        print('seq_start_to_end::WARNING: output sequence length != input, rounding leads to ', len(positions))
    
    # Second check - 
    if len(positions) != n_vals:
        cut = (stop-start)/((n_mp-1)*1E4)
        while len(positions) != n_vals:
            # If our interval is too large
            if len(positions) < n_vals:                
                interval = (stop-start)/(n_mp-1) - cut
                positions = np.arange(start, stop+interval, interval)                
            else:                 
                interval = (stop-start)/(n_mp-1) + cut
                positions = np.arange(start, stop+interval, interval)
            
        print('seq_start_to_end::WARNING: output sequence length != input, cutting leads to ', len(positions))
      
    return positions

########################################################################
# Round number to n significant figures
########################################################################
def round_sig(x, sig=3):
    return round(x, sig-int(floor(log10(abs(x))))-1)

########################################################################
# Replace points in a string with the letter p - useful for filenames
########################################################################
def replace_point_with_p(input_str):
    return input_str.replace(".", "p")

# Note that size of programs is (n_sections, n_turns+1)
print('Momentum : %.5e eV/c' %(ring.momentum[0,0]))
print('Kinetic energy : %.5e eV' %(ring.kin_energy[0,0]))
print('Total energy : %.5e eV' %(ring.energy[0,0]))
print('beta : %.5f' %(ring.beta[0,0]))
print('gamma : %.5f' %(ring.gamma[0,0]))
print('Revolution period : %.5e s' %(ring.t_rev[0]))

########################################################################
# Read PTC Twiss and return dictionary of columns/values
########################################################################
def Read_PTC_Twiss_Return_Dict(filename, verbose=True):
    # Dictionary for output
    d = dict()
    d['HEADER_FILENAME'] = filename
    keywords = ''
    
    # First we open and count header lines
    fin0=open(filename,'r').readlines()
    headerlines = 0
    for l in fin0:
        # Store each header line
        headerlines = headerlines + 1
        # Stop if we find the line starting '* NAME'
        if '* NAME' in l:
            keywords = l
            break
        # Store the headers as d['HEADER_<name>'] = <value>
        else:
            #try:
            #    d[str('HEADER_'+l.split()[1])]=[float(l.split()[-1])]     
            #except ValueError:
            #    d[str('HEADER_'+l.split()[1])]=[str(l.split()[-1])]   
            if '"' in l:
                d[str('HEADER_'+l.split()[1])]=[str(l.split('"')[1])]
            else:
                d[str('HEADER_'+l.split()[1])]=[float(l.split()[-1])]                 
    headerlines = headerlines + 1    
    
    if verbose: print '\nRead_PTC_Twiss_Return_Dict found Keywords: \n',keywords
    
    # Make a list of column keywords to return (as an aid to iterating)
    dict_keys = []
    for key in keywords.split():
        dict_keys.append(key)
    dict_keys.remove('*')
    
    if verbose: print '\nRead_PTC_Twiss_Return_Dict Dict Keys: \n',dict_keys
    
    # Initialise empty dictionary entries for column keywords 
    for key in dict_keys:
        d[key]=[]
        
    if verbose: print '\nRead_PTC_Twiss_Return_Dict header only dictionary \n', d
    
    # Strip header
    fin1=open(filename,'r').readlines()[headerlines:]   
    
    # Populate the dictionary line by line
    for l in fin1:
        i = -1        
        for value in l.split():
            i = i+1
            if 'NAME' in dict_keys[i]:
                d[dict_keys[i]].append(str(value))
            else:
                d[dict_keys[i]].append(float(value))    
                
    # Return list of column keywords 'dict_keys', and dictionary 'd'
    return dict_keys, d
