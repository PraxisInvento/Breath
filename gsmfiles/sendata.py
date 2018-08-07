import serial
import time, sys
from SIM800Modem import *
import RPi.GPIO as GPIO
#create config file for apn host port and last successful send time
APN = "airtelgprs.com"
HOST = "cleancitiesfoundation.com"
PORT = 80

req = "/dibrugarh/vote.php?camera=1&device_number=500&latitude=10&longitude=10&speed=10&altitude=10"

SERIAL_PORT = "/dev/ttyAMA0"  

ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)

print "Connecting to GSM net..."
connectGSM(ser, APN)

print "Connecting to TCP server..."
reply = connectTCP(ser, HOST, PORT)
if "CONNECT OK" not in reply:
    print "Connection failed"
    #sys.exit(0)

print "Connection established. Sending data..."
while True:
	#msg = "Breath is Out"
	#k = len(msg) # do not exceed value returned by AT+CIPSEND? (max 1460)
	#ser.write("AT+CIPSEND=" + str(k) +"\r") # fixed length sending
	time.sleep(1) # wait for prompt
	#ser.write(msg)
	sendHTTPRequest(ser, HOST, req)
	time.sleep(4)
	closeTCP(ser)
	time.sleep(10)


