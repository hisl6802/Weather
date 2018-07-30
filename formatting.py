#!/usr/bin/python3
import configparser
	
def WU_urlform():
	'''This function sets up the appropriate Url to send a post request
	to Wunderground. The function will pull the default beginning of
	the Wunderground Url as well as the unique Personal Weather Station
	ID and password from the settings.ini file. '''
	
	#sets the CongfigParser class equal to settings 
	settings = configparser.ConfigParser()

	#reads in the ini file containing the defaults
	settings.read('/home/pi/weather/settings.ini')
	
	#specifies the weather underground url 
	WU_url = settings['Settings']['WU_url']
	
	#specifies the weather station Identification given by weather underground.
	WU_id = settings['Settings']['WU_id']

	#specifies the weather underground password.
	WU_pswd = settings['Settings']['WU_pswd']
	
	#specifies the type of update that should be performed to http.
	action_str = settings['Settings']['action_str']
	
	#specfies the time format that should be sent. 
	date_str = settings['Settings']['date_str']
	
	#adds the PWS ID and wunderground account Password to the http post request.
	WU_url += 'ID=' + WU_id + '&PASSWORD=' + WU_pswd + date_str
	
	return WU_url
			
def url_form(n):
	self = eval(n)
	
	#sets the CongfigParser class equal to settings 
	settings = configparser.ConfigParser()

	#reads in the ini file containing the defaults
	settings.read('your settings file')
	
	#specifies the weather underground url 
	url_dest = settings['Settings']['url_dest']
	
	#specifies the type of update that should be performed to http.
	action_str = settings['Settings']['action_str']
	
	#specfies the time format that should be sent. 
	date_str = settings['Settings']['date_str']
	
	#adds the data_str to the url_dest to tell Wunderground the data is for now.
	url_dest += date_str
	
	return url_dest
	
	  
	
	
