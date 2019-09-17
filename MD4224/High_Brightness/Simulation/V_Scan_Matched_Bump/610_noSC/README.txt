# 29.08.19 Haroon Rafique CERN BE-ABP-HSI
------------------------------------------------------------------------

Proton Synchrotron Injection Bump Closure MAD-X and PTC Simulation:
Case: 03_SBEND_With_Errors
- Using 4 x 20 cm SBENDs with no set angle
- Applying injection bump as a dipole and sextupole error on said quadrupoles

Running Instructions:
------------------------------------------------------------------------

1. ./madx-linux64 < Flat_File.madx
2. ./move_files.sh
3. python Plot_PTC_cf_MADX_Closed_Orbit.py
4. python PyORBIT_Table_Creator.py

What's in the folder?
------------------------------------------------------------------------

Inputs:

> Lattice/ contains the MAD-X lattice sequence, strength, aperture, and element files.
> MADX_Input/ contains the MAD-X input table for the injecion bump variables, generated in PS-injection-bump/From_Scratch/01_Create_MADX_Input_Table

> Flat_File.madx is the MAD-X input file and defines the simulation.
> clean_folder.sh removes junk after a simulation.
> move_files.sh moves files into relevent folders after a simulation.
> Plot_PTC_cf_MADX_Closed_Orbit.py plots the full closed orbit for each of the 50 steps in the MAD-X simulation, for MAD-X and PTC.
> PyORBIT_Table_Creator.py reads the contents of MADX_Tables/ and creates the corresponding PTC-PyORBIT readable tables in PyORBIT_Tables/.

Outputs:

> MADX_Tables/ contains the MAD-X output tables required for a PTC-PyORBIT simulation. These still require one step of conversion.
> PTC_Twiss/ contains the (MAD-X) PTC twiss output files for each step in the injection bump.
> MAD_Twiss/ contians the MAD-X twiss output files for each step in the injection bump.
> PTC-PyORBIT_Tables/ contains the converted MAD-X output PTC tables, now in a PTC-PyORBIT readable format.

> madx.ps output from MAD-X shows plots from PTC and MAD-X.
> PTC-PyORBIT_flat_file.flt is the PTC-PyORBIT readable flat file that defines the PTC lattice.
> PS.seq is the final optimised Proton Synchrotron sequence.
