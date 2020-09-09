import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import imuheadingTest2
import time
import numpy as np

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

a = np.array([1000, 1000, 1000, -1000, -1000, -1000])
#np.savetxt('test1.txt', a, fmt='%f')
b = np.loadtxt('test1.txt', dtype=float)
print(b)
maxangle= [1000,1000,1000,-1000,-1000,-1000]
#maxangle = np.array([1000, 1000, 1000, -1000, -1000, -1000])
while True: # Run forever
    if GPIO.input(10) == GPIO.HIGH:
        #print("Button was pushed!")
        #maxangle= [1000,1000,1000,-1000,-1000,-1000]
        #maxangle = np.array([1000, 1000, 1000, -1000, -1000, -1000])
        i = 0
        while i<10:
#            try:
            te =  imuheadingTest2.test()
            maxangle = imuheadingTest2.readSensor(te,maxangle)
#            print(maxangle)
            i = i + 1
            time.sleep(0.05)
            np.savetxt('test1.txt', maxangle, fmt='%d')
# pfef
    else:
        maxangle= [1000,1000,1000,-1000,-1000,-1000]
        print("zeros")
        time.sleep(1)
