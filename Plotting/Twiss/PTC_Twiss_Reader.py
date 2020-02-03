import numpy as np
import os

# Function reads PTC TWISS, counts header lines to skip, automatically creates dictionary with keywords as keys
# Note NAME keyword is stored as string, all others stored as float

def Read_PTC_Twiss_Return_Dict(filename, verbose=True):
    # Dictionary for output
    d = dict()
    keywords = ''
    
    # First we open and count header lines
    fin0=open(filename,'r').readlines()
    headerlines = 0
    for l in fin0:
        headerlines = headerlines + 1
        if '* NAME' in l:
            keywords = l
            break
    headerlines = headerlines + 1
    
    if verbose: print '\nRead_PTC_Twiss_Return_Dict found Keywords: \n',keywords
    dict_keys = []
    for key in keywords.split():
        dict_keys.append(key)
    dict_keys.remove('*')
    if verbose: print '\nRead_PTC_Twiss_Return_Dict Dict Keys: \n',dict_keys
    
    for key in dict_keys:
        d[key]=[]
        
    if verbose: print '\nRead_PTC_Twiss_Return_Dict empty dictionary \n', d
    
    # Strip header
    fin1=open(filename,'r').readlines()[headerlines:]   
    
    for l in fin1:
        i = -1        
        for value in l.split():
            i = i+1
            if 'NAME' in dict_keys[i]:
                d[dict_keys[i]].append(str(value))
            else:
                d[dict_keys[i]].append(float(value))    
                
    return dict_keys, d
