# Weather measurements

The purpose of this Repository is to create a weather module which is compatible with a Young's Weather Station set-up in order to calculate 
and upload weather measurements. 

The settings.ini file should be the only file the user needs to access once I have finished adding the callout for new equations 
which will allow the user to simply input the appropriate equation into the Equations section and it will be calculated. 

If you are using a Young's weather station with the 32500 Board installed this one is geared towards the outputs of that board, this
repository also focuses on the ASCII and NMEA outputs from the board but is able to accept new measurements if need be. 

Also note that a serial port was used to read in the data from the weather station.

This package should allow for the addition of multiple inputs, such as a usb input or another serial port. 
