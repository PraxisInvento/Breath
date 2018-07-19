##sudo apt-get install libgeos-dev
#sudo pip install pytz
#sudo pip install tzwhere
#sudo pip install pynmea2

import serial
import pynmea2
from datetime import datetime, timedelta, date, time
#import pytz
#from tzwhere import tzwhere


def parseGPS(stri):
    if stri.find('GGA') > 0:#'RMC' #'GGA'
		try:
		    msg = pynmea2.parse(stri)
		except pynmea2.nmea.ParseError as e:
		    print("pynmea>>", e)
		    return False	
		print("\n New data \n Timestamp:  %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" % (msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units))
		#Insert into db
		return True
		
            
serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)

while True:
    try:
        str = serialPort.readline()
        print(str)
    except serial.SerialException as e:
        #There is no new data from serial port
        print("SerialEXE:   ",e)
        serialPort.close()
	try:
	    serialPort.open()
	except IOError as e:
	    print("IO >>",e)
	#break
        #serialPort.open()
        
    except TypeError as e:
        #Disconnect of USB->UART occured
        serialPort.close()
        serialPort.open()
        print("Type=>> ",e)
        
    if parseGPS(str):
		break



##Note cron job is added
# run script every 5 minutes
#*/5 * * * *   myuser  python /path/to/script.py

# run script after system (re)boot
#@reboot       myuser  python /path/to/script.py
'''
		#### No need for changing to local time.... Let change in cloud..
		if(msg.lat != 75):# 75 is variable. store in db for future use.
			print("get lat and lon UTC only if it's coordinate change ")
		tz = tzwhere.tzwhere()
		timezone_str = tz.tzNameAt(float(msg.lat)/100,float(msg.lon)/100) 
		timezone = pytz.timezone(timezone_str)
		
		timenow = datetime.combine(date.today(),msg.timestamp) #+ timedelta(hours=5,minutes=30)
		timeoffset = timezone.utcoffset(timenow).total_seconds()
		
		##above will placed in if condition.
		
		gpslocaltime = timenow+  timedelta(seconds=timeoffset)
		print(" \n now time: %s " % gpslocaltime.strftime('%d-%m-%Y %H:%m'))
		'''
