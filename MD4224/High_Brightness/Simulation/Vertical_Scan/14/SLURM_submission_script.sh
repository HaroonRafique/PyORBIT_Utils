#!/bin/bash
#SBATCH -p be-long
#SBATCH --job-name 14_V_MD4224
#SBATCH -N 1
#SBATCH --ntasks-per-node 40
#SBATCH --mem-per-cpu 3200M
#SBATCH -t 14-00:00
#SBATCH -o slurm.%N.%j.out
#SBATCH -e slurm.%N.%j.err
#SBATCH --exclusive

BATCH_ROOT_DIR=/hpcscratch/user/harafiqu
RUN_DIR=/bescratch/user/harafiqu/PyORBIT_Utils/MD4224/High_Brightness/Simulation/Vertical_Scan/14
OrigIwd=$(pwd)

# Make an output folder in the root directory to hold SLURM info file
cd ${BATCH_ROOT_DIR}
output_dir="output"
mkdir -p $output_dir

# Fill the SLURM info file
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

# Enter job directory, clean it, and setup environment -> SLURM info file
cd ${RUN_DIR}
./clean_all.sh
. setup_environment.sh >> ${simulation_info_file}

# Load correct MPI
module load mpi/mvapich2/2.2

tstart=$(date +%s)

# Run the job
srun -${ORBIT_ROOT}/bin/pyORBIT ${RUN_DIR}/pyOrbit.py

tend=$(date +%s)
dt=$(($tend - $tstart))
echo "total simulation time (s): " $dt >> ${simulation_info_file}