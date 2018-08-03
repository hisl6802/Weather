#!/usr/bin/python3
import time
from weather_utils import WeatherUtils
import math
import configparser

class WeatherAve:

	def init():  
		'''This function initializes all of the values in the 
		engineering data units,allowing them to averaged over
		a specified period of time.'''
		
		init={}
		
		#sets the ConfigParser equal to config
		settings = configparser.ConfigParser()
		
		#reads in the ini file containing the defaults
		settings.read('/home/pi/weather/settings.ini')
		
		#specifies the Young's weather station output type.
		arg = settings['Settings']['Young_out']
		
		#specifies the time period over which measurements will be taken.
		ave_per = float(settings['Settings']['ave_period'])
		
		#pulls the dictionary of possible new eqns from the settings.ini file
		new_eqns = dict(settings['Equations'])
		
		if arg == 'ASCII':
			init['ave_period'] = ave_per * 2
			init['windspeedmph'] = 0
			init['winddir_sin'] = 0
			init['winddir_cos'] = 0
			init['windgustmph'] = 0
			init['tempf'] = 0
			init['baromin'] = 0
			init['humidity'] = 0
			init['solarradiation'] = 0
			init['dewptf'] = 0
			init['comp_dir'] = 0
			init['cnt'] = 0
			init['time_start'] = time.time()
			init['time_stop'] = time.time() + ave_per
			
			return init
		
		elif arg == 'ASCII_L':
			init['ave_period'] = ave_per * 2
			init['windspeedmph'] = 0
			init['winddir_sin'] = 0
			init['winddir_cos'] = 0
			init['windgustmph'] = 0
			init['tempf'] = 0
			init['baromin'] = 0
			init['humidity'] = 0
			init['solarradiation'] = 0
			init['dewptf'] = 0
			init['comp_dir'] = 0
			init['lake_temp'] = 0
			init['cnt'] = 0
			init['time_start'] = time.time()
			init['time_stop'] = time.time() + ave_per
			
					
			return init
		
		elif arg == 'NMEA':  
			init['ave_period'] = ave_per * 2
			init['windspeedmph'] = 0
			init['winddir_sin'] = 0
			init['winddir_cos'] = 0
			init['windgustmph'] = 0
			init['tempf'] = 0
			init['baromin'] = 0
			init['humidity'] = 0
			init['dewptf'] = 0
			init['cnt'] = 0
			init['time_start'] = time.time()
			init['time_stop'] = time.time() + ave_per
			
			
			return init
		
		elif arg == 'NMEA_L':  
			init['ave_period'] = ave_per * 2
			init['windspeedmph'] = 0
			init['winddir_sin'] = 0
			init['winddir_cos'] = 0
			init['windgustmph'] = 0
			init['tempf'] = 0
			init['baromin'] = 0
			init['humidity'] = 0
			init['dewptf'] = 0
			init['cnt'] = 0
			init['lake_temp'] = 0
			init['time_start'] = time.time()
			init['time_stop'] = time.time() + ave_per
			
					
			return init
		
		else:
			return ('Unable to Initialize variables')
		
		
			
		
	def ave(sum_m, inst):
		
		ave={}
		
		#sets the ConfigParser equal to settings
		settings = configparser.ConfigParser()
		
		#reads the in the ini file containing the default values
		settings.read('/home/pi/weather/settings.ini')
		
		#specifies the Young's weather station output type.
		arg = settings['Settings']['Young_out']
		
		#specifies the location of the weather station.
		loc = settings['Settings']['loc']
		
		#specifies the barometric factor equation to use.
		alg = settings['Settings']['alg']
		
		if arg == 'ASCII':
			
			#Wind speed summation 
			windspeedmph_new = inst['windspeedmph']
			sum_m['windspeedmph'] += windspeedmph_new
		
			#Wind direction sine summation. 
			winddir_sin_new = math.sin(math.radians(inst['winddir']))
			sum_m['winddir_sin'] += winddir_sin_new
		
			#Wind direction cosine summation.
			winddir_cos_new = math.cos(math.radians(inst['winddir']))
			sum_m['winddir_cos'] += winddir_cos_new
		
			#Wind gust caluclation.
			if inst['windspeedmph'] >= sum_m['windgustmph']:
				sum_m['windgustmph'] = inst['windspeedmph']
				
			#Temperature summation tool.
			tempf_new = inst['tempf']
			sum_m['tempf'] += tempf_new
		
			#Pressure summation tool.
			baromin_new = WeatherUtils.baro_st_to_sl(inst, alg)
			sum_m['baromin'] += baromin_new
		
			#Relative humidity summation tool. 
			humidity_new = inst['humidity']
			sum_m['humidity'] += humidity_new
		
			#Solar Radiation summation tool.
			solarradiation_new = inst['solarradiation']
			sum_m['solarradiation'] += solarradiation_new
		
			#Compass Direction summation tool.
			comp_dir_new = inst['comp_dir']
			sum_m['comp_dir'] += comp_dir_new
	
			#Dew Point summation tool.
			dewptf_new = inst['dewptf']
			sum_m['dewptf'] += dewptf_new
		
			#Time counter
			ave['time'] = time.time()
			ave['time'] = float(format(ave['time'], '.2f'))
			
			#Counter
			sum_m['cnt'] += 1
			
		
			if ave['time'] >= sum_m['time_stop']:
				
				#calculates the windspeed over the specified averaging period.
				ave['windspeedmph'] = sum_m['windspeedmph']/sum_m['cnt']
				ave['windspeedmph'] = float(format(ave['windspeedmph'], '.2f')) 
				
				winddir_sin_ave = sum_m['winddir_sin']/sum_m['cnt']
				winddir_cos_ave = sum_m['winddir_cos']/sum_m['cnt']
				
				#calculates the wind direction over the specified averaging period.
				ave['winddir'] = math.degrees(math.atan2(winddir_sin_ave, winddir_cos_ave))
				ave['winddir'] = float(format(ave['winddir'], '.2f'))  
				
				if ave['winddir'] < 0:
					#calculates the wind direction over the specified averaging period.
					ave['winddir'] = 360 + ave['winddir_ave']
					ave['winddir'] =float(format(ave['winddir'], '.2f')) 
				
				#calculates the temperature over the specified averaging period.
				ave['tempf'] = sum_m['tempf']/sum_m['cnt']
				ave['tempf'] = float(format(ave['tempf'], '.2f')) 
				
				#calculates the barometric pressure over the specified averaging period.
				ave['baromin'] = sum_m['baromin']/sum_m['cnt']
				ave['baromin'] = float(format(ave['baromin'], '.2f'))  
				
				#calculates the humidity over the specified averaging period.
				ave['humidity'] = sum_m['humidity']/sum_m['cnt']
				ave['humidity'] = float(format(ave['humidity'], '.2f'))  
				
				#calculates the compass direction over the specified averaging period. 
				ave['comp_dir'] = sum_m['comp_dir']/sum_m['cnt']
				ave['comp_dir'] = float(format(ave['comp_dir'], '.2f'))  
				
				#calculates the solar radiation over the specified averaging period.
				ave['solarradiation'] = sum_m['solarradiation']/sum_m['cnt']
				ave['solarradiation'] = float(format(ave['solarradiation'], '.2f')) 
				
				#calculates the dew point temperature over the specified averaging period.  
				ave['dewptf'] = sum_m['dewptf']/sum_m['cnt']
				ave['dewptf'] = float(format(ave['dewptf'], '.2f'))
				
				#adds the location of the weather station to the averaging dictionary.
				ave['location'] = loc
				
				#calculates and adds the largest wind gust that occured during the specified averaging period. 
				ave['windgustmph'] = sum_m['windgustmph']
				ave['windgustmph'] = float(format(ave['windgustmph'], '.2f'))
						
				#reset the summations of the weather values. 
				sum_m['windspeedmph'] = 0
				sum_m['winddir_sin'] = 0
				sum_m['winddir_cos'] = 0
				sum_m['windgustmph'] = 0
				sum_m['tempf'] = 0
				sum_m['baromin'] = 0
				sum_m['humidity'] = 0 
				sum_m['solarradiation'] = 0
				sum_m['dewptf'] = 0
				sum_m['comp_dir'] = 0
				sum_m['cnt'] = 0
				sum_m['time_start'] = time.time()
				sum_m['time_stop'] = time.time() + (sum_m['ave_period']/2)
				
						
				return ave
		
		elif arg == 'ASCII_L':
			
			#Wind speed summation 
			windspeedmph_new = inst['windspeedmph']
			sum_m['windspeedmph'] += windspeedmph_new
		
			#Wind direction sine summation. 
			winddir_sin_new = math.sin(math.radians(inst['winddir']))
			sum_m['winddir_sin'] += winddir_sin_new
		
			#Wind direction cosine summation.
			winddir_cos_new = math.cos(math.radians(inst['winddir']))
			sum_m['winddir_cos'] += winddir_cos_new
			
			#Wind gust caluclation.
			if inst['windspeedmph'] >= sum_m['windgustmph']:
				sum_m['windgustmph'] = inst['windspeedmph']
				
			#Temperature summation tool.
			tempf_new = inst['tempf']
			sum_m['tempf'] += tempf_new
		
			#Pressure summation tool.
			baromin_new = WeatherUtils.baro_st_to_sl(inst, alg)
			sum_m['baromin'] += baromin_new
		
			#Relative humidity summation tool. 
			humidity_new = inst['humidity']
			sum_m['humidity'] += humidity_new
		
			#Solar Radiation summation tool.
			solarradiation_new = inst['solarradiation']
			sum_m['solarradiation'] += solarradiation_new
		
			#Compass Direction summation tool.
			comp_dir_new = inst['comp_dir']
			sum_m['comp_dir'] += comp_dir_new
	
			#Dew Point summation tool.
			dewptf_new = inst['dewptf']
			sum_m['dewptf'] += dewptf_new
			
			#Lake Temperature summation tool.
			lake_temp_new = inst['lake_temp']
			sum_m['lake_temp'] += lake_temp_new
		
			#Time counter
			ave['time'] = time.time()
			ave['time'] = float(format(ave['time'], '.2f'))
			
			#Counter
			sum_m['cnt'] += 1
					
			if ave['time'] >= sum_m['time_stop']:
				#calculates the wind speed over the specified averaging period.
				ave['windspeedmph'] = sum_m['windspeedmph']/sum_m['cnt']	
				ave['windspeedmph'] = float(format(ave['windspeedmph'], '.2f'))
						
				winddir_sin_ave = sum_m['winddir_sin']/sum_m['cnt']
				winddir_cos_ave = sum_m['winddir_cos']/sum_m['cnt']
				#calculates the wind direction over the specified averaging period.
				ave['winddir'] = math.degrees(math.atan2(winddir_sin_ave, winddir_cos_ave))
				ave['winddir'] = float(format(ave['winddir'], '.2f'))
				
				if ave['winddir'] < 0:
					#calculates the wind direction over the specified averaging period.
					ave['winddir'] = 360 + ave['winddir']
					ave['winddir'] =float(format(ave['winddir'], '.2f'))
				
				#calculates the temperature over the specified averaging period.
				ave['tempf'] = sum_m['tempf']/sum_m['cnt']
				ave['tempf'] = float(format(ave['tempf'], '.2f'))
				
				#calculates the barometric pressure over the specified averaging period.
				ave['baromin'] = sum_m['baromin']/sum_m['cnt']
				ave['baromin'] = float(format(ave['baromin'], '.2f')) 
				
				#calculates the humidity over the specified averaging period.
				ave['humidity'] = sum_m['humidity']/sum_m['cnt']
				ave['humidity'] = float(format(ave['humidity'], '.2f'))
				
				#calculates the compass direction over the specified averaging period.
				ave['comp_dir'] = sum_m['comp_dir']/sum_m['cnt']
				ave['comp_dir'] = float(format(ave['comp_dir'], '.2f'))
				
				#calculates the solar radiation over the specified averaging period.
				ave['solarradiation'] = sum_m['solarradiation']/sum_m['cnt']
				ave['solarradiation'] = float(format(ave['solarradiation'], '.2f')) 
				
				#calculates the dew point temperature over the specified averaging period.
				ave['dewptf'] = sum_m['dewptf']/sum_m['cnt']
				ave['dewptf'] = float(format(ave['dewptf'], '.2f'))
				
				#calculates the lake temperature over the specified averaging period.
				ave['lake_temp'] = sum_m['lake_temp']/sum_m['cnt']
				ave['lake_temp'] = float(format(ave['lake_temp']))
				
				#adds the location of the weather station to the averaging dictionary.
				ave['location'] = loc
				
				#calculates the largest wind gust speed during the averaging period.
				ave['windgustmph'] = sum_m['windgustmph']
				ave['windgustmph'] = float(format(ave['windgustmph']))
				
				#reset the summations of the weather values. 
				sum_m['windspeedmph'] = 0
				sum_m['winddir_sin'] = 0
				sum_m['winddir_cos'] = 0
				sum_m['windgustmph'] = 0
				sum_m['tempf'] = 0
				sum_m['baromin'] = 0
				sum_m['humidity'] = 0 
				sum_m['solarradiation'] = 0
				sum_m['dewptf'] = 0
				sum_m['comp_dir'] = 0
				sum_m['lake_temp'] = 0
				sum_m['cnt'] = 0
				sum_m['time_start'] = time.time()
				sum_m['time_stop'] = time.time() + (sum_m['ave_period']/2)
				
				return ave
		
		elif arg == 'NMEA':
			
			#Wind speed summation 
			windspeedmph_new = inst['windspeedmph']
			sum_m['windspeedmph'] += windspeedmph_new
		
			#Wind direction sine summation. 
			winddir_sin_new = math.sin(math.radians(inst['winddir']))
			sum_m['winddir_sin'] += winddir_sin_new
		
			#Wind direction cosine summation.
			winddir_cos_new = math.cos(math.radians(inst['winddir']))
			sum_m['winddir_cos'] += winddir_cos_new
			
			#Wind gust caluclation.
			if inst['windspeedmph'] >= sum_m['windgustmph']:
				sum_m['windgustmph'] = inst['windspeedmph']
				
			#Temperature summation tool.
			tempf_new = inst['tempf']
			sum_m['tempf'] += tempf_new
		
			#Pressure summation tool.
			baromin_new = WeatherUtils.baro_st_to_sl(inst, alg)
			sum_m['baromin'] += baromin_new
		
			#Relative humidity summation tool. 
			humidity_new = inst['humidity']
			sum_m['humidity'] += humidity_new
			
			#Time counter
			ave['time'] = time.time()
			ave['time'] = float(format(ave['time'], '.2f'))
			
			#Counter
			sum_m['cnt'] += 1
					
			if ave['time'] >= sum_m['time_stop']:
				#calculates the wind speed over the specified averaging period.
				ave['windspeedmph'] = sum_m['windspeedmph']/sum_m['cnt']			
				ave['windspeedmph'] = float(format(ave['windspeedmph'],'.2f'))
				
				winddir_sin_ave = sum_m['winddir_sin']/sum_m['cnt']				
				winddir_cos_ave = sum_m['winddir_cos']/sum_m['cnt']				
				
				#calculates the wind direction over the specified averaging period.
				ave['winddir'] = math.degrees(math.atan2(winddir_sin_ave, winddir_cos_ave))
				ave['winddir'] = float(format(ave['winddir'],'.2f'))
				
				if ave['winddir'] < 0:	
					#calculates the wind direction over the specified averaging period.				
					ave['winddir'] = 360 + ave['winddir_ave']
					ave['winddir'] = float(format(ave['winddir'], '.2f'))
					
				#calculates the temperature over the specified averaging period.
				ave['tempf'] = sum_m['tempf']/sum_m['cnt']			
				ave['tempf'] = float(format(ave['tempf'], '.2f'))
				
				#calculates the barometric pressure over the specified averaging period.	
				ave['baromin'] = sum_m['baromin']/sum_m['cnt']				
				ave['baromin'] = float(format(ave['baromin'], '.2f'))
				
				#calculates the humdity over the specified averaging period.
				ave['humidity'] = sum_m['humidity']/sum_m['cnt']
				ave['humidity'] = float(format(ave['humidity'], '.2f'))
				
				#adds the location to the averaging dictionary
				ave['location'] = loc
				
				#calculates the largest wind gust during the specified averaging period.
				ave['windgustmph'] = sum_m['windgustmph']
						
				#resets the summations of the weather values.
				sum_m['windspeedmph'] = 0
				sum_m['winddir_sin'] = 0
				sum_m['w_dir_cos'] = 0
				sum_m['windgustmph'] = 0
				sum_m['tempf'] = 0
				sum_m['baromin'] = 0
				sum_m['humidity'] = 0 
				sum_m['cnt'] = 0
				sum_m['time_start'] = time.time()
				sum_m['time_stop'] = time.time() + (sum_m['ave_period']/2)
						
				return ave
		
		
		elif arg == 'NMEA_L':
			
			#Wind speed summation 
			windspeedmph_new = inst['windspeedmph']
			sum_m['windspeedmph'] += windspeedmph_new
		
			#Wind direction sine summation. 
			winddir_sin_new = math.sin(math.radians(inst['winddir']))
			sum_m['winddir_sin'] += winddir_sin_new
		
			#Wind direction cosine summation.
			winddir_cos_new = math.cos(math.radians(inst['winddir']))
			sum_m['winddir_cos'] += winddir_cos_new
			
			#Wind gust caluclation.
			if inst['windspeedmph'] >= sum_m['windgustmph']:
				sum_m['windgustmph'] = inst['windspeedmph']
				
			#Temperature summation tool.
			tempf_new = inst['tempf']
			sum_m['tempf'] += tempf_new
		
			#Pressure summation tool.
			baromin_new = WeatherUtils.baro_st_to_sl(inst, alg)
			sum_m['baromin'] += baromin_new
		
			#Relative humidity summation tool. 
			humidity_new = inst['humidity']
			sum_m['humidity'] += humidity_new
			
			#Time counter
			ave['time'] = time.time()
			ave['time'] = float(format(ave['time'], '.2f'))
			
			#Counter
			sum_m['cnt'] += 1
					
			if ave['time'] >= sum_m['time_stop']:
				#calculates the wind speed over the specified averaging period.
				ave['windspeedmph'] = sum_m['windspeedmph']/sum_m['cnt']
				ave['windspeedmph'] = float(format(ave['windspeedmph'], '.2f'))
				
				winddir_sin_ave = sum_m['winddir_sin']/sum_m['cnt']
				winddir_cos_ave = sum_m['winddir_cos']/sum_m['cnt']
				
				#calculates the wind direction over the specified averaging period
				ave['winddir'] = math.degrees(math.atan2(winddir_sin_ave, winddir_cos_ave))
				ave['winddir'] = float(format(ave['winddir'], '.2f'))
				
				if ave['winddir'] < 0:
					#calculates the wind direction over the specified averaging period.
					ave['winddir'] = 360 + ave['winddir']
					ave['winddir'] = float(format(ave['winddir'], '.2f'))
				
				#calculates the temperature over the specified averaging period.	
				ave['tempf'] = sum_m['tempf']/sum_m['cnt']
				ave['tempf'] = float(format(ave['tempf'], '.2f'))
				
				#calculates the barometric pressure over the specified averaging period. 
				ave['baromin'] = sum_m['baromin']/sum_m['cnt']				
				ave['baromin'] = float(format(ave['tempf'], '.2f'))
				
				#calculates the humdity over the specified averaging period.
				ave['humidity'] = sum_m['humidity']/sum_m['cnt']
				ave['humidity'] = float(format(ave['humidity'], '.2f'))
				
				#calculates the lake temperature over the specified averaging period. 
				ave['lake_temp'] = sum_m['lake_temp']/sum_m['cnt']
				ave['lake_temp'] = float(format(ave['lake_temp'], '.2f'))
				
				#adds the location to the averaging dictionary.
				ave['location'] = loc
				
				#calculates the largest wind gust during the specified averaging period.
				ave['windgustmph'] = sum_m['windgustmph']
				ave['windgustmph'] = float(format(ave['windgustmph'], '.2f'))
						
				#resets the summations of the weather values.
				sum_m['windspeedmph'] = 0
				sum_m['winddir_sin'] = 0
				sum_m['winddir_cos'] = 0
				sum_m['windgustmph'] = 0
				sum_m['tempf'] = 0
				sum_m['baromin'] = 0
				sum_m['humidity'] = 0 
				sum_m['lake_temp'] = 0
				sum_m['cnt'] = 0
				sum_m['time_start'] = time.time()
				sum_m['time_stop'] = time.time() + (sum_m['ave_period']/2)
						
				return ave
		else:
			
			return ('The input type is not supported by this class')
	
