#!/bin/bash

export PYTHONPATH=${PYTHONPATH}:${ORBIT_ROOT}/py:${ORBIT_ROOT}/lib:${ORBIT_ROOT}/virtualenvs/py2.7/bin/lib/python2.7/site-packages/numpy
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${ORBIT_ROOT}/lib
module load mpi/mpich-x86_64
source /home/HR/Documents/PyORBIT_HB_New_Features/py-orbit/customEnvironment.sh
source /home/HR/Documents/PyORBIT_HB_New_Features/virtualenvs/py2.7/bin/activate


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

# /afs/cern.ch/project/LIUsc/space_charge/Codes/mpich-3.0/bin/mpirun -np $2 ${ORBIT_ROOT}/bin/pyORBIT $1
mpirun -np $2 ${ORBIT_ROOT}/bin/pyORBIT $1
