#!/usr/bin/env python

import sqlite3

import os
import time
import glob
import time
import grovepi
dbname='/var/www/templog.db'

#Sensor connected to A0,A1,A2 Port 
sensor0 = 0		 
sensor1 = 1		 
sensor2 = 2		 

def log_temperature(temp):
    print (temp)
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))
#    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (25,))
    
    # commit the changes
    conn.commit()

    conn.close()    


#while True:
try:
    sensor_value0 = grovepi.analogRead(sensor0)
    print ("%d" %(sensor_value0))
except IOError:
    print ("Error")

log_temperature(sensor_value0)
