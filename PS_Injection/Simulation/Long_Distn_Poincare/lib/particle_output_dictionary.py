# ~ import time
import orbit_mpi
import os
# ~ import scipy.io as sio

# 24.07.2018: 	Created by Haroon Rafique, CERN BE-ABP-HSI 
#			Started with clone of Hannes Bartosik's output dictionary

class Particle_output_dictionary(object):
	
	def __init__(self, particle_output_dictionary = None):
		if particle_output_dictionary:
			print "Particle_output_dictionary::__init__: constructor with existing dictionary not yet implemented"
		else:
			self.update_flag = 0
			self.particles = {}			# Top level dictionary : N : All data	
			self.particle_list = [] 	# Record indices of stored particles
			self.turn_list = [] 		# Record indices of stored turns
			
			self.AddNewParticle(0)
			
			print 'Particle_output_dictionary: Created initial particle data dictionary \'particles\'\n \tprinting for particle 0'
			print 'Format: {\'particle\': {\'turn\': {\'dE\': 0.0, \'px\': 0.0, \'py\': 0.0, \'y\': 0.0, \'x\': 0.0, \'z\': 0.0}}}'
			print self.particles
			
	def AddNewParticle(self, n):
		# Check that we haven't updated anything before adding a new particle
		if self.update_flag:
			print "Particle_output_dictionary::AddNewParticle: Particles already updated. Add particles before tracking. Aborting addition."
		else:			
			# Check that the particle isn't already present
			if n in self.particle_list:
				print "Particle_output_dictionary::AddNewParticle: Particle already added. Aborting addition."
			else:	
				# Append the new particle
				self.particles[str(n)] = {} # First level in : N-1 : Particle Index
			
				# Add zero turn
				self.particles[str(n)]['0'] = {}	# Second level : N-2 : Turn
			
				# Add each co-ordinate and set initial values to zero
				self.particles[str(n)]['0']['x'] = 0.	# Third level : N-3 : x
				self.particles[str(n)]['0']['px'] = 0.	# Third level : N-3 : px
				self.particles[str(n)]['0']['y'] = 0.	# Third level : N-3 : y
				self.particles[str(n)]['0']['py'] = 0.	# Third level : N-3 : py
				self.particles[str(n)]['0']['z'] = 0.	# Third level : N-3 : z
				self.particles[str(n)]['0']['dE'] = 0.	# Third level : N-3 : dE
				
				# Append to list of indices
				self.particle_list.append(n)
				
				print "Particle_output_dictionary::AddNewParticle: Added particle "
				print n
				print "Dictionary now:"
				print self.particles
		
	def update(self, bunch, turn):
		self.update_flag = 1
		
		rank = orbit_mpi.MPI_Comm_rank(orbit_mpi.mpi_comm.MPI_COMM_WORLD)
		if not rank:
						
			for n in self.particle_list:
				# Create the particle and turn dictionaries
				self.particles[str(n)] = {} # First level in : N-1 : Particle Index
				self.particles[str(n)][str(turn)] = {}	# Second level : N-2 : Turn
			
				# self.particles[index][turn]['x'] = bunch.x(index)
				self.particles[str(n)][str(turn)]['x'] = bunch.x(n)
				self.particles[str(n)][str(turn)]['xp'] = bunch.xp(n)
				self.particles[str(n)][str(turn)]['y'] = bunch.y(n)
				self.particles[str(n)][str(turn)]['yp'] = bunch.yp(n)
				self.particles[str(n)][str(turn)]['z'] = bunch.z(n)
				self.particles[str(n)][str(turn)]['dE'] = bunch.dE(n)
				
		self.turn_list.append(turn)
				
	# Function to print 6D co-ordinates for a particle for 1 given turn
	def print_particle_for_turn(self, turn, n, filename=None):
		rank = orbit_mpi.MPI_Comm_rank(orbit_mpi.mpi_comm.MPI_COMM_WORLD)
		if not rank:
			if filename is None:				
				filename = 'Particle_' + str(n) + '_turn_' + str(turn) + '.dat'
				
			# Check that the particle exists
			if n not in self.particle_list:
				print "Particle_output_dictionary::print_particle_for_turn: Particle not stored, use AddNewParticle(n) before tracking."
			else:
				# if file exists then append
				if os.path.exists(filename):
					f = open(filename,"a+")
										
				# if file doesn't exist create and add header
				else:
					f = open(filename,"w+")
					f.write("#ParticleID\tTurn\tx\txp\ty\typ\tz\tdE")
				
				f.write("\n%i\t%i\t%f\t%f\t%f\t%f\t%f\t%f" % ( 	\
					n, turn, 										\
					self.particles[str(n)][str(turn)]['x'],		\
					self.particles[str(n)][str(turn)]['xp'],	\
					self.particles[str(n)][str(turn)]['y'],		\
					self.particles[str(n)][str(turn)]['yp'],	\
					self.particles[str(n)][str(turn)]['z'],		\
					self.particles[str(n)][str(turn)]['dE']		))
				f.close()

	# Function to print 6D co-ordinates for a particle for all turns
	def print_particle(self, n, filename=None):
		rank = orbit_mpi.MPI_Comm_rank(orbit_mpi.mpi_comm.MPI_COMM_WORLD)
		if not rank:
			if filename is None:				
				filename = 'Particle_' + str(n) + '.dat'
				
			# Check that the particle exists
			if n not in self.particle_list:
				print "Particle_output_dictionary::print_particle: Particle not stored, use AddNewParticle(n) before tracking."
			else:
				# if file exists then append
				if os.path.exists(filename):
					f = open(filename,"a+")
										
				# if file doesn't exist create and add header
				else:
					f = open(filename,"w+")
					f.write("#ParticleID\tTurn\tx\txp\ty\typ\tz\tdE")
				
				for t in self.turn_list:				
					f.write("\n%i\t%i\t%f\t%f\t%f\t%f\t%f\t%f" % ( 	\
						n, t, 										\
						self.particles[str(n)][str(t)]['x'],		\
						self.particles[str(n)][str(t)]['xp'],		\
						self.particles[str(n)][str(t)]['y'],		\
						self.particles[str(n)][str(t)]['yp'],		\
						self.particles[str(n)][str(t)]['z'],		\
						self.particles[str(n)][str(t)]['dE'] 		))
				f.close()
				
					
	# Function to print 6D co-ordinates for all particles for all turns
	def print_all_particles(self, filename=None):
		rank = orbit_mpi.MPI_Comm_rank(orbit_mpi.mpi_comm.MPI_COMM_WORLD)
		if not rank:
			if filename is None:				
				filename = 'Particles_all.dat'

			# if file exists then append
			if os.path.exists(filename):
				f = open(filename,"a+")
									
			# if file doesn't exist create and add header
			else:
				f = open(filename,"w+")
				f.write("#ParticleID\tTurn\tx\txp\ty\typ\tz\tdE")
			
			for n in self.particle_list:	
				for t in self.turn_list:			
					f.write("\n%i\t%i\t%f\t%f\t%f\t%f\t%f\t%f" % ( 	\
						n, t, 										\
						self.particles[str(n)][str(t)]['x'],		\
						self.particles[str(n)][str(t)]['xp'],		\
						self.particles[str(n)][str(t)]['y'],		\
						self.particles[str(n)][str(t)]['yp'],		\
						self.particles[str(n)][str(t)]['z'],		\
						self.particles[str(n)][str(t)]['dE']		))
			f.close()
			print self.particle_list
			print self.turn_list
				
			
	# ~ def save_to_matfile(self, filename):
		# ~ rank = orbit_mpi.MPI_Comm_rank(orbit_mpi.mpi_comm.MPI_COMM_WORLD)
		# ~ if not rank:
			# ~ sio.savemat(filename, self.output_dict)
		# ~ orbit_mpi.MPI_Barrier(orbit_mpi.mpi_comm.MPI_COMM_WORLD)

	# ~ def import_from_matfile(self, filename):
		# ~ d = sio.loadmat(filename, squeeze_me=True)
		# ~ for k in self.output_dict:
			# ~ self.output_dict[k] = d[k].tolist()
