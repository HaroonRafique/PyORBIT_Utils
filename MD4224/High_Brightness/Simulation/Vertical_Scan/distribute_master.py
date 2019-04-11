import shutil

sbs = False
twopfive = True

master_directory = './Master'
pyorbit_file = master_directory + '/pyOrbit.py'
sim_params_file = master_directory + '/simulation_parameters.py'

sbs_locations = []
twopfive_locations = []

sbs_locations.append('./610_SbS/')
sbs_locations.append('./612_SbS/')
sbs_locations.append('./614_SbS/')
sbs_locations.append('./616_SbS/')
sbs_locations.append('./618_SbS/')
sbs_locations.append('./620_SbS/')
sbs_locations.append('./622_SbS/')
sbs_locations.append('./624_SbS/')

twopfive_locations.append('./610_2p5/')
twopfive_locations.append('./612_2p5/')
twopfive_locations.append('./614_2p5/')
twopfive_locations.append('./616_2p5/')
twopfive_locations.append('./618_2p5/')
twopfive_locations.append('./620_2p5/')
twopfive_locations.append('./622_2p5/')
twopfive_locations.append('./624_2p5/')

if sbs:
	for loc in sbs_locations:
		newPath = shutil.copy(pyorbit_file, loc)
		newPath = shutil.copy(sim_params_file, loc)
		print pyorbit_file, ' copied to ', loc
if twopfive:
	for loc in sbs_locations:
		newPath = shutil.copy(pyorbit_file, loc)
		newPath = shutil.copy(sim_params_file, loc)
		print pyorbit_file, ' copied to ', loc
