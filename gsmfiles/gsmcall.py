import RPi.GPIO as GPIO
import serial
import time,sys

SERIAL_PORT = "/dev/ttyAMA0"
ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)

ser.write("ATD+918903457463;\r")
print("Dialling.....")
time.sleep(10)
ser.write("ATH\r")
print("Hangup ..")
