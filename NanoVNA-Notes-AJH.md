
# Notes on measuring Z-Match Antenna Tuner with NanoVNA-4

## The Hardware

* The QRP Z-Match tuner
  * <https://www.amazon.com/dp/B0CGR2TCN3>
* NanoVNA-H4
  * <https://www.amazon.com/dp/B083PQ4RXZ>

----

## Software and Documents

* Scikit-RF
  * <https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9632487>
  * <https://github.com/scikit-rf/scikit-rf_workshop>
  * <https://scikit-rf.readthedocs.io/en/latest/>
  * <https://github.com/scikit-rf/scikit-rf>

* NanoVNA-Tools
  * <https://github.com/Ho-Ro/nanovna-tools>
  * uses scikit-rf for calculations

* NanoVNASaver
  * <https://github.com/NanoVNA-Saver/nanovna-saver>
  * <https://nanovna.com/?page_id=90>

* VNA Primer and Labs
  * <https://download.tek.com/document/70W_60918_0_Tek_VNA_PR.pdf>
  * <https://anlage.umd.edu/Anritsu_understanding-vna-calibration.pdf>
  * <https://pages.hmc.edu/mspencer/e157/fa24/slides/11.pdf>
  * <https://pages.hmc.edu/mspencer/e157/fa24/labs/03.pdf>
  * <https://www.allaboutcircuits.com/technical-articles/introduction-to-vna-calibration-techniques/>

* Touchstone format
  * <https://helpfiles.keysight.com/csg/N1930xB/FilePrint/SnP_File_Format.htm>

* Conda environment for NanoVNA-saver on MacOS 15.2/Apple Silicon

````sh
    git clone https://github.com/NanoVNA-Saver/nanovna-saver
    conda create -n nanovna python=3.11 numpy scipy pyserial Cython
    conda activate nanovna
    # conda-forge does not have PyQt6, so use PyPI and pip
    python  -m pip install pyqt6 pyqt6-sip sip
    python  -m pip install setuptools setuptools-scm

    conda install skikit-rf ipython matplotlib
    conda install pyvisa-py

    git clone https://github.com/Ho-Ro/nanovna-tools/
````

* running NanoVNASaver

````sh
    python nanovna-saver.py
````

----

## What I learned

### Surprize #1

* scikit-rf _does not_ support the NanoVNA-H4 control protocol, only the NanoVNA-V2 is supported
  * scikit-rf does support Touchstone format (good!)

* NanoVNASaver does support the NanoVNA-H4, but it is a GUI app with no scripting or automation, so lots of button pushing and typing for each measurement
  * NanoVNASaver can save measurements in Touchstone format

* NanoVNA Tools
  * supports NanoVNA-H4 control protocol (yay!)
  * supports Touchstone format (yay!)
  * does not handle calibration
  * uses scikit-rf for underlying calculations

### Surprize #2

* \$$k VNAs like HP and Anritsu are 2-port, 2-path VNAs
  * can measure all four 2-port parameter for each sweep

* \$$ NanoVNA is "2-port, 1-path" (aka "3-receiver") architecture
  * It can measure S11 and S21 directly -- reflected and through, but not S12 and S22
  * workarounds
    * reverse DuT to measure S12 and S22  
    * if DUT is symmetric can use "flip-fake" -- S22 = S11 and S12 = S21
      * Z-match tuner is not symmetric
  * example: <https://scikit-rf.readthedocs.io/en/v1.3.0/examples/metrology/NanoVNA_V2_4port-splitter.html>

* Figure 7 in the Tek document shows this clearly

### Surprize #3

* NanoVNA always returns uncalibrated ("raw") measurements
  * scikit-rf supports calibrating raw measurements with Touchstone files of calibrations runs
  * calibration runs are called SOLT -- short, open, load, through
    * include test cables, aka "fixtures"
    * Example: <https://scikit-rf.readthedocs.io/en/v1.3.0/examples/metrology/Calibration%20With%20Three%20Receivers.html>

----

## Measuring the Z-Match Tuner

* Z-match tuner details
  * two variable caps, 11 settings labeled 0 - 10,
  * two-position switch, low and high impedance antenna - instructions say to start with high, switch to low if needed
  * full measurement set 11x11x2x2  = 484 sweeps (!)  forward/reverse direction, high/low impedance
  * I can do about 1 measurement/min with NVNASaver (lots of button pushes, typing filenames, ...)  -- that's 8 hours!  
  * automated script would speed that up considerably

* What did Aaron do?
  * only used positions 1, 3, 5, 7, 9 and high impedance only
  * no detents, so eyeballed settings
  * 5x5x2 = 50 measurements (< 1 hr, whew!)
  * sweep 1 MHz to 30 MHz
  * 505 frequencies -- 5 segments of 101 frequencies
    * 57.54 kHz steps
    * NVNA will only do 101 point sweep  -- automated by NanoVNASaver
    * repeat sweep 5 times, discard worst, average remaining 4  -- automated by NanoVNASaver
  * forward SOLT calibration

* What could be done better
  * better fixturing
    * cables supplied with NanoVNA are rigid, get some more flexible cables
    * SMA connectors tend to loosen, had to check tightness frequently
    * HP manual suggests using SMA torque wrench for repeatable connections between cal and test phases - \$28 (ebay) - \$350 (Pasternak)

  * tradeoff - repeatability of settings vs. reversing connections
    * Option 1: 25 forward, then 25 reverse  -- settings might not be the same for forward and reverse, only one reconnections
    * Option 2: reverse each for setting -- settings are the same, but 25 reconnections
    * Option 3: use transfer (DPDT) coaxial switch for reverse connection -- used RF switches are >$100
  * I used Option 2

----

## Further thoughts

* Next steps
  * write scikit-rf scripts
    . to calibrate measurements
    . merge forward and reverse measurements to make full 2-port Touchstone files
    . combine with antenna S11 measurement
    . select optimal tuner settings
  * write NanoVNA Tools scripts to automate measurements
  * try it out with a real antenna and transmitter!

* Questions
  * how repeatable are these measurements?
  * are my measurements good for other samples of Z-match tuner?
  * are five settings of each adjustment enough?
  * are 505 frequencies enough?
    * focus on ham band frequencies?
    * focus on exact frequencies for FT8, PSK31, ...?
  * how critical is fixturing for HF (< 30 MHz)?  Most of the writeups on VNA assume S-band and above.

----
Aaron Heller <ajheller@gmail.com> -- 13 Jan 2025
