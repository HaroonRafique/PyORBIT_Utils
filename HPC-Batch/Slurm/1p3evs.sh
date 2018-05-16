#!/bin/bash
#SBATCH -p be-short
#SBATCH --job-name 1p3eVs
#SBATCH -n 100
#SBATCH -t 1-23:59
#SBATCH -o slurm.%N.%j.out
#SBATCH -e slurm.%N.%j.err

# some MPI related stuff
module load mpi/mvapich2/2.2

export PYTHONPATH=${PYTHONPATH}:${ORBIT_ROOT}/py:${ORBIT_ROOT}/lib:${ORBIT_ROOT}/virtualenvs/py2.7/bin/lib/python2.7/site-packages/numpy
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${ORBIT_ROOT}/lib

# source intel libraries and custom environment variables
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/all-setup.sh
#~ source /hpcscratch/user/harafiqu/PyORBIT/virtualenvs/py2.7/bin/activate
source /hpcscratch/user/harafiqu/PyORBIT/py-orbit/customEnvironment.sh

#~ which python

BATCH_ROOT_DIR='/hpcscratch/user/harafiqu'
ORBIT_ROOT='/hpcscratch/user/harafiqu/PyORBIT/py-orbit'
RUN_DIR='/hpcscratch/user/harafiqu/PS_Injection/1p3evs'
#~ RUN_DIR='/hpcscratch/user/harafiqu/PyORBIT/py-orbit/examples/CERN_PSB_spacecharge'
VIRT_PY_DIR='/hpcscratch/user/harafiqu/PyORBIT/virtualenvs/py2.7/bin'
#~ OrigIwd=${ORBIT_ROOT}
OrigIwd=$(pwd)

# Activate the virtual python environment
cd ${VIRT_PY_DIR}
source activate

ClusterID=$SLURM_NODEID
ProcID=$SLURM_JOB_ID

cd ${BATCH_ROOT_DIR}

output_dir='output'
mkdir -p $output_dir

#~ simulation_info_file="${output_dir}/simulation_info_%N.%j.txt"
simulation_info_file="${BATCH_ROOT_DIR}/${output_dir}/simulation_info_${SLURM_JOB_ID}.${SLURM_NODEID}.${SLURM_PROCID}.txt"

echo "PyOrbit path:  `readlink -f ${ORBIT_ROOT}`" >> ${simulation_info_file}
echo "Python path:  `readlink -f ${PYTHONPATH}`" >> ${simulation_info_file}
echo "LD_LIBRARY_PATH:  `readlink -f ${LD_LIBRARY_PATH}`" >> ${simulation_info_file}
echo "Run path:  `readlink -f ${RUN_DIR}`" >> ${simulation_info_file}
#echo "Submit directory:  `readlink -f ${SLURM_SUBMIT_DIRECTORY}`" >> ${BATCH_ROOT_DIR}/${simulation_info_file}
echo "Submit host:  `readlink -f ${SLURM_SUBMIT_HOST}`" >> ${simulation_info_file}
echo "SLURM Job name:  `readlink -f ${SLURM_JOB_NAME}`" >> ${simulation_info_file}
echo "SLURM Job ID:  `readlink -f ${SLURM_JOB_ID}`" >> ${simulation_info_file}
echo "SLURM Nodes allocated:  `readlink -f ${SLURM_JOB_NUM_NODES}`" >> ${simulation_info_file}
echo "SLURM CPUS per Node:  `readlink -f ${SLURM_CPUS_ON_NODE}`" >> ${simulation_info_file}
echo "SLURM Node ID:  `readlink -f ${SLURM_NODEID}`" >> ${simulation_info_file}
echo "SLURM total cores for job:  `readlink -f ${SLURM_NTASKS}`" >> ${simulation_info_file}
echo "SLURM process ID:  `readlink -f ${SLURM_PROCID}`" >> ${simulation_info_file}
echo "****************************************" >> ${simulation_info_file}


cd ${RUN_DIR}

# run the job
tstart=$(date +%s)
#~ nnodes=$SLURM_NTASKS #CPUs

#~ $MPIBIN/mpirun -np $nnodes ${ORBIT_ROOT}/bin/pyORBIT ${RUN_DIR}/pyOrbit.py

srun ${ORBIT_ROOT}/bin/pyORBIT ${RUN_DIR}/pyOrbit.py
#~ srun ${ORBIT_ROOT}/bin/pyORBIT ${RUN_DIR}/PSB_spacecharge.py

rm Maxwellian_bend_for_ptc.txt
rm junk.txt

tend=$(date +%s)
dt=$(($tend - $tstart))
#~ cd ${BATCH_ROOT_DIR}
echo 'total simulation time (s): ' $dt >> ${simulation_info_file}

