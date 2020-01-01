#!/bin/bash

#######################################################################
#   Script to build PTC-pyORBIT from Source with a custom Environment
#   
#   Use of this script:
#                     1) create a folder for the whole environment (ex:pyorbit_env)
#                     2) copy this script in this folder
#                     3) execute this script in this folder
#
#######################################################################

#source ifort for compiling PTC
source setup_ifort.sh

#download and untar sources
echo "download and untar sources..."
curl http://www.mpich.org/static/downloads/3.2/mpich-3.2.tar.gz | tar xvz
curl https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz | tar xvz
curl http://zlib.net/fossils/zlib-1.2.11.tar.gz | tar xvz
curl http://www.fftw.org/fftw-3.3.5.tar.gz | tar xvz
curl https://files.pythonhosted.org/packages/eb/74/724d0dcc1632de285499ddd67035dd9313b84c28673add274b9c151dbb65/virtualenv-15.0.0.tar.gz | tar xvz

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
source _setPythonPaths.sh
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
echo "installing imageio"
./pip install imageio
echo "installing pandas"
./pip install pandas

echo "DONE"
echo
cd ../../..
