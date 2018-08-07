import os.path
import time
from sensor import si7021,hpm,gps
from gas import gases
import sqlite3
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "breath.db")
#print("db: ",db_path)
conn = sqlite3.connect(db_path)
print("\nOpened db")

if __name__=="__main__":
	UTCtime,Latitude,Longitude,Altitude=gps()
	Humidity,Temperature = si7021() #check output is present or not
	avgPM25 = 0
	avgPM10 = 0
	sample=2
	for a in range(sample):#10
		PM25,PM10 = hpm()
		avgPM25 += PM25
		avgPM10 += PM10
	avgPM25 /= sample
	avgPM10 /= sample
	CO="0"
	NO2="0"
	SO2="0"
	O3="0"
	
	PT_ADC,NO2_we,NO2_ae,O3_we,O3_ae,CO_we,CO_ae,SO2_we,So2_ae,NO2_s,NO2_a,O3_s,O3_a,CO_s,CO_a,SO2_s,SO2_a = gases()
	
	print("%s\nGPSTime= %s Loc= %s N, %s E Alt= %s, Temp = %s*c, Hum= %s%%, PM2.5= %s ug/m3, PM10 = %s ug/m3 "%(datetime.datetime.now(),UTCtime,Latitude,Longitude,Altitude,Temperature,Humidity,avgPM25,avgPM10))
	
	
	conn.execute("INSERT INTO model1 (UTCtime, Lat, Lon, Alt, Temp, Hum, PM25, PM10, PT_ADC,NO2_we,NO2_ae,O3_we,O3_ae,CO_we,CO_ae,SO2_we,So2_ae, NO2_s, NO2_a, O3_s, O3_a, CO_s, CO_a, SO2_s,SO2_a) \
      VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (str(UTCtime),str(Latitude),str(Longitude),str(Altitude),str(Temperature),str(Humidity),str(avgPM25),str(avgPM10),str(PT_ADC),str(NO2_we),str(NO2_ae),str(O3_we),str(O3_ae),str(CO_we),str(CO_ae),str(SO2_we),str(So2_ae),str(NO2_s),str(NO2_a),str(O3_s),str(O3_a),str(CO_s),str(CO_a),str(SO2_s),str(SO2_a)))

	conn.commit()
