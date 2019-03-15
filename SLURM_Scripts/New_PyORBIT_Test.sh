#!/bin/bash
#SBATCH -p be-long				# queues: inf: be-long, batch-long. 2-day:batch-short, be-short 
#SBATCH -N 5					# Nodes
#SBATCH --job-name PO_Test		# job name, keep it short to see on queue (8 chars max)
#SBATCH --mem-per-cpu 3200M		# Memory limit required when using hyperthreading
#SBATCH --ntasks-per-node 20	# be queues have 20 cores, batch have 16 (x2 for hyperthreading)
#SBATCH -exclusive				# only your user can access excess cores on this node
#SBATCH -t 13-23:59				# time limit days-hours:minutes
#SBATCH -o slurm.%N.%j.out		# screen output piped to this file
#SBATCH -e slurm.%N.%j.err		# errors piped to this file
#SBATCH --hint=nomultithread	# turn off multithreading, need to repeat at srun command

BATCH_ROOT_DIR='/hpcscratch/user/harafiqu'
RUN_DIR='/hpcscratch/user/harafiqu/bescratch/PyORBIT_Utils/SLURM_Tests/MD4224_Horizontal_HB'
OrigIwd=$(pwd)

# Source appropriate files to use custom environment
echo
source /afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/py-orbit/customEnvironment.sh
echo "customEnvironment done"
echo
source /afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/virtualenvs/py2.7/bin/activate
echo
echo "python packages charged"
echo
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/setup.sh
echo
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/ifortvars.sh intel64
echo
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/iccvars.sh intel64
echo
echo "ifort charged (necessary for running)"
echo

# Clean the simulation folder (old data, needed for pickle sims etc)
cd ${RUN_DIR}
./clean_folder.sh
cd ${BATCH_ROOT_DIR}

# Output directory for following slurm info file only (error and standard output go to submission directory)
output_dir='output'
mkdir -p $output_dir

simulation_info_file="${BATCH_ROOT_DIR}/${output_dir}/simulation_info_${SLURM_JOB_ID}.${SLURM_NODEID}.${SLURM_PROCID}.txt"

echo "PyOrbit path:  `readlink -f ${ORBIT_ROOT}`" >> ${simulation_info_file}
echo "Run path:  `readlink -f ${RUN_DIR}`" >> ${simulation_info_file}
echo "Submit host:  `readlink -f ${SLURM_SUBMIT_HOST}`" >> ${simulation_info_file}
echo "SLURM Job name:  `readlink -f ${SLURM_JOB_NAME}`" >> ${simulation_info_file}
echo "SLURM Job ID:  `readlink -f ${SLURM_JOB_ID}`" >> ${simulation_info_file}
echo "SLURM Nodes allocated:  `readlink -f ${SLURM_JOB_NUM_NODES}`" >> ${simulation_info_file}
echo "SLURM CPUS per Node:  `readlink -f ${SLURM_CPUS_ON_NODE}`" >> ${simulation_info_file}
echo "SLURM Node ID:  `readlink -f ${SLURM_NODEID}`" >> ${simulation_info_file}
echo "SLURM total cores for job:  `readlink -f ${SLURM_NTASKS}`" >> ${simulation_info_file}
echo "SLURM process ID:  `readlink -f ${SLURM_PROCID}`" >> ${simulation_info_file}
echo "****************************************" >> ${simulation_info_file}

# load MPI
module load mpi/mvapich2/2.2

# Timing
cd ${RUN_DIR}
tstart=$(date +%s)

# Run the job
srun --hint=nomultithread ${ORBIT_ROOT}/bin/pyORBIT ${RUN_DIR}/pyOrbit.py

tend=$(date +%s)
dt=$(($tend - $tstart))
echo 'total simulation time (s): ' $dt >> ${simulation_info_file}
