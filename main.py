import os
import glob
import time
import requests

 
#SETUP
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c
    
#dummy temperature printing	
#while True:
#      print(read_temp())	
#      time.sleep(1)

#test measurements     
humidity = 55.998
ambient_temp = 23.456
pressure = 1067.890
ground_temp = 16.345
wind_speed = 5.6129
wind_gust = 12.9030
wind_average = 180
rainfall = 1.270      

# create a string to hold the first part of the URL for uploading
WUurl = "https://weatherstation.wunderground.com/weatherstation\
/updateweatherstation.php?"

WU_station_id = "IBRATISL609" #PWS ID
WU_station_pwd = "3sec7ubq" #Password
WUcreds = "ID=" + WU_station_id + "&PASSWORD="+ WU_station_pwd
date_str = "&dateutc=now"
action_str = "&action=updateraw"

#send the data to Weather Underground
while True:   
    #get and round the temperature
    temp = read_temp()
    ambient_temp = "{0:.2f}".format(temp)

    #build http request
    r= requests.get(
            WUurl +
            WUcreds +
            date_str +
            "&tempf=" + ambient_temp +
            action_str)
    
    #check
    print(f"received {str(r.status_code)} {str(r.text)}")
    
    #send next weather update in 300s
    sleep(300)
