#!/usr/bin/python3
import math
import warnings
import time
import configparser
import serial

class WeatherUtils:
	
    ############## Engineering Data Calculations ################
	def engr(units): 
		Eng_data={}
		
		#sets the CongfigParser class equal to settings
		settings = configparser.ConfigParser()

        #reads in the ini file containing the defaults
		settings.read('/home/pi/weather/settings.ini')

		#specifies the Young weather station output type.
		output = settings['Settings']['Young_out']
		
		#specifices the secondary port that the pi should read from.
		sec_port = settings['Settings']['sec_port']
		
		#puts the entire Equations section of the ini file into a useable dictionary
		new_eqns = dict(settings['Equations'])
		
		if output == 'ASCII':
			#wind speed (mph)
			Eng_data["windspeedmph"] = 0.1097 * units[0]
			
			# wind direction (degrees)
			Eng_data["winddir"] = units[1]/10
			
			#temperature (Celsius)
			Eng_data["tempf"] = WeatherUtils.C2F((units[2]-2000)/40)
			
			#Relative humidity(%)
			Eng_data["humidity"] = 0.025 * units[3]
			
			#Station Barometric pressure (InHg)
			Eng_data["baro_st"] = WeatherUtils.HPa2In((0.15 * units[4]) + 500)
			
			#Solar radiation (W/m2)
			Eng_data["solarradiation"] = 0.3125 * units[5]
			
			#Compass direction
			Eng_data["comp_dir"] = units[6] / 10
			
			#Adds time since Epoch
			Eng_data["time"] = time.time()
			
			#Calculates the Dew point temperature. 
			Eng_data["dewptf"] = ((Eng_data["humidity"]/100)**(1/8)) * (112 + 0.9*Eng_data["tempf"]) + 0.1 * Eng_data["tempf"] - 112
			
			##Look for new equations from ini file
			#for key,value in new_eqns.items():
				##have python evaluate the strings in the dictionary new_eqns
				#eval_input = eval(value)
    
				##Check to see if the input from ini file is a string.
				#type_check_str = isinstance(eval_input,str)
    
				##convert the output of isinstance to a string to check versus in 
				##the conditional.
				#type_check_str = str(type_check_str)
    
				##If any of the keys are strings check to see if they match any of the
				##weather outputs that are expected to be text for Weather Underground
				##uploading.
				#if type_check is 'True':
					#if key == 'weather':
					##insert this key into the engineering data dictionary
					#eng_data[key] = x
					#if key == 'clouds':
					##insert this key into the engineering data dictionary 
					#eng_data[key] = x
				#else:
					##check to see if evaluating the strings returned an integer
					#type_check_int = isinstance(eval_input, int)
        
					##convert to string for checking in conditional
					#type_check_int = str(type_check_two)
        
					##if an int then add to the engineering data dictionary.
					#if type_check_int is 'True':
					##add any of the evaluated inputs (eval_input) to the engineering 
					##data dictionary with its corresponding key.
					#eng_data[key] = eval_input
        
					##check to see if the evaluated string is a float.
					#type_check_float = isinstance(eval_input,float)
        
					##if a float then add to the engineering data dictionary. 
					#if type_check_float is 'True':
					##add inputs to the engineering data dictionary.
					#eng_data[key] = eval_input

			
			return Eng_data 
		
			
		elif output == 'ASCII_L':
			
			#wind speed (mph)
			Eng_data["windspeedmph"] = 0.1097 * units[0]
			
			# wind direction (degrees)
			Eng_data["winddir"] = units[1]/10
			
			#temperature (Celsius)
			Eng_data["tempf"] = WeatherUtils.C2F((units[2]-2000)/40)
			
			#Relative humidity(%)
			Eng_data["humidity"] = 0.025 * units[3]
			
			#Station Barometric pressure (InHg)
			Eng_data["baro_st"] = WeatherUtils.HPa2In((0.15 * units[4]) + 500)
			
			#Solar radiation (W/m2)
			Eng_data["solarradiation"] = 0.3125 * units[5]
			
			#Compass direction
			Eng_data["comp_dir"] = units[6] / 10
			
			#Adds time since Epoch
			Eng_data["time"] = time.time()
			
			#Calculates the Dew point temperature. 
			Eng_data["dewptf"] = ((Eng_data["humidity"]/100)**(1/8)) * (112 + 0.9*Eng_data["tempf"]) + 0.1 * Eng_data["tempf"] - 112
			
			#Adds the secondary ports output to the dictionary of eng_data
			#If this is a serial the data may need to be run through the decoder module.
			weather_serial_sec = serial.Serial(sec_port)
			Eng_data["lake_temp"] = weather_serial_sec.readline()
			
			#looks for the addition of new equations.
			if len(new_eqns) is not 0:
				for key, value in new_eqns.items():
					Eng_data[key] = value
					Eng_data[key] = eval(Eng_data[key])
			
			return Eng_data
		
		elif output == 'NMEA':
			
			#wind speed (mph)
			Eng_data["windspeedmph"] = 0.1097 * units[0]
			
			# wind direction (degrees)
			Eng_data["winddir"] = units[1]/10
			
			#Station Barometric pressure (InHg)
			Eng_data["baro_st"] = WeatherUtils.HPa2In((0.15 * units[2]) + 500)
			
			#temperature (Celsius)
			Eng_data["tempf"] = WeatherUtils.C2F((units[3]-2000)/40)
			
			#Relative humidity(%)
			Eng_data["humidity"] = 0.025 * units[4]
			
			#Adds time since Epoch
			Eng_data["time"] = time.time()
			
			#Calculates the Dew point temperature.
			Eng_data["dewptf"] = ((Eng_data["humidity"]/100)**(1/8)) * (112 + 0.9*Eng_data["tempf"]) + 0.1 * Eng_data["tempf"] - 112
			
			#looks for the addition of new equations.
			if len(new_eqns) is not 0:
				for key, value in new_eqns.items():
					Eng_data[key] = value
					Eng_data[key] = eval(Eng_data[key])
			
			return Eng_data
		
		elif output == 'NMEA_L':
			
			#wind speed (mph)
			Eng_data["windspeedmph"] = 0.1097 * units[0]
			
			# wind direction (degrees)
			Eng_data["winddir"] = units[1]/10
			
			#Station Barometric pressure (InHg)
			Eng_data["baro_st"] = WeatherUtils.HPa2In((0.15 * units[2]) + 500)
			
			#temperature (Celsius)
			Eng_data["tempf"] = WeatherUtils.C2F((units[3]-2000)/40)
			
			#Relative humidity(%)
			Eng_data["humidity"] = 0.025 * units[4]
			
			#Adds time since Epoch
			Eng_data["time"] = time.time()
			
			#Calculates the Dew point temperature.
			Eng_data["dewptf"] = ((Eng_data["humidity"]/100)**(1/8)) * (112 + 0.9*Eng_data["tempf"]) + 0.1 * Eng_data["tempf"] - 112
			
			#Adds the secondary ports output to the dictionary of eng_data
			#If this is a serial the data may need to be run through the decoder module.
			weather_serial_sec = serial.Serial(sec_port)
			Eng_data["lake_temp"] = float(weather_serial_sec.readline()) #do we need or want to make sure this is float.
			
			#looks for the addition of new equations.
			if len(new_eqns) is not 0:
				for key, value in new_eqns.items():
					Eng_data[key] = value
					Eng_data[key] = eval(Eng_data[key])
			
			return Eng_data
		
		else:  
			
			return ('Available engineering unit calculations are ASCII, ASCII_L, NMEA and NMEA_L') 
    
################## Barometric Pressure Calculation ##############
	def baro_st_to_sl(n, alg='default'):
		#calls in the last Barometric pressure measurement taken at the... 
		#station. 
		baro_station=n['baro_st']
		#calls out the wanted algorithm for the barmetric factor calculations.
		algo = alg 
		#sets the configparser class ConfigParser equal to settings to ...
		#allow for the reading of the settings.ini file. 
		settings = configparser.ConfigParser()
		
		#opens and reads the ini file. 
		settings.read('/home/pi/weather/settings.ini')
		
		#sets the elevation of the weather station. 
		Elevation = float(settings['Settings']['Elevation']) 
		
		#calls out the barometric factor equation. 
		baro_factor = WeatherUtils.baro_factor(Elevation, algo)
		
		#calculates the barometric pressure relative to sea level. 
		cal_value = baro_factor*baro_station
        
		return cal_value
    
################ Barometric Factor equations #####################
	##baro_factor will be called out in the baro_st_to_sl equation
	#converts the barometric pressure from the barometric pressure...
	# relative to the station to the barometric pressure relative to ...
	#sea level. 
	def baro_factor(Elevation, algo):
		Tb = 288
		Tk = Tb
		
		if (algo =='default'):  
			#Method #1
			#US standard atmosphere 1976
			R = 8.31432; # N*m /(mol*K)
			G = 9.80665; #m/s^2
			Tb = 288; # K
			Lb = -0.0065; #K/m
			M = 0.0289644; # kg/mol 
			exp = G*M/R/Lb # exponent
			base = Tb / (Tb + (Lb * Elevation))
			return (1/(base ** exp)) # barometric factor using the US standard Atmosphere
#################################################################
		elif(algo == 'davis'):
			#http://www.softwx.com/weather/uwxutils.html
			#Method #2
			vpLapseRate = 0.00275
			hCorr = 0
			#converts elevation from meters to ft.
			elevation_ft = WeatherUtils.M2Ft(Elevation)
			exp2 = elevation_ft /(122.8943111 * (50 + 460 + (elevation_ft * vpLapseRate/2) + hCorr))
			return (10**exp2) # barometric factor calculated using the softwx method.
#################################################################
			#Method #3
		elif(algo == 'sandhurst'):
			Tk = 288
			exp3 = -(Elevation/Tk/29.263)
			return (1/ math.exp(exp3))
		else:
			return ('Algorithm not found')  
      
########### Conversion Equations ####################   
 
	#Farenheit to celsius
	def F2C(n):
		return ((n - 32) * 5)/9
	# Celsius to farenheit
	def C2F(n):  
		return ((n * 9)/5) + 32
	# Celsius to Kelvin
	def C2K(n):  
		return n + 273.15
	# Kelvin to Celsius
	def K2C(n): 
		return n - 273.15
	# Farenheit to Rankine
	def F2R(n):  
		return n + 459.67
	# Rankine to Farenheit
	def R2F(n): 
		return n - 459.67
	# inHg to hPa
	def In2HPa(n): 
		return n / 0.02953
	#hPa to inHg
	def HPa2In(n):  
		return n * 0.02953
	# Ft to meters
	def Ft2M(n):  
		return n * 0.3048
	# Meters to Ft
	def M2Ft(n):  
		return n / 0.3048
	# inches to mm
	def In2mm(n): 
		return n * 25.4
	# mm to inches
	def mm2In(n): 
		return n / 25.4
	#miles to km 
	def M2km(n): 
		return n * 1.609344
	#km to miles
	def km2M(n): 
		return n / 1.609344
	#knots to mph
	def Knt2Mph(n):
		return n * 1.15078
    
