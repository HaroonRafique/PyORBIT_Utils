#!/bin/bash
cd 1_SC_Core
condor_submit htcond.sub &
cd ../2_SC_Core
condor_submit htcond.sub &
cd ../4_SC_Core
condor_submit htcond.sub &
cd ../8_SC_Core
condor_submit htcond.sub &
cd ../16_SC_Core
condor_submit htcond.sub &
cd ../
