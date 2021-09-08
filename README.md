# Gen2 UHF RFID Reader
This is a Gen2 UHF RFID Reader. It is able to identify commercial Gen2 RFID Tags with FM0 line coding and 40kHz data rate (BLF), and extract their EPC. It requires USRPN200 and a RFX900 or SBX daughterboard.  

The project is based on the RFID Gen2 Reader available at https://github.com/ransford/gen2_rfid. The reader borrows elements from the software developed by Buettner, i.e. Data flow: Gate -> Decoder -> Reader as well as the conception regarding the detection of the reader commands. CRC calculation and checking functions were also adapted from https://www.cgran.org/browser/projects/gen2_rfid/.

### Implemented GNU Radio Blocks:

- Gate : Responsible for reader command detection.  
- Tag decoder : Responsible for frame synchronization, channel estimation, symbol period estimation and detection.  
- Reader : Create/send reader commands.

## Installation

## **This script has been modified and only supports up to Ubuntu 18.X due to python 2.7, qt4 and deprecation of GNURadio 3.7.X on Ubuntu 20.04.**

- Install log4cpp (http://log4cpp.sourceforge.net/)
- Using build-script will automatically fetch, build and install the following:
> UHD driver + GNU Radio + SoapySDR + Gen2 UHF RFID Reader +
> rtl-sdr + gr-osmosdr + gr-iqbal + hackrf + bladeRF + airspyone_host

- Grant permissions 
```sh
chmod a+x ./build-script
```
- Execute with the following flags 
```sh
./build-script -ja -v
```

Usage: build-script [--help|-h] [-v|--verbose] [-jN] [-ja] 
                      [-l|--logfile logfile ] [-u|--users ulist] [-m] funcs

-m             - Use HEAD of *master* branch, rather than *maint*.

-v|--verbose   - turn on verbose logging to stdout

-jN            - have make use N concurrent jobs

-ja            - have make use N concurrent jobs with auto setting of N
                 (based on number of cpu cores on build system)
                 

-u|--users ul  - add comma-separated users to 'usrp' group in addition
                 to calling user ( $USER )

-l|--logfile lf - log messages to 'lf'
-ut <tag>       - set tag for UHD checkout to <tag>
-ucf <ucflags>  - set UHD CMake flags to <ucflags>
-gt <tag>       - set tag for Gnu Radio checkout to <tag>
-gcf <gcflags>  - set Gnu Radio CMake flags to <gcflags>
-e|--extras     - add an item to "extras" to be built after Gnu Radio/UHD/gs-osmosdr

Available funcs:

all             - do all functions
prereqs         - install prerequisites
gitfetch        - use GIT to fetch Gnu Radio and UHD
uhd_build       - build only UHD
firmware        - fetch firmware/FPGA
gnuradio_build  - build only Gnu Radio
mod_groups      - modify the /etc/groups and add user to group 'usrp'
mod_udev        - add UDEV rule for USRP1
mod_sysctl      - modify SYSCTL for larger net buffers
SoapySDR        - fetch and build SoapySDR
G2RFID          - build Gen2 UHF RFID Reader

## Configuration

- Set USRPN200 address in apps/reader.py (default: 192.168.10.2)
- Set frequency in apps/reader.py (default: 910MHz)
- Set tx amplitude in apps/reader.py (default: 0.1)
- Set rx gain in apps/reader.py (default: 20)
- Set maximum number of queries in include/global_vars.h (default:1000)
- Set number of inventory round slots in include/global_vars.h (default: 0)

## How to run

- Real time execution:  
If you use an SBX daughterboard uncomment  #self.source.set_auto_dc_offset(False) in reader.py file
cd Gen2-UHF-RFID-Reader/gr-rfid/apps/    
sudo GR_SCHEDULER=STS nice -n -20 python ./reader.py     
After termination, part of EPC message (hex value of EPC[104:111]) of identified Tags is printed.  

- Offline:  
    Change DEBUG variable in apps/reader.py to TRUE (A test file already exists named file_source_test).  
    The reader works with offline traces without using a USRP.  
    The output after running the software with test file is:  
    
    | Number of queries/queryreps sent : 71  
    | Current Inventory round : 72  

    | Correctly decoded EPC : 70  
    | Number of unique tags : 1  
    | Tag ID : 27  Num of reads : 70  
 
## Logging

- Configuration file : /home/username/.gnuradio/config.conf  
    Edit the above file and add the following lines  

    [LOG]  
    debug_file = /PathToLogFile/Filename  
    debug_level = info  
    
    Logging may cause latency issues if it is enabled during real time execution!

## Debugging  

The reader may fail to decode a tag response for the following reasons

1) Latency: For real time execution you should disable the output on the terminal. If you see debug messages, you should either install log4cpp or comment the corresponding lines in the source code e.g., GR_LOG_INFO(d_debug_logger, "EPC FAIL TO DECODE");

2) Antenna placement. Place the antennas side by side with a distance of 50-100cm between them and the tag 2m (it can detect a tag up to 6m) away facing the antennas.

3) Parameter tuning. The most important is self.ampl which controls the power of the transmitted signal (takes values between 0 and 1).

If the reader still fails to decode tag responses, uncomment the following line in reader.py file

 #self.connect(self.source, self.file_sink_source)

Run the software for a few seconds (~5s). A file will be created in misc/data directory named source. This file contains the received samples. You can plot the amplitude of the received samples using the script located in misc/code folder. The figure should be similar to the .eps figure included in the folder. Plotting the figure can give some indication regarding the problem. You can also plot the output of any block by uncommenting the corresponding line in the reader.py file. Output files will be created in misc/data folder:

- /misc/data/source  
- /misc/data/matched_filter  
- /misc/data/gate 
- /misc/data/decoder  
- /misc/data/reader

Useful discussions on software issues:

https://github.com/nkargas/Gen2-UHF-RFID-Reader/issues/1

https://github.com/nkargas/Gen2-UHF-RFID-Reader/issues/4

https://github.com/nkargas/Gen2-UHF-RFID-Reader/issues/10

    
## Hardware:

  - 1x USRPN200/N210  
  - 1x RFX900/SBX daughterboard  
  - 2x circular polarized antennas  

## Tested on:
  Ubuntu 18.04.5 LTS 64-bit  
  GNU Radio 3.7.14
  
## If you use this software please cite:
N. Kargas, F. Mavromatis and A. Bletsas, "Fully-Coherent Reader with Commodity SDR for Gen2 FM0 and Computational RFID", IEEE Wireless Communications Letters (WCL), Vol. 4, No. 6, pp. 617-620, Dec. 2015. 

## Contact:
  Nikos Kargas (email: karga005@umn.edu)  

This research has been co-financed by the European Union (European Social Fund-ESF) and Greek national funds through the Operational Program Education and Lifelong Learning of the National Strategic Reference Framework (NSRF) - Research Funding Program: THALES-Investing in knowledge society through the European Social Fund.
