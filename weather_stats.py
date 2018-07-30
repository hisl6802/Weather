#!/usr/bin/python3 -u

#Weather Station:
from decoder import decode
from weather_utils import WeatherUtils
from formatting import WU_urlform, url_form
from averaging import WeatherAve
import glob, os, requests, sys, time, json

import solo
solo.chk_and_stopall(__file__)

#initializes the measurements for averaging
x = WeatherAve.init()

while True:

    #reads and decodes serial output
    read_serial_output = decode()

    #Puts data into engineering units
    eng_data = WeatherUtils.engr(read_serial_output)

    #averages the weather stats over a given time.
    averaged_data = WeatherAve.ave(x, eng_data)
    if averaged_data is not None:

        #creates a string containing time since epoch.
        time_str = str(int(time.time()))
        
        #formats a string into another string.
        time_file_name = ('/home/pi/weather/results/{}.txt'.format(time_str))

        #serializes a dictionary allowing for the dictionary to be saved to a file.
        serialize_output = json.dumps(averaged_data)

        #creates a file and opens for writing.
        with open(time_file_name, 'x') as write:
                write.write(serialize_output)
                write.close()

        #checks the given path for files ending in .txt
        chk_buffer = glob.glob("/home/pi/weather/results/*.txt")
        #creates a list of the files
        chk_buffer = list(chk_buffer)
        #sorts the list in chronological order from oldest to most recent.
        chk_buffer.sort()

        for files in chk_buffer:

            with open(files, 'r') as open_file:
                read_weather_file = open_file.read()
                open_file.close()
            #takes the serialized dictionary from the file and puts it...
            #it into a dictionary.    
            deserialize_file = json.loads(read_weather_file)
            
            #creates the necessary Url to send to Wunderground.
            WU_url = WU_urlform()
             
            #tries to post the dictionary from the file to the Wunderground
            #website. 
            try:
                wunderground = requests.post(WU_url, deserialize_file)
            finally:
                #This will print the returned status code to the pi terminal.
                #With this here the status of the Wunderground upload can be checked.
                print(wunderground.status_code)
                
            if wunderground.status_code == 200:
                #if the data sucessfully uploaded then remove the file from the results folder.
                os.remove(files)
