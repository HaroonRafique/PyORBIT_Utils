#!/bin/bash

#######################################################################
#   Script to build PTC-pyORBIT from Source with a custom Environment
#   Use of this script:
#                     1) execute this script in the folder of the PyOrbit environment 
#						 created by running installation script 01_install_PyOrbit_env.sh
#######################################################################

pyorbit_dir=py-orbit_frozenSC_20170731

#source ifort for compiling PTC
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/setup.sh
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/ifortvars.sh intel64
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/iccvars.sh intel64

#clone pyorbit version from github:
git clone --branch=new-features https://github.com/hannes-bartosik/py-orbit.git $pyorbit_dir

#clone PTC from github
cd $pyorbit_dir/ext
git clone --branch=analytical-space-charge https://github.com/hannes-bartosik/PTC.git
cd PTC
mkdir obj/
cd ../../..
#enable the compilation of PTC and disable compilation of ecloud
sed -i 's/.*#DIRS += .\/PTC*/DIRS += .\/PTC/' $pyorbit_dir/ext/Makefile
sed -i 's/.*DIRS += .\/ecloud*/#DIRS += .\/ecloud/' $pyorbit_dir/ext/Makefile


#NOW COMPILE

#activate environments
source $pyorbit_dir/customEnvironment.sh
source virtualenvs/py2.7/bin/activate

#build pyorbit
echo "Building pyORBIT..."
cd $pyorbit_dir
source customEnvironment.sh
make clean
make

