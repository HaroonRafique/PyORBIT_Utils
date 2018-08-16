import numpy as np
import scipy.io as sio
from scipy import interpolate
import orbit_mpi
import csv

# import matplotlib.pylab as plt
from orbit.utils.consts import speed_of_light
from orbit.bunch_generators import TwissContainer, TwissAnalysis
from orbit.bunch_generators import WaterBagDist2D, GaussDist2D

class LongitudinalDistributionFromTomoscope():

	def __init__(self, filename, matfile=0):
		if matfile:
			data = sio.loadmat(filename, squeeze_me=True)
			self.data = data
			self.I = data['density_array']
			self.t, self.dE = np.meshgrid(data['time_nsec'],data['energy_MeV'])		
			print self.t
			# ~ print self.t	#keys
			# ~ print self.t['key'] #array structure 1 level in
			print self.dE.shape
			print self.I.shape
			
		else:
			thefile = open(filename,"r")
			lines=0
			for l in thefile:
				lines = lines + 1
				
			lines = lines - 2
			print 'grid size = ', lines, ' * ', lines, ' = ', (lines*lines)
				
			thefile.close()
			thefile = open(filename,"r")			
			
			# Need to know the size of the square numpy array from the input file
			# ~ self.I = np.zeros(shape=(lines,lines))
			self.dt_bin =  np.zeros(shape=(lines,lines))
			self.dE_bin =  np.zeros(shape=(lines,lines))
			self.dt_no_bins = 0
			self.dE_no_bins = 0
			
			for l in thefile:
				# First line: Minimum dt, maximum dt, binsize, bins
				if l == 0:
					self.dt_min = l.split()[0]
					self.dt_max = l.split()[1]
					self.dt_bin = l.split()[2]
					self.dt_no_bins = l.split()[3]
				# Second line: Minimum dE, maximum dE, binsize, bins
				elif l == 1:
					self.dE_min = l.split()[0]
					self.dE_max = l.split()[1]
					self.dE_bin = l.split()[2]
					self.dE_no_bins = l.split()[3]
				# Read grid line by line to create density array
				else:
					self.temp=[]
					# read each value and append to array
					for i in l.split():
						self.temp.append(float(i))
					# append array to density array
					self.I.append(self.temp)
					self.temp=[]
			print self.I
			
			self.dt_bins = np.arange(self.dt_no_bins)*self.dt_bin
			self.dE_bins = np.arange(self.dE_no_bins)*self.dE_bin
					
			# make a meshgrid using the min max and binsize etc
			self.t, self.dE = np.meshgrid( self.dt_bins, self.dE_bins)
			print self.t
			print self.t.keys()
			
		self.t_rand = []
		self.dE_rand = []			
		
	def getCoordinates(self, n_mp=1, noise_level=0):
		# ~ data = self.data
		I = self.I
		t = self.t
		dE = self.dE

		U_ = []
		V_ = []
		W_ = []
		t_min = np.min(t)
		t_max = np.max(t)
		dE_min = np.min(dE)
		dE_max = np.max(dE)
		I_max = np.max(I)
		while len(U_)<n_mp:
			u = np.random.uniform(t_min,t_max,n_mp)
			v = np.random.uniform(dE_min,dE_max,n_mp)
			w = np.random.uniform(0,I_max,n_mp)
			# unique creates an array of unique values in an array (for 
			# example dE). Digitize bins an array (v) according to bins
			# (np.unique(dE)) and returns an output array of indices the
			#  same size as (v).Basically this tells us which 'bin' v is
			# in, we minus 1 to give the start of the bin rather than 
			# the end. This points to the density in the 2D array 
			# generated by the tomo.
			d = I[np.digitize(v, np.unique(dE))-1, np.digitize(u, np.unique(t))-1]
			mask = np.where(w < d-noise_level*I_max)[0]
			U_.extend(u[mask])
			V_.extend(v[mask])
			W_.extend(w[mask])
			# print len(U_)
		t_rand = np.array(U_[:n_mp])
		dE_rand = np.array(V_[:n_mp])
		self.t_rand = t_rand
		self.dE_rand = dE_rand
		return t_rand, dE_rand

	def plot_Tomoscope_data(self):
		f,ax = plt.subplots(1)
		plt.scatter(self.t, self.dE, 15, self.I, lw=0)
		ax.set_xlabel('time [ns]')
		ax.set_ylabel('dE [MeV]')

	def plot_generated_distribution(self):
		f,ax = plt.subplots(1)
		plt.hist2d(self.t_rand, self.dE_rand, len(np.unique(self.t)))
		ax.set_xlabel('time [ns]')
		ax.set_ylabel('dE [MeV]')


def generate_initial_distribution(parameters, matfile=0, Lattice=None, output_file='ParticleDistribution.in', outputFormat='pyOrbit',
								  summary_file='ParticleDistribution_summary.txt', summary_mat_file=None):
	assert outputFormat in ['Orbit', 'pyOrbit']								 
	parameters['alphax0'] = Lattice.alphax0
	parameters['betax0']  = Lattice.betax0
	parameters['alphay0'] = Lattice.alphay0
	parameters['betay0']  = Lattice.betay0
	parameters['etax0']   = Lattice.etax0
	parameters['etapx0']  = Lattice.etapx0
	parameters['etay0']   = Lattice.etay0
	parameters['etapy0']  = Lattice.etapy0
	parameters['x0']      = Lattice.orbitx0
	parameters['xp0']     = Lattice.orbitpx0
	parameters['y0']      = Lattice.orbity0
	parameters['yp0']     = Lattice.orbitpy0
	parameters['gamma_transition'] = Lattice.gammaT
	parameters['circumference']    = Lattice.getLength()
	parameters['length'] = Lattice.getLength()/Lattice.nHarm	
	
	twissX = TwissContainer(alpha = parameters['alphax0'], beta = parameters['betax0'], emittance = parameters['epsn_x'] / parameters['gamma'] / parameters['beta'])
	twissY = TwissContainer(alpha = parameters['alphay0'], beta = parameters['betay0'], emittance = parameters['epsn_y'] / parameters['gamma'] / parameters['beta'])
	dispersionx = {'etax0': parameters['etax0'], 'etapx0': parameters['etapx0']}
	dispersiony = {'etay0': parameters['etay0'], 'etapy0': parameters['etapy0']}
	closedOrbitx = {'x0': parameters['x0'], 'xp0': parameters['xp0']} 
	closedOrbity = {'y0': parameters['y0'], 'yp0': parameters['yp0']} 
	
	Transverse_distribution = GaussDist2D(twissX, twissY, cut_off=parameters['TransverseCut'])
		
	# initialize particle arrays
	x = np.zeros(parameters['n_macroparticles'])
	xp = np.zeros(parameters['n_macroparticles'])
	y = np.zeros(parameters['n_macroparticles'])
	yp = np.zeros(parameters['n_macroparticles'])
	z = np.zeros(parameters['n_macroparticles'])
	dE = np.zeros(parameters['n_macroparticles'])
	
	# only the main CPU is actually writing its distribution to a file ...
	comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
	if orbit_mpi.MPI_Comm_rank(comm) == 0:
		with open(output_file,"w") as fid:
			csv_writer = csv.writer(fid, delimiter=' ')			
		
			for i in range(parameters['n_macroparticles']):
				(x[i], xp[i], y[i], yp[i]) = Transverse_distribution.getCoordinates()

				x[i] += closedOrbitx['x0']
				xp[i] += closedOrbitx['xp0']
				y[i] += closedOrbity['y0']
				yp[i] += closedOrbity['yp0']
				dpp = dE[i] / (parameters['energy']) / parameters['beta']**2
				x[i] += dpp * dispersionx['etax0']
				xp[i] += dpp * dispersionx['etapx0']	
				y[i] += dpp * dispersiony['etay0']
				yp[i] += dpp * dispersiony['etapy0']	
				
				if outputFormat == 'Orbit':
					x[i] *= 1000.
					xp[i] *= 1000.
					y[i] *= 1000.
					yp[i] *= 1000.
					dE[i] /= 1.e9		
					csv_writer.writerow([x[i], xp[i], y[i], yp[i], phi[i], dE[i]])
					#csv_writer.writerow([x[i], xp[i], y[i], yp[i], z[i], dE[i]])
					
		if summary_file:
			with open(summary_file, 'w') as fid:
				map(lambda key: fid.write(key + ' = ' + str(parameters[key]) + '\n'), parameters)
		print '\nCreated particle distribution with ' + str(parameters['n_macroparticles']) + ' macroparticles into file: ', output_file
								
	orbit_mpi.MPI_Barrier(comm)

	return output_file
									  
def generate_initial_distribution_old_tomo(parameters, matfile=0, Lattice=None, output_file='ParticleDistribution.in', outputFormat='pyOrbit',
								  summary_file='ParticleDistribution_summary.txt', summary_mat_file=None):
	assert outputFormat in ['Orbit', 'pyOrbit']
	p = parameters
	beta = p['beta']
	gamma = p['gamma']
	if Lattice:
		p['alphax0'] = Lattice.alphax0
		p['betax0']  = Lattice.betax0
		p['alphay0'] = Lattice.alphay0
		p['betay0']  = Lattice.betay0
		p['etax0']   = Lattice.etax0
		p['etapx0']  = Lattice.etapx0
		p['etay0']   = Lattice.etay0
		p['etapy0']  = Lattice.etapy0
		p['x0']      = Lattice.orbitx0
		p['xp0']     = Lattice.orbitpx0
		p['y0']      = Lattice.orbity0
		p['yp0']     = Lattice.orbitpy0
		p['gamma_transition'] = Lattice.gammaT
		p['circumference']    = Lattice.getLength()

	# building the distributions
	# eta = 1/p['gamma_transition']**2 - 1/p['gamma']**2
	# R = p['circumference']/2/np.pi
	# beta = p['beta']
	# energy = p['energy']
	# phi_rf = p['phi_s']
	# h = p['harmonic_number']
	# h_main = np.atleast_1d(p['harmonic_number'])[0]
	# rf_voltage = p['rf_voltage']
	# RF = DoubleRF(R, eta, beta, energy, phi_rf, h, rf_voltage)
	# Longitudinal_distribution = LongitudinalBinomialDistribution(RF, p['LongitudinalDistribution_z_max'], p['LongitudinalJohoParameter'])
	# z, dpp = Longitudinal_distribution.getCoordinates(p['n_macroparticles'])
	
	# building the distributions
	beta = p['beta']
	try: 
		noise_level = p['noise_level']
	except KeyError:
		noise_level = 0
	
	# ~ Longitudinal_distribution = LongitudinalDistributionFromTomoscope(p['tomo_file'])
	Longitudinal_distribution = LongitudinalDistributionFromTomoscope(p['tomo_file'], matfile)
	
	# ~ Longitudinal_distribution.plot_Tomoscope_data()
	# ~ Longitudinal_distribution.plot_generated_distribution()
	
	t_rand, dE_rand = Longitudinal_distribution.getCoordinates(p['n_macroparticles'], noise_level) 
	z = t_rand * speed_of_light * beta * 1e-9 # convert ns to s and then m
	# ~ z = (t_rand * 1e-9) * speed_of_light * beta * 0.075 # convert ns to s and then m
	dE = dE_rand * 1e-3 # convert from MeV to GeV
	dpp = dE / p['energy'] / 1.e-9 / beta**2 
	# ~ dpp = dE / p['energy'] / beta**2  # Not sure which dpp definition is correct
	
	# h_main = np.atleast_1d(p['harmonic_number'])[0]
	# R = p['circumference']/2/np.pi
	# phi = - z * h_main / R

	# z_arr, z_profile, z_rms, dp, dp_profile, dpp_rms = Longitudinal_distribution.getBunchProfile()
	# p['dpp_sigma'] = _GaussianFit(dp, dp_profile)[0][2]
	# p['dpp_sigma_from_FWHM'] = _Gaussian_sigma_from_FWHM(dp, dp_profile)
	# p['dpp_profile'] = np.array([dp, dp_profile])
	# p['dpp_rms'] = dpp_rms
	# p['linedensity_profile'] = np.array([z_arr, z_profile])
	# phi = - z * h_main / R
	# dE = dpp * p['energy'] * beta**2 * 1.e-9

	# transverse coordinates
	x,xp,y,yp = [],[],[],[]
	for epsn_x, epsn_y, intensity in zip(np.atleast_1d(p['epsn_x']), np.atleast_1d(p['epsn_y']), np.atleast_1d(p['intensity'])):
		# twiss containers
		twissX = TwissContainer(alpha = p['alphax0'], beta = p['betax0'], emittance = epsn_x / gamma / beta)
		twissY = TwissContainer(alpha = p['alphay0'], beta = p['betay0'], emittance = epsn_y / gamma / beta)

		Transverse_distribution = GaussDist2D(twissX, twissY, cut_off=p['TransverseCut'])
		n_macroparticles_tmp = int(p['n_macroparticles']*(intensity/np.sum(p['intensity'])))
		Transverse_coords = np.array(map(lambda i: Transverse_distribution.getCoordinates(), xrange(n_macroparticles_tmp)))
		x.extend(Transverse_coords[:,0].tolist())
		xp.extend(Transverse_coords[:,1].tolist())
		y.extend(Transverse_coords[:,2].tolist())
		yp.extend(Transverse_coords[:,3].tolist())
		
	# in case x has not yet a length of n_macroparticles
	# ~ while len(x)<p['n_macroparticles']:
		# ~ Transverse_coords = Transverse_distribution.getCoordinates()
		# ~ x.append(Transverse_coords[0])
		# ~ xp.append(Transverse_coords[1])
		# ~ y.append(Transverse_coords[2])
		# ~ yp.append(Transverse_coords[3])
		
	# Dispersion and closed orbit	
	x = np.array(x) + p['x0']  + dpp * p['etax0']
	xp = np.array(xp) + p['xp0'] + dpp * p['etapx0']
	y = np.array(y) + p['y0']  + dpp * p['etay0']
	yp = np.array(yp) + p['yp0'] + dpp * p['etapy0']

	# only the main CPU is actually writing its distribution to a file ...
	comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
	if orbit_mpi.MPI_Comm_rank(comm) == 0:
		with open(output_file,"w") as fid:
			csv_writer = csv.writer(fid, delimiter=' ')
			if outputFormat == 'Orbit':
				x  *= 1000.
				xp *= 1000.
				y  *= 1000.
				yp *= 1000.
				# ~ dE[i] /= 1.e9	# Already in the correct units	
				map(lambda i: csv_writer.writerow([x[i], xp[i], y[i], yp[i], phi[i], dE[i]]), range(p['n_macroparticles']))	
			elif outputFormat == 'pyOrbit':
				map(lambda i: csv_writer.writerow([x[i], xp[i], y[i], yp[i], z[i], dE[i]]), range(p['n_macroparticles']))	

		if summary_file:
			with open(summary_file, 'w') as fid:
				map(lambda key: fid.write(key + ' = ' + str(p[key]) + '\n'), p)

		if summary_mat_file:
			with open(summary_mat_file, 'w') as fid:
				sio.savemat(fid, parameters) 

		print '\nCreated particle distribution with ' + str(p['n_macroparticles']) + ' macroparticles into file: ', output_file
	
	orbit_mpi.MPI_Barrier(comm)

	return output_file

		

def generate_initial_distribution_old_original(parameters, matfile=0, Lattice=None, output_file='ParticleDistribution.in', outputFormat='pyOrbit',
								  summary_file='ParticleDistribution_summary.txt', summary_mat_file=None):
							
	assert outputFormat in ['Orbit', 'pyOrbit']
	parameters['alphax0'] = Lattice.alphax0
	parameters['betax0']  = Lattice.betax0
	parameters['alphay0'] = Lattice.alphay0
	parameters['betay0']  = Lattice.betay0
	parameters['etax0']   = Lattice.etax0
	parameters['etapx0']  = Lattice.etapx0
	parameters['etay0']   = Lattice.etay0
	parameters['etapy0']  = Lattice.etapy0
	parameters['x0']      = Lattice.orbitx0
	parameters['xp0']     = Lattice.orbitpx0
	parameters['y0']      = Lattice.orbity0
	parameters['yp0']     = Lattice.orbitpy0
	parameters['gamma_transition'] = Lattice.gammaT
	parameters['circumference']    = Lattice.getLength()
	parameters['length'] = Lattice.getLength()/Lattice.nHarm
	# twiss containers
	twissX = TwissContainer(alpha = parameters['alphax0'], beta = parameters['betax0'], emittance = parameters['epsn_x'] / parameters['gamma'] / parameters['beta'])
	twissY = TwissContainer(alpha = parameters['alphay0'], beta = parameters['betay0'], emittance = parameters['epsn_y'] / parameters['gamma'] / parameters['beta'])
	dispersionx = {'etax0': parameters['etax0'], 'etapx0': parameters['etapx0']}
	dispersiony = {'etay0': parameters['etay0'], 'etapy0': parameters['etapy0']}
	# ~ dispersionx = {'etax0': parameters['etax0'], 'etapx0': parameters['etapx0']}
	# ~ dispersiony = {'etay0': parameters['etay0'], 'etapy0': parameters['etapy0']}
	closedOrbitx = {'x0': parameters['x0'], 'xp0': parameters['xp0']} 
	closedOrbity = {'y0': parameters['y0'], 'yp0': parameters['yp0']} 

	# initialize particle arrays
	x = np.zeros(parameters['n_macroparticles'])
	xp = np.zeros(parameters['n_macroparticles'])
	y = np.zeros(parameters['n_macroparticles'])
	yp = np.zeros(parameters['n_macroparticles'])
	z = np.zeros(parameters['n_macroparticles'])
	dE = np.zeros(parameters['n_macroparticles'])

	# building the distributions
	Transverse_distribution = GaussDist2D(twissX, twissY, cut_off=parameters['TransverseCut'])
	
	try: 
		noise_level = parameters['noise_level']
	except KeyError:
		noise_level = 0
	
	# ~ Longitudinal_distribution = LongitudinalDistributionFromTomoscope(p['tomo_file'])
	# ~ Longitudinal_distribution = LongitudinalDistributionFromTomoscope(parameters['tomo_file'], matfile)
	# ~ t_rand, dE_rand = Longitudinal_distribution.getCoordinates(parameters['n_macroparticles'], noise_level)
	# ~ z = t_rand * speed_of_light * parameters['beta'] * 1e-9 # convert ns to s and then m
	# ~ z = (t_rand * 1e-9) * speed_of_light * beta * 0.075 # convert ns to s and then m
	# ~ dE = dE_rand * 1e-3 # convert from MeV to GeV
	# ~ dpp = dE / p['energy']/1.e-9 / beta**2 
	# ~ dpp = dE / p['energy'] / beta**2 

	# only the main CPU is actually writing its distribution to a file ...
	comm = orbit_mpi.mpi_comm.MPI_COMM_WORLD
	if orbit_mpi.MPI_Comm_rank(comm) == 0:
		with open(output_file,"w") as fid:
			csv_writer = csv.writer(fid, delimiter=' ')			
		
			# ~ t_rand, dE_rand = Longitudinal_distribution.getCoordinates(parameters['n_macroparticles'], noise_level) 
			# ~ z = (t_rand * 1e-9) * speed_of_light * parameters['beta'] # convert ns to s and then m
			# ~ dE = dE_rand * 1e-3 # convert from MeV to GeV

			for i in range(parameters['n_macroparticles']):
				(x[i], xp[i], y[i], yp[i]) = Transverse_distribution.getCoordinates()
				x[i] += closedOrbitx['x0']
				xp[i] += closedOrbitx['xp0']
				y[i] += closedOrbity['y0']
				yp[i] += closedOrbity['yp0']
				dpp = dE[i] / (parameters['energy']) / parameters['beta']**2
				x[i] += dpp * dispersionx['etax0']
				xp[i] += dpp * dispersionx['etapx0']	
				y[i] += dpp * dispersiony['etay0']
				yp[i] += dpp * dispersiony['etapy0']	
				
				if outputFormat == 'Orbit':
					x[i] *= 1000.
					xp[i] *= 1000.
					y[i] *= 1000.
					yp[i] *= 1000.
					dE[i] /= 1.e9		
					csv_writer.writerow([x[i], xp[i], y[i], yp[i], phi[i], dE[i]])
				#csv_writer.writerow([x[i], xp[i], y[i], yp[i], z[i], dE[i]])
		if summary_file:
			with open(summary_file, 'w') as fid:
				map(lambda key: fid.write(key + ' = ' + str(parameters[key]) + '\n'), parameters)
		print '\nCreated particle distribution with ' + str(parameters['n_macroparticles']) + ' macroparticles into file: ', output_file


	orbit_mpi.MPI_Barrier(comm)

	return output_file
