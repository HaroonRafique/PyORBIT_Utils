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

export ORBIT_ROOT=/afs/cern.ch/user/p/pyorbit/public/PyORBIT/py-orbit
#export ORBIT_ROOT=/afs/cern.ch/project/LIUsc/space_charge/Codes/py-orbit_revison1291_dev_FrozenPIC

# Use these if you have a simply python linking error
#source /afs/cern.ch/sw/lcg/external/gcc/4.8.4/x86_64-slc6-gcc48-opt/setup.sh 
#export LD_LIBRARY_PATH=/afs/cern.ch/sw/lcg/contrib/gcc/4.8.1/x86_64-slc6-gcc48-opt/lib64 
#source /afs/cern.ch/user/n/nkarast2/work/public/virtualenvs/py27/bin/activate

echo 'ORBIT_ROOT = '
echo ${ORBIT_ROOT}

# /afs/cern.ch/project/LIUsc/space_charge/Codes/mpich-3.0/bin/mpirun -np $2 ${ORBIT_ROOT}/bin/pyORBIT $1
/afs/cern.ch/project/LIUsc/space_charge/Codes/mpich2-1.4.1p1/bin/mpirun -np $2 ${ORBIT_ROOT}/bin/pyORBIT $1
