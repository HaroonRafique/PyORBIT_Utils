#!/bin/bash

#######################################################################
#   Script to build PTC-pyORBIT from Source with a custom Environment
#   from JB Lagrange Github depositories for pyORBIT and PTC
#   Use of this script:
#                     1) create a folder for the whole environment (ex:pyorbit_env)
#                     2) copy this script in this folder
#                     3) execute this script in this folder
#   After installing everything, you can check things by running the examples in py-orbit/examples/
#
#   NB: if you want to recompile pyORBIT after the first installation, you need to use:
#cd py-orbit
#source /cvmfs/projects.cern.ch/intelsw/psxe/linux/all-setup.sh
#source customEnvironment.sh
#make clean
#make
#######################################################################

#source ifort for compiling PTC
source /cvmfs/projects.cern.ch/intelsw/psxe/linux/all-setup.sh

#clone pyorbit version from github:
#~ git clone --branch=smooth_binning https://github.com/jbcern/py-orbit.git
git clone --branch=new-features https://github.com/hannes-bartosik/py-orbit.git

#clone PTC from github
cd py-orbit/ext
git clone --branch=analytical-space-charge https://github.com/jbcern/PTC.git
cd PTC
mkdir obj/
cd ../../..

#download and untar sources
echo "download and untar sources..."
curl http://www.mpich.org/static/downloads/3.2/mpich-3.2.tar.gz | tar xvz
curl https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz | tar xvz
curl http://zlib.net/fossils/zlib-1.2.11.tar.gz | tar xvz
curl http://www.fftw.org/fftw-3.3.5.tar.gz | tar xvz
curl https://pypi.python.org/packages/source/v/virtualenv/virtualenv-15.0.0.tar.gz  | tar xvz

#build python
echo "build python2.7..."
cd Python-2.7.12
./configure -prefix=`pwd`/..
make
make install
cd ..

#build zlib
echo "build zlib..."
cd zlib-1.2.11
./configure -prefix=`pwd`/..
make
make install
cd ..

#build mpi
echo "build mpich..."
cd mpich-3.2
./configure -prefix=`pwd`/.. --disable-fortran
make
make install
cd ..

#build fftw
echo "build fftw..."
cd fftw-3.3.5
./configure -prefix=`pwd`/.. --disable-fortran --enable-mpi MPICC=`pwd`/../bin/mpicc
make
make install
cd ..

#build python packages
echo "build python packages..."
source py-orbit/customEnvironment.sh
cd virtualenv-15.0.0
../bin/python setup.py install

cd ..
mkdir virtualenvs
cd virtualenvs
../bin/virtualenv py2.7 --python=../bin/python
cd py2.7/bin
source activate

#Add here the python packages you want to install
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
echo "DONE"
echo
cd ../../..

#build pyorbit
echo "Building pyORBIT..."
cd py-orbit
source customEnvironment.sh
make clean
make

