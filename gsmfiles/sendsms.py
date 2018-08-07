import RPi.GPIO as GPIO
import serial
import time

SERIAL_PORT = "/dev/ttyUSB0"  # Raspberry Pi 2

ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)
ser.write('AT+CUSD=1,"*123#"\r')
time.sleep(3)
reply = ser.read(ser.inWaiting())
print reply
ser.write('AT+CUSD=1,"1"\r')
time.sleep(3)
reply = ser.read(ser.inWaiting())
print reply

ser.write('AT+CMGS="+918903457463"\r')
time.sleep(3)
t,state= "1" ,"on" 
msg = "Sending status at " + t + ":--" + state
print "Sending SMS with status info:" + msg
ser.write(msg + chr(26))
time.sleep(3)
reply = ser.read(ser.inWaiting())
print reply
