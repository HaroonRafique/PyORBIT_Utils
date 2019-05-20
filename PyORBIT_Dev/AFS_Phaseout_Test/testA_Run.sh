#!/bin/bash

#######################################################################
#   Script to test PTC-PyORBIT on EOS
#######################################################################
# The following files should be present in the directory $PATHTEST for
# the examples to run
#
# setup_ifort.sh
# CheckGitStatus.sh
#
# these files can be found here:
# runfiles="/afs/cern.ch/user/p/pyorbit/public/pyorbit_examples_repository/AFS_Phaseout_Test"
# Let's assume you already have these from the examples repository
runfiles=$(pwd)

PATHTEST="/afs/cern.ch/work/p/pyorbit/private/AFS_Phaseout_Test_5"

# The script will stop on the first error 
set -e

# Create the test folder
mkdir $PATHTEST
cd $PATHTEST

# copy required files
cp $runfiles/setup_ifort.sh .
cp $runfiles/CheckGitStatus.sh .

# Source intel fortran libraries
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/setup.sh
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/ifortvars.sh intel64
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2019/compilers_and_libraries_2019.1.144/linux/bin/iccvars.sh intel64

# download and untar sources
echo "download and untar sources..."
curl http://www.mpich.org/static/downloads/3.2/mpich-3.2.tar.gz | tar xvz
curl https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz | tar xvz
curl http://zlib.net/fossils/zlib-1.2.11.tar.gz | tar xvz
curl http://www.fftw.org/fftw-3.3.5.tar.gz | tar xvz
curl https://files.pythonhosted.org/packages/eb/74/724d0dcc1632de285499ddd67035dd9313b84c28673add274b9c151dbb65/virtualenv-15.0.0.tar.gz | tar xvz

# build python
echo "build python2.7..."
cd Python-2.7.12
./configure -prefix=`pwd`/..
make
make install
cd ..

# build zlib
echo "build zlib..."
cd zlib-1.2.11
./configure -prefix=`pwd`/..
make
make install
cd ..

# build mpi
echo "build mpich..."
cd mpich-3.2
./configure -prefix=`pwd`/.. --disable-fortran
make
make install
cd ..

# build fftw
echo "build fftw..."
cd fftw-3.3.5
./configure -prefix=`pwd`/.. --disable-fortran --enable-mpi MPICC=`pwd`/../bin/mpicc
make
make install
cd ..

# build python packages
echo "build python packages..."

export PATH=`pwd`/bin/:$PATH

export PYTHON_VERSION=`python -c "from distutils import sysconfig; print sysconfig.get_config_var('VERSION');"`
echo "Python version is $PYTHON_VERSION"

PYTHON_LIB_DIR=`python -c "from distutils import sysconfig; print sysconfig.get_config_var('LIBPL');"`
if [ -f $PYTHON_LIB_DIR/libpython${PYTHON_VERSION}.a ]
   then
	export PYTHON_ROOT_LIB=$PYTHON_LIB_DIR/libpython${PYTHON_VERSION}.a
	LIB_TYPE=static
   else
	export PYTHON_ROOT_LIB="-L $PYTHON_LIB_DIR -lpython${PYTHON_VERSION}"
	LIB_TYPE=dynamic
fi

echo "Found python library: ${PYTHON_LIB_DIR} will use $LIB_TYPE library"

export PYTHON_ROOT_INC=`python -c "from distutils import sysconfig; print sysconfig.get_config_var('INCLUDEPY');"`
echo "Found Python include directory: $PYTHON_ROOT_INC"

export PYTHONPATH=${PYTHONPATH}:${ORBIT_ROOT}/py:${ORBIT_ROOT}/lib
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${ORBIT_ROOT}/lib

cd virtualenv-15.0.0
../bin/python setup.py install

# Make and source virtual environment
cd ..
mkdir virtualenvs
cd virtualenvs
../bin/virtualenv py2.7 --python=../bin/python
cd py2.7/bin
source $PATHTEST/virtualenvs/py2.7/bin/activate

echo "Installing Python packages"
echo "--------------------------"

# Install python packages
echo "installing numpy..."
./pip install numpy
echo "installing scipy..."
./pip install scipy
echo "installing ipython..."
./pip install ipython
echo "installing matplotlib..."
./pip install matplotlib
echo "installing h5py..."
./pip install h5py
echo "installing imageio"
./pip install imageio
echo "DONE"
echo
cd ../../..

# PyORBIT installation
pyorbit_dir=py-orbit

# clone pyorbit version from github:
git clone --branch=master https://github.com/hannes-bartosik/py-orbit.git $pyorbit_dir

# clone PTC from github
cd $pyorbit_dir/ext
git clone --branch=master https://github.com/hannes-bartosik/PTC.git
cd PTC
mkdir obj/
cd ../../..
# enable the compilation of PTC and disable compilation of ecloud
sed -i 's/.*#DIRS += .\/PTC*/DIRS += .\/PTC/' $pyorbit_dir/ext/Makefile
sed -i 's/.*DIRS += .\/ecloud*/#DIRS += .\/ecloud/' $pyorbit_dir/ext/Makefile

# activate environments
source $pyorbit_dir/customEnvironment.sh
source $pyorbit_dir/../virtualenvs/py2.7/bin/activate

# Compile PyORBIT
echo
echo "Building pyORBIT..."
echo "-------------------"
echo
cd $pyorbit_dir
make clean
make
echo "pyORBIT Buit"
echo "-------------------"

echo "Cloning pyORBIT examples repository"
echo "-----------------------------------"

cd $PATHTEST
mkdir examples
cd examples
git clone https://gitlab.cern.ch/pyorbit/pyorbit_examples.git .

cd $PATHTEST
test_run_dir='Simulation_Test_Runs'
mkdir $test_run_dir
cd $test_run_dir

testdir=`date +%Y%m%dT%H%M%S`
mkdir $testdir
cd $testdir

echo "Duplicate PS example for HTCondor submission"
echo "--------------------------------------------"

# Function creates N duplicate folders and submits N jobs to HTCondor
Duplicate_and_Submit(){
	
	for (( c=1; c<=$1; c++ )) ; do
		echo "Duplicating PS_1p4GeV_Injection into directory $c"
		cp -r $PATHTEST/examples/Machines/PS/PS_1p4GeV_Injection $c
		cd $c
		
		echo "Edit setup_environment.sh to point to this installed version of PyORBIT"
		echo "-----------------------------------------------------------------------"
		old_po_dir="/afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/py-orbit"
		new_po_dir="$PATHTEST/py-orbit"
		sed -i "s|pyOrbit_dir=$old_po_dir|pyOrbit_dir=$new_po_dir|" setup_environment.sh
				
		echo "Submitting Condor Job"
		echo "---------------------"
		condor_submit htcond.sub		
		cd ..
		
	done
}

#####################################################
# Change No of duplicate HTCondor simulations here: #
#####################################################
Number_of_duplicates=3
Duplicate_and_Submit $Number_of_duplicates

# run local job
echo "Starting Local Job"
echo "---------------------"

cp -r $PATHTEST/examples/Machines/PS/PS_1p4GeV_Injection $PATHTEST/$test_run_dir/$testdir

cd $PATHTEST/$test_run_dir/$testdir/PS_1p4GeV_Injection

# Edit the setup_environment file
old_po_dir="/afs/cern.ch/user/p/pyorbit/public/PyOrbit_env/py-orbit"
new_po_dir="$PATHTEST/py-orbit"
sed -i "s|pyOrbit_dir=$old_po_dir|pyOrbit_dir=$new_po_dir|" setup_environment.sh

# setup environment manually
./START_local.sh pyOrbit.py 4
