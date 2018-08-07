import os, time
import serial   
 
# Enable Serial Communication
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
 
# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key
while(1):
	port.write('AT'+'\r\n')
	try:
		dataIn = port.read(100)
	except serial.SerialException as e:
		#There is no new data from serial port
		print None
	except TypeError as e:
		#Disconnect of USB->UART occured
		port.close()
		print None
	else:
		#Some data was received
		print dataIn
		#break
