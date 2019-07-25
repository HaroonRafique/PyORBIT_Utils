#!/bin/bash
cd MADX
# AFS MAD-X
#/afs/cern.ch/eng/sl/MAD-X/pro/releases/5.02.00/madx-linux64 < Flat_file.madx
# Local MAD-X
./madx-linux64 < Flat_file.madx
cp PTC-PyORBIT_flat_file.flt ../
cd ../Tables
python PyORBIT_Table_Creator.py

