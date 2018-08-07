# _*_ coding: utf-8 _*_
import serial
import time
import json

phone = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)

def sim800_responde(cmd,data=None,timeout=0):
	phone.write(cmd)
	time.sleep(2)
	if(data):
		phone.write(data+ chr(26))
	while True:
		response = phone.readline()    
		if not response:
			continue
		print  "* ",response
		if "DOWNLOAD" in response:
			return 1
		if "CLOSED" in response:
			return 1	
		if "OK" in response:
			print "sucess"
			return 1
		if "ERROR" in response:
			print "fail"
			time.sleep(3)
			return 0
		if timeout == 1:
			return 1
		elif timeout == 2:
			for i in range(30):
				response = phone.readline() 
				print i
				if not response:
					continue
				print i,"=>",response
			return 1

     

def webhttp(): 
	data = {"name":"sam","age":1452}
	sim800_responde('AT+SAPBR=3,1,"APN","airtelgprs.com"\r')
 	sim800_responde('AT+SAPBR=1,1\r')
	sim800_responde('AT+SAPBR=2,1\r')
	sim800_responde('AT+HTTPINIT\r')
	sim800_responde('AT+HTTPPARA="CID",1\r')
	sim800_responde('AT+HTTPPARA="URL"," ec2-52-66-151-17.ap-south-1.compute.amazonaws.com:192/index.php?name=sam&age=45"\r')#/dibrugarh/vote.php?camera=1&device_number=500&latitude=10&longitude=10&speed=1&altitude=100"\r')
	#sim800_responde('AT+HTTPPARA="URL"," http://ec2-52-66-151-17.ap-south-1.compute.amazonaws.com:192/index.php"\r')#/dibrugarh/vote.php?camera=1&device_number=500&latitude=10&longitude=10&speed=1&altitude=100"\r')
	#sim800_responde('AT+HTTPPARA="CONTENT","application/json"\r')
	#sim800_responde('AT+HTTPDATA=100,10000 \r')
	#sim800_responde(json.dumps(data))
	#time.sleep(10)
	sim800_responde('AT+HTTPACTION=0\r')
	#sim800_responde('AT+HTTPACTION=1\r')
	time.sleep(3)
	sim800_responde('AT+HTTPREAD\r')
	sim800_responde('AT+HTTPTERM\r')
	sim800_responde('AT+SAPBR=0,1\r')   
	
def webtcp():
	#sim800_responde("AT+CGATT?\r")
	#sim800_responde("AT+CGATT=1\r")
	sim800_responde("AT+CSTT='airtelgprs.com'\r")
	sim800_responde("AT+CSTT?\r")
	#sim800_responde("AT+CREG?\r")
	sim800_responde("AT+CIICR\r")
	time.sleep(3)
	sim800_responde("AT+CIPSTATUS\r")
	sim800_responde("AT+CIFSR\r",timeout=True)
	sim800_responde("AT+CDNSORIP=1\r")
	sim800_responde("AT+CIPSPRT=1\r")
	sim800_responde("AT+CIPHEAD=1\r")
	sim800_responde('AT+CIPSTART="TCP","ec2-52-66-151-17.ap-south-1.compute.amazonaws.com","192"\r')
	time.sleep(5)
	#sim800_responde('AT+CIPSEND\r\n',data='GET /index.php?name=nobody&age=98 HTTP/1.1\r\nHOST: ec2-52-66-151-17.ap-south-1.compute.amazonaws.com\r\nConnection: close\r\n\r\n',timeout=2)
	#time.sleep(10)
	sim800_responde('AT+CIPSEND\r\n',data='POST /index.php HTTP/1.1\r\nHOST: ec2-52-66-151-17.ap-south-1.compute.amazonaws.com\r\nConnection: keep-alive\r\nContent-Type: text/plain\r\nContent-Length: 100\r\nname=papa&age=43\r\n\r\n',timeout=2)
	#
	sim800_responde('AT+CIPCLOSE=1\r')#=4 try it

	sim800_responde('AT+CIPSHUT\r')
	
#webhttp()
webtcp()
