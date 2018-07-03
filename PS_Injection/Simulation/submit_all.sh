#!/bin/bash
cd 1p3evs
condor_submit htcond.sub &
cd ../1p6evs
condor_submit htcond.sub &
cd ../1p9evs
condor_submit htcond.sub &
cd ../2p3evs
condor_submit htcond.sub &
cd ../2p6evs
condor_submit htcond.sub &
cd ../
