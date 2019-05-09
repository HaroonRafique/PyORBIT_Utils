import os

sbs = True

master_dir = os.getcwd()

sbs_locations = []

sbs_locations.append('/32')
sbs_locations.append('/64')
sbs_locations.append('/128')
sbs_locations.append('/256')

if sbs:
	for loc in sbs_locations:
		dir_ = master_dir + loc
		make_command = 'python Make_SLURM_submission_script.py'		
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)		
		os.system(submit_command)
