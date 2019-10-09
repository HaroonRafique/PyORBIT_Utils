import os

sbs = True

master_dir = os.getcwd()

sbs_locations = []

sbs_locations.append('/610_SbS')
sbs_locations.append('/611_SbS')
sbs_locations.append('/612_SbS')
sbs_locations.append('/613_SbS')
sbs_locations.append('/614_SbS')
sbs_locations.append('/615_SbS')
sbs_locations.append('/616_SbS')
sbs_locations.append('/617_SbS')
sbs_locations.append('/618_SbS')
sbs_locations.append('/619_SbS')
sbs_locations.append('/620_SbS')
sbs_locations.append('/621_SbS')
sbs_locations.append('/622_SbS')
sbs_locations.append('/623_SbS')
sbs_locations.append('/624_SbS')

if sbs:
	for loc in sbs_locations:
		dir_ = master_dir + loc
		make_command = 'python Make_SLURM_submission_script.py'		
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)		
		os.system(submit_command)
