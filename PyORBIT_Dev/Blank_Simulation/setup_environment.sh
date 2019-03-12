#!/bin/bash
echo
echo '******************************************'
echo 'Set up virtual environment for PTC-PyORBIT'
echo '------------------------------------------'
echo
#~ source /afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/py-orbit_frozenSC_20170731/customEnvironment.sh
source /afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/py-orbit/customEnvironment.sh
echo
echo '******************************************'
echo "customEnvironment done"
echo '------------------------------------------'
echo
source /afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/virtualenvs/py2.7/bin/activate
echo '******************************************'
echo "python packages charged"
echo '------------------------------------------'
echo
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/setup.sh
echo
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/ifortvars.sh intel64
echo
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/iccvars.sh intel64
echo
echo '******************************************'
echo "ifort charged (necessary for running)"
echo '------------------------------------------'
echo

