#!/usr/bin/python3
import serial
import configparser

def decode():
	
	
	settings = configparser.ConfigParser()
	settings.read('/home/pi/weather/settings.ini')
    
	#specifies serial port.	
	port = settings['Settings']['port']
    
	#specifies the baud rate.
	baudrate = int(settings['Settings']['baudrate'])
    
	#specifies the format to decode to.(ex.ASCII)
	decode_type = settings['Settings']['decode']
    
	#connects to the serial port
	weather_serial = serial.Serial(port, baudrate, parity='N', stopbits=1, timeout=None)
    
	#reads the output line from the serial port.
	output_line= weather_serial.readline()
    
	try:
		#decodes the serial output into a spcified form.
		decoded_line = output_line.decode(decode_type)
	except UnicodeDecodeError:
		print("ASCII Error need to restart script")
	
	decode_split = decoded_line.split()
    
	#creates a list of integers that will be sent to the engineering units
	# function. 
	final_decode = list(map(int, decode_split))
    
	return final_decode
