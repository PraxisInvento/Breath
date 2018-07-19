import time
import serial
import pynmea2
import smbus
from datetime import datetime, timedelta, date

utctime=0
lat=0
lon=0
alt=0

def si7021():
	# Get I2C bus
	bus = smbus.SMBus(1)

	# SI7021 address, 0x40(64)
	#		0xF5(245)	Select Relative Humidity NO HOLD master mode
	bus.write_byte(0x40, 0xF5)

	time.sleep(0.3)

	# SI7021 address, 0x40(64)
	# Read data back, 2 bytes, Humidity MSB first
	data0 = bus.read_byte(0x40)
	data1 = bus.read_byte(0x40)

	# Convert the data
	humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6

	time.sleep(0.3)

	# SI7021 address, 0x40(64)
	#		0xF3(243)	Select temperature NO HOLD master mode
	bus.write_byte(0x40, 0xF3)

	time.sleep(0.3)

	# SI7021 address, 0x40(64)
	# Read data back, 2 bytes, Temperature MSB first
	data0 = bus.read_byte(0x40)
	data1 = bus.read_byte(0x40)

	# Convert the data
	cTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
	fTemp = cTemp * 1.8 + 32
	# Output data to screen
	#print "Relative Humidity is : %.2f %%" %humidity
	#print "Temperature in Celsius is : %.2f C" %cTemp
	#print "Temperature in Fahrenheit is : %.2f F" %fTemp
	
	return "%.2f"%humidity,'%.2f'%cTemp

def hpm():
	PM25=0
	PM10=0
	port = serial.Serial("/dev/ttyUSB1", baudrate=9600, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout=1.5)
	if port.isOpen():
		port.close()
	port.open()
	time.sleep(0.1)
	data = port.read(32);
	time.sleep(0.1)
	try:
		if ord(data[0]) == 66 and ord(data[1]) == 77:
			suma = 0
			for a in range(30):
				suma += ord(data[a])
			if suma == ord(data[30])*256+ord(data[31]):
				PM25 = int(ord(data[6])*256+ord(data[7]))
				PM10 = int((ord(data[8])*256+ord(data[9]))/0.75)
				#print 'PM2.5: %d ug/m3' % round(PM25)
				#print 'PM10: %d ug/m3' % round(PM10)
			else:
				print "no data"
		else:
			print "no data"
	except Exception as ex:
		print ex
	finally:
		port.close()
		return PM25,PM10

def gps():
	serialPort = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
	str=""
	while True:
		try:
			str = serialPort.readline()
			#print(str)
		except serial.SerialException as e:
			#There is no new data from serial port
			print("SerialEXE:   ",e)
			serialPort.close()
			try:
				if serialPort.isOpen():
					serialPort.close()
				serialPort.open()
			except IOError as e:
				print("IO >>",e)		
		except TypeError as e:
			#Disconnect of USB->UART occured
			serialPort.close()
			serialPort.open()
			print("Type=>> ",e)
			
		if parseGPS(str):
			return utctime,lat,lon,alt
			break
	
	
def parseGPS(stri):
	if stri.find('GGA') > 0:#'RMC' #'GGA'
		try:
			msg = pynmea2.parse(stri)
		except pynmea2.nmea.ParseError as e:
			print("pynmea>>", e)
			return False	
		#print("\n Timestamp:  %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" % (msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units))
		timenow = datetime.combine(date.today(),msg.timestamp) + timedelta(minutes=330) #msg.timestamp
		global utctime,lat,lon,alt
		utctime,lat,lon,alt= timenow.strftime('%d,%H:%M'),msg.lat,msg.lon,msg.altitude #timenow.strftime('%H:%m:%S')
		
		return True
		
            
