import os

sbs = True
sbs_nolk = True
twopfive = True

master_dir = os.getcwd()

sbs_locations = []
twopfive_locations = []
sbs_nlk_locations = []

sbs_locations.append('/Grid/32_32_16')
sbs_locations.append('/Grid/64_64_32')
sbs_locations.append('/Grid/128_128_64')
sbs_locations.append('/Grid/256_256_128')
sbs_locations.append('/N_mp/0p5E6')
sbs_locations.append('/N_mp/1E6')
sbs_locations.append('/N_mp/1p5E6')
sbs_locations.append('/N_mp/2E6')
sbs_locations.append('/N_mp/2p5E6')
sbs_locations.append('/N_mp/3E6')

sbs_nlk_locations.append('/Grid_nLK/32_32_16')
sbs_nlk_locations.append('/Grid_nLK/64_64_32')
sbs_nlk_locations.append('/Grid_nLK/128_128_64')
sbs_nlk_locations.append('/Grid_nLK/256_256_128')
sbs_nlk_locations.append('/N_mp_nLK/0p5E6')
sbs_nlk_locations.append('/N_mp_nLK/1E6')
sbs_nlk_locations.append('/N_mp_nLK/1p5E6')
sbs_nlk_locations.append('/N_mp_nLK/2E6')
sbs_nlk_locations.append('/N_mp_nLK/2p5E6')
sbs_nlk_locations.append('/N_mp_nLK/3E6')

twopfive_locations.append('/Grid_2p5/32_32_16')
twopfive_locations.append('/Grid_2p5/64_64_32')
twopfive_locations.append('/Grid_2p5/128_128_64')
twopfive_locations.append('/Grid_2p5/256_256_128')
twopfive_locations.append('/N_mp_2p5/0p5E6')
twopfive_locations.append('/N_mp_2p5/1E6')
twopfive_locations.append('/N_mp_2p5/1p5E6')
twopfive_locations.append('/N_mp_2p5/2E6')
twopfive_locations.append('/N_mp_2p5/2p5E6')
twopfive_locations.append('/N_mp_2p5/3E6')

if sbs:
	for loc in sbs_locations:
		dir_ = master_dir + loc
		make_command = 'python Make_SLURM_submission_script.py'		
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)		
		os.system(submit_command)
if sbs_nolk:
	for loc in sbs_nlk_locations:
		dir_ = master_dir + loc
		make_command = 'python Make_SLURM_submission_script.py'		
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)		
		os.system(submit_command)
if twopfive:
	for loc in twopfive_locations:
		dir_ = master_dir + loc
		make_command = 'python Make_SLURM_submission_script.py'		
		submit_command = 'sbatch SLURM_submission_script.sh'
		os.chdir(dir_)
		os.system(make_command)		
		os.system(submit_command)
