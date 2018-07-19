import smbus
import time
import Adafruit_ADS1x15

no2 = {'we_e':279,'we_o':-7 ,'we_t':272,'ae_e':294,'ae_o':-2,'ae_t':292,'sen':0.308,\
'nt':[0.8, 0.8, 1.0, 1.2, 1.6, 1.8, 1.9, 2.5, 3.6]}
o3  = {'we_e':393,'we_o':-11,'we_t':382,'ae_e':392,'ae_o':-3,'ae_t':389,'sen':0.335,\
'nt':[1.0, 1.2, 1.2, 1.6, 1.7, 2.0, 2.1, 3.4, 4.6],\
'kt1':[0.1, 0.1, 0.2, 0.3, 0.7, 1.0, 1.7, 3.0, 4.0]}
co  = {'we_e':297,'we_o':-7 ,'we_t':290,'ae_e':288,'ae_o':-4,'ae_t':284,'sen':0.262,\
'nt':[1.0, 1.0, 1.0, 1.0, -0.2, -0.9, -1.5, -1.5, -1.5]}
so2 = {'we_e':293,'we_o':+21,'we_t':314,'ae_e':284,'ae_o':-4,'ae_t':280,'sen':0.350,\
'nt':[1.3, 1.3, 1.3, 1.2, 0.9, 0.4, 0.4, 0.4, 0.4],\
'kt2':[0, 0, 0, 0, 0, 0, 5, 25, 45]}

address = 0x04 # Arduino slave address for pt temp
bus = smbus.SMBus(1)

adc1 = Adafruit_ADS1x15.ADS1115(0x48)
adc2 = Adafruit_ADS1x15.ADS1115(0x49)

GAIN = 2/3
ADC_V = 0.1875


def pt_temp():
	try:
		bus.write_byte(address,1)
	except Exception as ex:
		print ex
		return 0,0
	time.sleep(1)
	try:
		volt_pt = float(bus.read_word_data(address,1))*(1.15/1024)
	except Exception as ex:
		print ex
		volt_pt=0
	Temp_pt = 28 + ((volt_pt - 0.348 ) / 0.001)#28,330
	#Ref mv at known temp 28*c #0.341 in arduino at5v 0.309 in arduino with raspi due to 3.3v
	#on 3.3v pro mini output at 347 @28*c, with ttl to usb 368 @28*c
	return volt_pt,Temp_pt
	
def ppb(we,ae,we_t,ae_t,sen,nt):
	print "nt: ",nt
	#WEc = WEu - nt * AEu
	#WEu = WE - WEt
	#AEu = AE - AEt
	we_u = we - float(we_t)
	ae_u = ae - float(ae_t)
	we_c = we_u - nt * ae_u
	ppb =  we_c/ float(sen)
	return ppb
	
while True:
	no2_we = float(adc1.read_adc(0, gain=GAIN) *ADC_V)
	no2_ae = float(adc1.read_adc(1, gain=GAIN) *ADC_V)
      
	o3_we = float(adc1.read_adc(2, gain=GAIN) *ADC_V)
	o3_ae = float(adc1.read_adc(3, gain=GAIN) *ADC_V)
        
	co_we = float(adc2.read_adc(0, gain=GAIN) *ADC_V)
	co_ae = float(adc2.read_adc(1, gain=GAIN) *ADC_V)
        
	so2_we = float(adc2.read_adc(2, gain=GAIN) *ADC_V)
	so2_ae = float(adc2.read_adc(3, gain=GAIN) *ADC_V)
        
	volt_pt,Temp_pt = pt_temp()
	time.sleep(1)
	print(" volt_pt: %1.2f mV Temp_pt: %1.2f C"% (volt_pt*1000,Temp_pt))
		
	if -30 >= Temp_pt < -20 :
		index = 0 #0
	elif -20 >= Temp_pt < -10 :
		index = 1 #1
	elif -10 >= Temp_pt < 0 :
		index = 2 #2
	elif 0 >= Temp_pt < 10 :
		index = 5 #3
	elif 10 >= Temp_pt < 20 :
		index = 5 #4
	elif 20 >= Temp_pt < 30 :
		index = 5 #5
	elif 30 >= Temp_pt < 40 :
		index = 5 #6
	elif 40 >= Temp_pt < 50 :
		index = 7 #7
	elif Temp_pt >= 50 :
		index = 8 #8
	else:
		index = 5 #9
	print " index : ",index

	no2_ppb = ( (no2_we - no2['we_t']) - no2['nt'][index] * (no2_ae - no2['ae_t']) ) / no2['sen']
	o3_ppb  = ( (o3_we  - o3['we_t'] ) - o3['nt'][index]  * (o3_ae  - o3['ae_t'] ) ) / o3['sen']
	co_ppb  = ( (co_we  - co['we_t'] ) - co['nt'][index]  * (co_ae  - co['ae_t'] ) ) / co['sen']
	so2_ppb = ( (so2_we - so2['we_t']) - so2['nt'][index] * (so2_ae - so2['ae_t']) ) / so2['sen']

	print('no2_we= %i mV no2_ae= %i mV NO2= %1.2f ppb'%(no2_we,no2_ae,no2_ppb))
	print('o3_we=  %i mV o3_ae=  %i mV O3=  %1.2f ppb'%(o3_we,o3_ae,o3_ppb))
	print('co_we=  %i mV co_ae=  %i mV CO=  %1.2f ppb'%(co_we,co_ae,co_ppb))
	print('so2_we= %i mV so2_ae= %i mV SO2= %1.2f ppb'%(so2_we,so2_ae,so2_ppb))
