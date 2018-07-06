#!/bin/bash
cd SC_1p3evs
condor_submit htcond.sub &
cd ../SC_1p6evs
condor_submit htcond.sub &
cd ../SC_1p9evs
condor_submit htcond.sub &
cd ../SC_2p3evs
condor_submit htcond.sub &
cd ../SC_2p6evs
condor_submit htcond.sub &
cd ../
