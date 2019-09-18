import os

sbs = True

master_dir = os.getcwd()

sbs_locations = []

sbs_locations.append('/610_noSC/PyORBIT')
sbs_locations.append('/612_noSC/PyORBIT')
sbs_locations.append('/614_noSC/PyORBIT')
sbs_locations.append('/616_noSC/PyORBIT')
sbs_locations.append('/618_noSC/PyORBIT')
sbs_locations.append('/620_noSC/PyORBIT')
sbs_locations.append('/622_noSC/PyORBIT')
sbs_locations.append('/624_noSC/PyORBIT')

if sbs:
	for loc in sbs_locations:
		dir_ = master_dir + loc
		make_command = 'python Make_SLURM_submission_script.py'		
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)		
		os.system(submit_command)
