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

	def __init__(self, matfile):
		data = sio.loadmat(matfile, squeeze_me=True)
		self.data = data
		self.I = data['density_array']
		self.t, self.dE = np.meshgrid(data['time_nsec'],data['energy_MeV'])
		self.t_rand = []
		self.dE_rand = []

	def getCoordinates(self, n_mp=1, noise_level=0):
		data = self.data
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
		plt.scatter(self.t,self.dE,15,self.I,lw=0)
		ax.set_xlabel('time [ns]')
		ax.set_ylabel('dE [MeV]')

	def plot_generated_distribution(self):
		f,ax = plt.subplots(1)
		plt.hist2d(self.t_rand,self.dE_rand,len(np.unique(self.t)))
		ax.set_xlabel('time [ns]')
		ax.set_ylabel('dE [MeV]')


def generate_initial_distribution(parameters, Lattice=None, output_file='ParticleDistribution.in', outputFormat='pyOrbit',
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
	Longitudinal_distribution = LongitudinalDistributionFromTomoscope(p['tomo_matfile'])
	t_rand, dE_rand = Longitudinal_distribution.getCoordinates(p['n_macroparticles'],noise_level) 
	z = t_rand * speed_of_light * beta * 1e-9 # convert ns to s and then m
	dE = dE_rand * 1e-3 # convert from MeV to GeV
	dpp = dE / p['energy']/1.e-9 / beta**2 
	
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
	while len(x)<p['n_macroparticles']:
		Transverse_coords = Transverse_distribution.getCoordinates()
		x.append(Transverse_coords[0])
		xp.append(Transverse_coords[1])
		y.append(Transverse_coords[2])
		yp.append(Transverse_coords[3])
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




'''
class LongitudinalBinomialDistribution():

	def __init__(self, RF, z_max, m):
		self.RF = RF
		self.z_max = z_max
		self.H_max = RF.get_H(z_max,0.0)
		self.m = m
		self.dist = lambda z,m: (1-np.clip(z,0,1)**2)**(m-1) # REPRESENTATION OF BEAM ELLIPSES FOR TRANSPORT CALCULATIONS, W. JOHO, SIN-REPORT TM-11-14

	def getCoordinates(self, n_mp=1):
		dist = self.dist
		RF = self.RF
		z_max = self.z_max
		H_max = self.H_max
		m = self.m

		z = np.linspace(-z_max,z_max,100)
		dp_max = 1.2*np.nanmax(RF.get_dp(z[1:-1], H_max))
		U_ = []
		V_ = []
		W_ = []		
		while len(U_)<n_mp:
			u = np.random.uniform(-z_max,z_max,n_mp)
			v = np.random.uniform(-dp_max,dp_max,n_mp)
			w = np.random.uniform(0,1,n_mp)
			d = dist(RF.get_H(u,v)/H_max, m)
			mask = np.where(w < d)[0]
			U_.extend(u[mask])
			V_.extend(v[mask])
			W_.extend(w[mask])
			# print len(U_)
		z_rand = np.array(U_[:n_mp])
		dp_rand = np.array(V_[:n_mp])
		return z_rand, dp_rand

	def getBunchProfile(self, n_steps=100):
	    dist = self.dist
	    RF = self.RF
	    z_max = self.z_max
	    H_max = self.H_max
	    m = self.m

	    z = np.linspace(-z_max,z_max,n_steps)
	    dp_max = 1.2*np.nanmax(RF.get_dp(z[1:-1], H_max))
	    dp = np.linspace(-dp_max,dp_max,n_steps)
	    xx, yy = np.meshgrid(z, dp, sparse=False)
	    hh = dist(RF.get_H(xx,yy)/H_max, m)
	    hh_ysum = np.sum(hh,axis=0)
	    z_step = np.mean(np.diff(z))
	    z_profile = hh_ysum/np.sum(hh_ysum*z_step)
	    z_mean = sum(z*z_profile)/sum(z_profile)    
	    z_rms = np.sqrt( sum(z_profile * (z-z_mean)**2)/sum(z_profile) )
	    # z_rms = np.sqrt(np.sum(z_profile * (z-z_mean)**2 * z_step ))
	    hh_xsum = np.sum(hh,axis=1)
	    dp_step = np.mean(np.diff(dp))
	    dp_profile = hh_xsum/np.sum(hh_xsum*dp_step)
	    dp_mean = sum(dp*dp_profile)/sum(dp_profile)
	    dp_rms = np.sqrt( sum(dp_profile*(dp-dp_mean)**2)/sum(dp_profile) )
	    # dp_rms = np.sqrt(np.sum(dp**2 * dp_profile * dp_step ))
	    return z, z_profile, z_rms, dp, dp_profile, dp_rms
'''
