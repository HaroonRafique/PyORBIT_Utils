
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
