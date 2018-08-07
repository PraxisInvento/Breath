import smbus
import time
import Adafruit_ADS1x15

no2 = {'we_e':279,'we_o':-7 ,'we_t':272,'ae_e':294,'ae_o':-2,'ae_t':292,'sen':0.308,\
'nt':[0.8, 0.8, 1.0, 1.2, 1.6, 1.8, 1.9, 2.5, 3.6],\
'kt1':[0.2, 0.2, 0.2, 0.2, 0.7, 1.0, 1.3, 2.1, 3.5],\
'kt2':[-4, -4, -4, -4, -2, 0, 10, 35, 132]}
o3  = {'we_e':393,'we_o':-11,'we_t':382,'ae_e':392,'ae_o':-3,'ae_t':389,'sen':0.335,\
'nt':[1.0, 1.2, 1.2, 1.6, 1.7, 2.0, 2.1, 3.4, 4.6],\
'kt1':[0.1, 0.1, 0.2, 0.3, 0.7, 1.0, 1.7, 3.0, 4.0],\
'kt2':[-5, -5, -4, -3, 0.5, 0, 9, 42, 134]}
co  = {'we_e':297,'we_o':-7 ,'we_t':290,'ae_e':288,'ae_o':-4,'ae_t':284,'sen':0.262,\
'nt':[1.0, 1.0, 1.0, 1.0, -0.2, -0.9, -1.5, -1.5, -1.5],\
'kt1':[1.9, 2.9, 2.7, 3.9, 2.1, 1.0, -0.6, -0.3, -0.5],\
'kt2':[13, 12, 16, 11, 4, 0, -15, -18, -36]}
so2 = {'we_e':293,'we_o':+21,'we_t':314,'ae_e':284,'ae_o':-4,'ae_t':280,'sen':0.350,\
'nt':[1.3, 1.3, 1.3, 1.2, 0.9, 0.4, 0.4, 0.4, 0.4],\
'kt1':[1.5, 1.5, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0, 1.0],\
'kt2':[0, 0, 0, 0, 0, 0, 5, 25, 45]}

algo = {'suggest':{'no2':1, 'o3':3, 'co':1,'so2':4},\
 'alternative':{'no2':3, 'o3':1, 'co':4,'so2':1}}

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
	Adc = 0
	try:
		Adc = bus.read_word_data(address,1)	
	except Exception as ex:
		print ex
		Adc = 0
	#ref voltage : 2048 so,1bit=1mv
	volt_pt = float(Adc)/1000.0#*(3.3/1023)#1.15 or 3.3
	Temp_pt = 28 + ((volt_pt - 0.095 ) / 0.001)#28,330
	#Ref mv at known temp 28*c #0.341 in arduino at5v 0.309 in arduino with raspi due to 3.3v
	#on 3.3v pro mini output at 347 @28*c, with ttl to usb 368 @28*c
	return Adc,volt_pt,Temp_pt
	
#WEu = WE - WEe  
#AEu = AE - AEe
def ppb_algo1(we,ae,we_e,ae_e,nt,sen):
	print "nt: " ,nt
	#WEc = WEu - nt * AEu  
	we_u = we - float(we_e)
	ae_u = ae - float(ae_e)
	we_c = we_u - (nt * ae_u)
	ppb =  we_c/ float(sen)
	return ppb

def ppb_algo3(we,ae,we_e,ae_e,we_o,ae_o,kt1,sen):
	print "kt1: ",kt1
	we_u = we - float(we_e)
	ae_u = ae - float(ae_e)
	we_c = we_u - (we_o - ae_o) - kt1 * ae_u
	ppb =  we_c/ float(sen)
	return ppb
	
def ppb_algo4(we,we_e,we_o,kt2,sen): 
	print "kt2: " ,kt2
	we_u = we - float(we_e)
	#ae_u = ae - float(ae_e)
	we_c = we_u - we_o - kt2
	ppb =  we_c/ float(sen)
	return ppb
	
def gases():
	no2_we = float(adc1.read_adc(0, gain=GAIN) *ADC_V)
	no2_ae = float(adc1.read_adc(1, gain=GAIN) *ADC_V)
      
	o3_we = float(adc1.read_adc(2, gain=GAIN) *ADC_V)
	o3_ae = float(adc1.read_adc(3, gain=GAIN) *ADC_V)
        
	co_we = float(adc2.read_adc(0, gain=GAIN) *ADC_V)
	co_ae = float(adc2.read_adc(1, gain=GAIN) *ADC_V)
        
	so2_we = float(adc2.read_adc(2, gain=GAIN) *ADC_V)
	so2_ae = float(adc2.read_adc(3, gain=GAIN) *ADC_V)
	
	Adc,volt_pt,Temp_pt=0,0,0
	Adc,volt_pt,Temp_pt = pt_temp()
	time.sleep(1)
	print('\nADC: %i volt_pt: %1.2f mV Temp_pt: %1.2f C'% (Adc,volt_pt*1000,Temp_pt))
	
	Temp_pt = int(Temp_pt)
	if Temp_pt in xrange(-30,-20) :
		index = 0 #0
	elif Temp_pt in xrange(-20,-10) :
		index = 1 #1
	elif Temp_pt in xrange(-10,0) :
		index = 2 #2
	elif Temp_pt in xrange(0,10) :
		index = 3 #3
	elif Temp_pt in xrange(10,20) :
		index = 4 #4
	elif Temp_pt in xrange(20,30):
		index = 5 #5
	elif Temp_pt in xrange(30,40):
		index = 6 #6
	elif Temp_pt in xrange(40,50):
		index = 7 #7
	elif Temp_pt in xrange(50,100) :
		index = 8 #8
	else:
		index = 5 #9
	'''	
	if -30.0 <= Temp_pt > -20.0 :
		index = 0 #0
	elif -20.0 <= Temp_pt > -10.0 :
		index = 1 #1
	elif -10.0 <= Temp_pt > -1.0 :
		index = 2 #2
	elif 0.0 >= Temp_pt < 10.0 :
		index = 3 #3
	elif 10.0 >= Temp_pt < 20.0 :
		index = 4 #4
	elif 20.0 >= Temp_pt < 30.0 :
		index = 5 #5
	elif 30.0 >= Temp_pt < 40.0 :
		index = 6 #6
	elif 40.0 >= Temp_pt < 50.0 :
		index = 7 #7
	elif Temp_pt >= 50.0 :
		index = 8 #8
	else:
		index = 5 #9
	'''	

	##index = 5 # no temp compensation is done in program need lot study before
	print " index : ",index
	
	no2_ppb1 = ppb_algo1( no2_we, no2_ae, no2['we_e'], no2['ae_e'], no2['nt'][index], no2['sen'] )
	no2_ppb3 = ppb_algo3( no2_we, no2_ae, no2['we_e'], no2['ae_e'], no2['we_o'], no2['ae_o'], no2['kt1'][index], no2['sen'] )

	o3_ppb3  = ppb_algo3( o3_we, o3_ae, o3['we_e'], o3['ae_e'], o3['we_o'], o3['ae_o'], o3['kt1'][index], o3['sen'] )
	o3_ppb1  = ppb_algo1( o3_we, o3_ae, o3['we_e'], o3['ae_e'], o3['nt'][index], o3['sen'] )
		
	co_ppb1  = ppb_algo1( co_we, co_ae, co['we_e'], co['ae_e'], co['nt'][index], co['sen'] )
	co_ppb4  = ppb_algo4( co_we, co['we_e'], co['we_o'], co['kt2'][index], co['sen'] )
	
	so2_ppb4 = ppb_algo4( so2_we, so2['we_e'], so2['we_o'], so2['kt2'][index], so2['sen'] )
	so2_ppb1 = ppb_algo1( so2_we, so2_ae, so2['we_e'], so2['ae_e'], so2['nt'][index], so2['sen'] )
	
	print('no2_we= %i no2_ae= %i N1= %1.1f N3= %1.1f'%(no2_we,no2_ae,no2_ppb1,no2_ppb3))
	print('o3_we=  %i o3_ae=  %i O3= %1.1f O1= %1.1f'%(o3_we, o3_ae, o3_ppb3, o3_ppb1 ))
	print('co_we=  %i co_ae=  %i C1= %1.1f C4= %1.1f'%(co_we, co_ae, co_ppb1, co_ppb4 ))
	print('so2_we= %i so2_ae= %i S4= %1.1f S1= %1.1f'%(so2_we,so2_ae,so2_ppb4,so2_ppb1))
	
	'''
	no2_ppb1 = ppb_algo1( no2_we, no2_ae, no2['we_e'], no2['ae_e'], no2['nt'][index], no2['sen'] )
	o3_ppb1  = ppb_algo1( o3_we, o3_ae, o3['we_e'], o3['ae_e'], o3['nt'][index], o3['sen'] )
	co_ppb1  = ppb_algo1( co_we, co_ae, co['we_e'], co['ae_e'], co['nt'][index], co['sen'] )
	so2_ppb1 = ppb_algo1( so2_we, so2_ae, so2['we_e'], so2['ae_e'], so2['nt'][index], so2['sen'] )
	
	no2_ppb3 = ppb_algo3( no2_we, no2_ae, no2['we_e'], no2['ae_e'], no2['we_o'], no2['ae_o'], no2['kt1'][index], no2['sen'] )
	o3_ppb3  = ppb_algo3( o3_we, o3_ae, o3['we_e'], o3['ae_e'], o3['we_o'], o3['ae_o'], o3['kt1'][index], o3['sen'] )
	co_ppb3  = ppb_algo3( co_we, co_ae, co['we_e'], co['ae_e'], co['we_o'], co['ae_o'], co['kt1'][index], co['sen'] )
	so2_ppb3 = ppb_algo3( so2_we, so2_ae, so2['we_e'], so2['ae_e'], so2['we_o'], so2['ae_o'], so2['kt1'][index], so2['sen'] )
	
	no2_ppb4 = ppb_algo4( no2_we, no2['we_e'], no2['we_o'], no2['kt2'][index], no2['sen'] )
	o3_ppb4  = ppb_algo4( o3_we, o3['we_e'], o3['we_o'], o3['kt2'][index], o3['sen'] )
	co_ppb4  = ppb_algo4( co_we, co['we_e'], co['we_o'], co['kt2'][index], co['sen'] )
	so2_ppb4 = ppb_algo4( so2_we, so2['we_e'], so2['we_o'], so2['kt2'][index], so2['sen'] )
	
	print('no2_we= %i no2_ae= %i N1= %1.1f N3= %1.1f N4= %1.1f'%(no2_we,no2_ae,no2_ppb1,no2_ppb3,no2_ppb4))
	print('o3_we=  %i o3_ae=  %i O1= %1.1f O3= %1.1f O4= %1.1f'%(o3_we,o3_ae,o3_ppb1,o3_ppb3,o3_ppb4))
	print('co_we=  %i co_ae=  %i C1= %1.1f C3= %1.1f C4= %1.1f'%(co_we,co_ae,co_ppb1,co_ppb3,co_ppb4))
	print('so2_we= %i so2_ae= %i S1= %1.1f S3= %1.1f S4= %1.1f'%(so2_we,so2_ae,so2_ppb1,so2_ppb3,so2_ppb4))
	'''
	
	data = time.asctime( time.localtime(time.time()) )+\
	'\nADC: %i volt_pt: %1.2f mV Temp_pt: %1.2f C'% (Adc,volt_pt*1000,Temp_pt)+\
	'\nno2_we= %i no2_ae= %i N1= %1.1f N3= %1.1f'%(no2_we,no2_ae,no2_ppb1,no2_ppb3)+\
	'\no3_we=  %i o3_ae=  %i O3= %1.1f O1= %1.1f'%(o3_we, o3_ae, o3_ppb3, o3_ppb1 )+\
	'\nco_we=  %i co_ae=  %i C1= %1.1f C4= %1.1f'%(co_we, co_ae, co_ppb1, co_ppb4 )+\
	'\nso2_we= %i so2_ae= %i S4= %1.1f S1= %1.1f'%(so2_we,so2_ae,so2_ppb4,so2_ppb1)+\
	'\n ***************************************** \n' 
	#print data
	f = open('gasreading.txt', 'a')
	f.write(data)
	f.close()
	return int(Adc),int(no2_we),int(no2_ae),int(o3_we),int(o3_ae),\
	int(co_we),int(co_ae),int(so2_we),int(so2_we),\
	int(no2_ppb1),int(no2_ppb3),int(o3_ppb3),int(o3_ppb1),\
	int(co_ppb1),int(co_ppb4),int(so2_ppb4),int(so2_ppb1)
	
'''	
while True:
	print "i am true"
	NO2,O3,CO,SO2 = gases()
'''
'''
	#print no2_ppb
	no2_ppb = ( (no2_we - no2['we_e']) - no2['nt'][index] * (no2_ae - no2['ae_e']) ) / no2['sen']
	o3_ppb  = ( (o3_we  - o3['we_e'] ) - o3['nt'][index]  * (o3_ae  - o3['ae_e'] ) ) / o3['sen']
	co_ppb  = ( (co_we  - co['we_e'] ) - co['nt'][index]  * (co_ae  - co['ae_e'] ) ) / co['sen']
	so2_ppb = ( (so2_we - so2['we_e']) - so2['nt'][index] * (so2_ae - so2['ae_e']) ) / so2['sen']
'''
