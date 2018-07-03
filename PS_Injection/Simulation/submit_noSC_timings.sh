#!/bin/bash
cd 1_NoSC_Core
condor_submit htcond.sub &
cd ../2_NoSC_Core
condor_submit htcond.sub &
cd ../4_NoSC_Core
condor_submit htcond.sub &
cd ../8_NoSC_Core
condor_submit htcond.sub &
cd ../16_NoSC_Core
condor_submit htcond.sub &
cd ../
