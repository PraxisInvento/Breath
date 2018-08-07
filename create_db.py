#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('breath.db')
print "Opened database successfully";

conn.execute("DROP TABLE IF EXISTS model1")

conn.execute('''CREATE TABLE model1
         (ID INTEGER PRIMARY KEY   AUTOINCREMENT,
         UTCtime	    TEXT,
         Lat            TEXT,
         Lon            TEXT,
         Alt            TEXT,
         Temp           TEXT,
         Hum            TEXT,
         PM25           TEXT,
         PM10           TEXT,
         PT_ADC     	TEXT,
         NO2_we			TEXT,
         NO2_ae			TEXT,  
         O3_we			TEXT,
         O3_ae			TEXT,
         CO_we			TEXT,
         CO_ae			TEXT,
         SO2_we			TEXT,
         SO2_ae			TEXT,
         NO2_s          TEXT,
         NO2_a          TEXT,
         O3_s           TEXT,
         O3_a           TEXT,
         CO_s           TEXT,
         CO_a           TEXT,
         SO2_s          TEXT,
         SO2_a          TEXT);''')
print "Table created successfully";

conn.close()
