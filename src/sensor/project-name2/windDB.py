#!/usr/bin/python

import analogRead
import datetime
from subprocess import Popen,PIPE
import time, os, subprocess
import sqlite3
import combine
dbwind='/var/www/windspeed.db'
dbdirection='/var/www/direction.db'
sensor0 = 0
new_path = '/home/pi/python/plantProjectV2/data.txt'
nameOfFile = 'data.txt'
relay =15



def dropbox_upload():
	is_valid=0

	nameOfFile = 'data.txt'
	fullDirectory = '/home/pi/python/plantProjectV2/' + nameOfFile
	command = '/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload ' + fullDirectory + ' /Apps/PythonUploader/'
	os.system(command)
	is_valid = 1
	command = ''
	print('EXITING UPLOAD')
	os.system(command)

def savefile(sensor):
    file = open(new_path,'a')
    today = str(datetime.datetime.now().strftime("%y%m%d:%H:%M:%S"))+','+str(sensor)+'\n'
    file.write(today)
#    dropbox_upload()



def log_temperature(temp,db):
    print ("saving to database")
    conn=sqlite3.connect(db)
    curs=conn.cursor()
    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))
#    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (25,))

    # commit the changes
    conn.commit()

    conn.close()


relay1 = 14

sensor_value0 = 0

while True:
    try:
        aR =  analogRead.analogRead()
        wind = analogRead.measure(aR)
        sensor_value0 = wind
        print("windSpeed:" + str(sensor_value0))
    except IOError:
        print ("Error")
        sensor_value0 = 10
    savefile(sensor_value0)
    log_temperature(sensor_value0,dbwind)
    windDir = combine.getWindDirection()
    print("windDir: "+str(windDir))
    log_temperature(windDir,dbdirection)
    time.sleep(1)
dropbox_upload()
#print(combine.getWindDirection())



