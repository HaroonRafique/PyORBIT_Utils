if [ ! -n "$1" ]
  then
        echo "Usage: `basename $0` <path to PyOrbit directory>"
  else
  	pyorbit_dir=$1
fi

#activate environments
source $pyorbit_dir/customEnvironment.sh
source $pyorbit_dir/../virtualenvs/py2.7/bin/activate
export FFTW3_ROOT=`pwd`/fftw-3.3.5

#source ifort for compiling PTC
source ${pyorbit_dir}/../setup_ifort.sh

#build pyorbit
echo
echo "Building pyORBIT..."
echo "-------------------"
echo
cd $pyorbit_dir
make clean
make
cd ..

