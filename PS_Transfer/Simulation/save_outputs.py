import os
import fnmatch
import datetime
from shutil import copyfile

# Function to check existence of a folder and create if nonexistent
def check_master_dir(directory_name):
	if os.path.isdir(directory_name):
		print '\n\tWARNING: directory', directory_name,' already exists. This function will overwrite any output files in this directory.'
	else:
		os.mkdir(directory_name)
	return

def check_and_make_directory(directory_name, verbose = False):
	if os.path.isdir(directory_name):
		if verbose: print '\n\tWARNING: in function check_and_make_directory: directory', directory_name,' already exists.'
	else:
		os.mkdir(directory_name)
	return

# Function to find a pattern in directories within this one
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

pwd = os.getcwd()  
print ("The current working directory is %s" % pwd)  

search_file = 'output.mat'

output_files = find(search_file, './')

print 'Found ', len(output_files), ' output.mat files'

# Make folder to hold data
now = datetime.datetime.now()
now_folder_ = now.strftime("%B_%d_%Y")
now_folder = 'Output_backup_' + now_folder_

check_and_make_directory(now_folder)

verbose = False

# Iterate over files, make folders, copy
for f in output_files:	
	
	# Make folder structure in now_folder
	os.chdir(now_folder)
	possible_folders = []
	
	# number of folders in relative path
	num_folders = len(f.split('/'))
	if verbose: print '\t number of folders to be created in ', f, ' = ', num_folders
	
	# Make a list of paths to these folders
	folder_list = []	
	folder_list.append(f.split('/')[0])
	for i in xrange(num_folders-2):
		folder_list.append(folder_list[i] + '/' + f.split('/')[i+1])
	
	# Remove first folder from list ('.')
	del folder_list[0]
	
	# Iterate over folder list, check, and make directories
	for folder in folder_list:
		check_and_make_directory(folder)
	
	# Go back to Simulation folder
	os.chdir(pwd)
	
	# Copy files
	# ~ destination = now_folder + f[1:-(len(search_file))]
	destination = now_folder + f[1:]
	if verbose: print 'file: ', f, '\ndestination: ', destination
	copyfile(f, destination)
	
