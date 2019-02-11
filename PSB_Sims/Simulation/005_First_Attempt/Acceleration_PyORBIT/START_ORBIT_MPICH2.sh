#!/bin/bash

if [ ! -n "$1" ]
  then
    echo "Usage: `basename $0` <name of the SC script> <N CPUs>"
    exit $E_BADARGS
fi

if [ ! -n "$2" ]
  then
    echo "Usage: `basename $0` <name of the SC script> <N CPUs>"
    exit $E_BADARGS
fi

# Have to choose which PyORBIT to use:
export ORBIT_ROOT=/afs/cern.ch/user/p/pyorbit/public/PyORBIT/py-orbit
#export ORBIT_ROOT=/afs/cern.ch/project/LIUsc/space_charge/Codes/py-orbit_revison1291_dev_FrozenPIC

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${ORBIT_ROOT}/lib
export PYTHONPATH=${PYTHONPATH}:${ORBIT_ROOT}/py:${ORBIT_ROOT}/lib
export PATH=$PATH:${ORBIT_ROOT}/bin

source /afs/cern.ch/user/p/pyorbit/public/PyORBIT/py-orbit/customEnvironment.sh
source /afs/cern.ch/user/p/pyorbit/public/PyORBIT/virtualenvs/py2.7/bin/activate
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/all-setup.sh

# opposite of useful:

# Probably required:

# Possibly useful:
#source /afs/cern.ch/sw/lcg/external/gcc/4.8.4/x86_64-slc6-gcc48-opt/setup.sh 
#export LD_LIBRARY_PATH=/afs/cern.ch/sw/lcg/contrib/gcc/4.8.1/x86_64-slc6-gcc48-opt/lib64 

echo 'ORBIT_ROOT = '
echo ${ORBIT_ROOT}

# /afs/cern.ch/project/LIUsc/space_charge/Codes/mpich-3.0/bin/mpirun -np $2 ${ORBIT_ROOT}/bin/pyORBIT $1
/afs/cern.ch/project/LIUsc/space_charge/Codes/mpich2-1.4.1p1/bin/mpirun -np $2 ${ORBIT_ROOT}/bin/pyORBIT $1
