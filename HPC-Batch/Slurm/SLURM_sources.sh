#!/bin/bash
source /hpcscratch/user/harafiqu/PyORBIT/virtualenvs/py2.7/bin/activate
source /hpcscratch/user/harafiqu/PyORBIT/py-orbit/customEnvironment.sh
VIRT_PY_DIR='/hpcscratch/user/harafiqu/PyORBIT/virtualenvs/py2.7/bin'
export ORBIT_ROOT='/hpcscratch/user/harafiqu/PyORBIT/py-orbit'
cd ${VIRT_PY_DIR}
source activate
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/all-setup.sh

