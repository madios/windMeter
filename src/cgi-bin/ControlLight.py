#!/usr/bin/env python
#from Tkinter import *
from phue import Bridge
import sqlite3
import sys
import cgi
import cgitb
import sqlite3
import datetime
from subprocess import Popen,PIPE
import time, os, subprocess
dbname_debug='/var/www/templog_debug.db'
dbname='/var/www/temlog.db'
b = Bridge('192.168.0.100') # Enter bridge IP here.
b.get_light
#b.set_light([1,2,3], 'on', True)
lights = b.get_light_objects()
new_path = '/home/pi/python/plantProjectV2/data_debug.txt'
dbname='/var/www/templog.db'
#dbname='/home/pi/python/plantProjectV2/templog.db'
def dropbox_upload():
	is_valid=0

	nameOfFile = 'data_debug.txt'
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
    dropbox_upload()

def log_temperature(temp):
    print (temp)
    conn=sqlite3.connect(dbname_debug)
    curs=conn.cursor()
    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (temp,))
#    curs.execute("INSERT INTO temps values(datetime('now'), (?))", (25,))
    
    # commit the changes
    conn.commit()

    conn.close() 

def get_data():

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    
    curs.execute("SELECT * FROM temps WHERE timestamp>datetime('now','-%s hours')" % 500)
    
    rows=curs.fetchall()

    conn.close()

    return rows


# get data from the database
records=get_data()
records=str(get_data())
records=records[-10:]
number=int(records[records.find(',')+2:records.find(')')])
print(number)

bLight = b.get_light(3, 'on')

if number<620:
    if bLight:
        lights[2].xy = [0.96,0.96]


savefile(number)
dropbox_upload()
log_temperature(number)
