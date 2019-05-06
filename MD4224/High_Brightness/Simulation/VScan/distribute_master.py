import shutil

pyorbit = False
simulation_parameters = False
flat_files = False

sbs = False

master_directory = './Master'
pyorbit_file = master_directory + '/pyOrbit.py'
sim_params_file = master_directory + '/simulation_parameters.py'
flat_file = master_directory + '/Flat_file.madx'

sbs_locations = []

sbs_locations.append('./610_SbS/')
sbs_locations.append('./611_SbS/')
sbs_locations.append('./612_SbS/')
sbs_locations.append('./613_SbS/')
sbs_locations.append('./614_SbS/')
sbs_locations.append('./615_SbS/')
sbs_locations.append('./616_SbS/')
sbs_locations.append('./617_SbS/')
sbs_locations.append('./618_SbS/')
sbs_locations.append('./619_SbS/')
sbs_locations.append('./620_SbS/')
sbs_locations.append('./621_SbS/')
sbs_locations.append('./622_SbS/')
sbs_locations.append('./623_SbS/')
sbs_locations.append('./624_SbS/')


if pyorbit:
	if sbs:
		for loc in sbs_locations:
			newPath = shutil.copy(pyorbit_file, loc)
			print pyorbit_file, ' copied to ', loc

if simulation_parameters:
	if sbs:
		for loc in sbs_locations:
			newPath = shutil.copy(sim_params_file, loc)
			print sim_params_file, ' copied to ', loc

if flat_files:
	if sbs:
		for loc in sbs_locations:
			newPath = shutil.copy(flat_file, loc)
			print sim_params_file, ' copied to ', loc

