#!/bin/bash
#SBATCH -p be-short
#SBATCH -N 5
#SBATCH --job-name Tr_5
#SBATCH --mem-per-cpu 3200M
#SBATCH --ntasks-per-node 40
#SBATCH -exclusive
#SBATCH -t 1-23:59
#SBATCH -o slurm.%N.%j.out
#SBATCH -e slurm.%N.%j.err

# source intel libraries and custom environment variables
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/all-setup.sh
source /hpcscratch/user/harafiqu/PyORBIT/py-orbit/customEnvironment.sh
source /hpcscratch/user/harafiqu/PyORBIT/virtualenvs/py2.7/bin/activate

# some MPI related stuff
module load mpi/mvapich2/2.2

BATCH_ROOT_DIR='/hpcscratch/user/harafiqu'
ORBIT_ROOT='/hpcscratch/user/harafiqu/PyORBIT/py-orbit'
RUN_DIR='/bescratch/user/harafiqu/PyORBIT_Utils/Performance_Tests/Simulations/Tracking/5_Node/'
OrigIwd=$(pwd)

cd ${RUN_DIR}
./clean_folder.sh
cd ${BATCH_ROOT_DIR}

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

# run the job
cd ${RUN_DIR}
tstart=$(date +%s)

srun ${ORBIT_ROOT}/bin/pyORBIT ${RUN_DIR}/pyOrbit.py

tend=$(date +%s)
dt=$(($tend - $tstart))
echo 'total simulation time (s): ' $dt >> ${simulation_info_file}
