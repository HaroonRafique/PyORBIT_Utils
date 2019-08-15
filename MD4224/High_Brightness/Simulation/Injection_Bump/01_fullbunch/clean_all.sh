#!/bin/bash
cd MADX
. clean_all.sh
cd ..
rm Tables/*.dat
rm Tables/*.ptc
. clean_run.sh
. clean_junk.sh
rm -r Condor_Logfiles
