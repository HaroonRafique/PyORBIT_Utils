if [ ! -n "$1" ]
  then
        echo "Usage: `basename $0` <path to PyOrbit directory>"
  else
  	pyorbit_dir=$1
fi

#source ifort for compiling PTC
source ${pyorbit_dir}/../setup_ifort.sh

#activate environments
source $pyorbit_dir/customEnvironment.sh
source $pyorbit_dir/../virtualenvs/py2.7/bin/activate

#build pyorbit
echo
echo "Building pyORBIT..."
echo "-------------------"
echo
cd $pyorbit_dir
make clean
make

