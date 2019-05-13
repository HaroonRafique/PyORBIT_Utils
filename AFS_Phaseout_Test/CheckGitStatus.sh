#!/bin/bash
# Useful git commands for checking the current status of a repository

if [ ! -n "$1" ]
  then
  	pyOrbit_dir=$PWD
  else
  	pyOrbit_dir=$1
fi

echo '*****************************************************'
echo
echo 'Checking Git status of PyORBIT repository located in:'
echo '-----------------------------------------------------'
echo $pyOrbit_dir
echo
echo 'Repository origin:'
echo '------------------'
git --git-dir $pyOrbit_dir/.git config --get remote.origin.url
echo
echo 'Available branches:'
echo '-------------------'
git --git-dir $pyOrbit_dir/.git branch -a | head
echo
echo 'Current branch:'
echo '---------------'
git --git-dir $pyOrbit_dir/.git branch | head
echo
echo 'Last commit:'
echo '------------'
git --git-dir $pyOrbit_dir/.git log | head -n3
echo
echo '*****************************************************'
echo
echo 'Checking Git status of PTC repository located in:'
echo '-------------------------------------------------'
pyOrbit_dir=$pyOrbit_dir/ext/PTC
echo $pyOrbit_dir
echo
echo 'Repository origin:'
echo '------------------'
git --git-dir $pyOrbit_dir/.git config --get remote.origin.url
echo
echo 'Available branches:'
echo '-------------------'
git --git-dir $pyOrbit_dir/.git branch -a | head
echo
echo 'Current branch:'
echo '---------------'
git --git-dir $pyOrbit_dir/.git branch | head
echo
echo 'Last commit:'
echo '------------'
git --git-dir $pyOrbit_dir/.git log | head -n3
echo
echo '*****************************************************'
