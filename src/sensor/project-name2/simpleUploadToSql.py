#!/usr/bin/python

import datetime
from subprocess import Popen,PIPE
import time, os, subprocess
import sqlite3
dbname='/var/www/windspeed.db'
sensor0 = 0
new_path = '/home/pi/python/plantProjectV2/data.txt'
nameOfFile = 'data.txt'
relay =15
#grovepi.pinMode(relay,"OUTPUT")


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



def log_temperature(temp):
    print ("saving to database")
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))
#    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (25,))

    # commit the changes
    conn.commit()

    conn.close()

#grovepi.analogWrite(relay,255)
relay1 = 14
#grovepi.pinMode(relay1,"INPUT")
sensor_value0 = 0
try:
    sensor_value0 = 4
    print(sensor_value0)
except IOError:
    print ("Error")
    sensor_value0 = 10
savefile(sensor_value0)
#dropbox_upload()
log_temperature(sensor_value0)



