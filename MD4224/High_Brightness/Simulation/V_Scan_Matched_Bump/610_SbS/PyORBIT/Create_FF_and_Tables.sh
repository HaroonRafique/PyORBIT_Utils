#!/bin/bash
cd ../
# AFS MAD-X
#/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < Flat_file.madx
# Local MAD-X
./madx-linux64 < Flat_file.madx
./move_files.sh
python Plot_PTC_cf_MADX_Closed_Orbit.py
python PyORBIT_Table_Creator.py
mv PTC-PyORBIT_flat_file.flt PyORBIT
cd PyORBIT
