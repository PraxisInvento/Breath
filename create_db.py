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
         CO             TEXT,
         NO2            TEXT,
         SO2            TEXT,
         O3             TEXT);''')
print "Table created successfully";

conn.close()
