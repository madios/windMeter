
#!/usr/bin/python
#
import FaBo9Axis_MPU9250
import time
import math
import datetime
import os
import numpy as np
#import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

#maxangle = 10.0 
arr1       = [0,0,0,0,0,0,0,0,0,0]
arr2       = [0,0,0,0,0,0,0,0,0,0]

#GPIO.setwarnings(False) # Ignore warning for now
#GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
#GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class test:

    RAD_TO_DEG = 57.29578
    M_PI = 3.14159265358979323846
    G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
    AA =  0.40      # Complementary filter constant

    magXmin =  -24.0
    magYmin =  -3.9
    magZmin =  -90
    magXmax =  30.388
    magYmax =  44.558
    magZmax =  11

    gyroXangle = 0.0
    gyroYangle = 0.0
    gyroZangle = 0.0
    CFangleX = 0.0
    CFangleY = 0.0
    maxangle = 10.0
    mpu9250 = FaBo9Axis_MPU9250.MPU9250()

    #a = datetime.datetime.now()

    def __init__(self):
        self.instance_var1 = 10

def readSensor(te,maxangle):
#    print("old"+str(maxangle[0]))
#    try:
#        a = datetime.datetime.now()
    accel = te.mpu9250.readAccel()
    gyro = te.mpu9250.readGyro()
    mag = te.mpu9250.readMagnet()
#        while 1<2:
    if 1==1:
        time.sleep(0.1)
        mag = te.mpu9250.readMagnet()
        ACCx = accel['x']
        ACCy = accel['y']
        ACCz = accel['z']
        GYRx = gyro['x']
        GYRy = gyro['y']
        GYRz = gyro['z']
        MAGx = mag['x']
        MAGy = mag['y']
        MAGz = mag['z']
        if MAGx != 0:
            maxangle[0] = min(maxangle[0],MAGx)
            maxangle[1] = min(maxangle[1],MAGy)
            maxangle[2] = min(maxangle[2],MAGz)
            maxangle[3] = max(maxangle[3],MAGx)
            maxangle[4] = max(maxangle[4],MAGy)
            maxangle[5] = max(maxangle[5],MAGz)
            print(str(int(MAGx))+","+str(int(MAGy))+","+str(int(MAGz)))
#            print("x: "+str(MAGx) )
        return maxangle
#    except:
#        print("cound not get measure")
#        ACCx = 1
#        ACCy = 1
#        ACCz = 1
#        GYRx = 1
#        GYRy = 1
#        GYRz = 1
#        MAGx = 1
#        MAGy = 1
#        MAGz = 1

def measure(te,maxangle):
    try:
#        print("per")
        maxangle = np.loadtxt('test1.txt', dtype=float)
#        print(maxangle)
#        print("per1")
        te.magXmin =  maxangle[0]
        te.magYmin =  maxangle[1]
        te.magZmin =  maxangle[2]
        te.magXmax =  maxangle[3]
        te.magYmax =  maxangle[4]
        te.magZmax =  maxangle[5]
 #       a = datetime.datetime.now()
        accel = te.mpu9250.readAccel()
        gyro = te.mpu9250.readGyro()
        mag = te.mpu9250.readMagnet()
#        while 1<2:
        if 1==1:
            time.sleep(0.1)
            mag = te.mpu9250.readMagnet()
            ACCx = accel['x']
            ACCy = accel['y']
            ACCz = accel['z']
            GYRx = gyro['x']
            GYRy = gyro['y']
            GYRz = gyro['z']
            MAGx = mag['x']
            MAGy = mag['y']
            MAGz = mag['z']
#            if MAGx != 0:
                #maxangle[0] = min(maxangle[0],MAGx)
                #maxangle[1] = min(maxangle[1],MAGy)
                #maxangle[2] = min(maxangle[2],MAGz)
                #maxangle[3] = max(maxangle[3],MAGx)
                #maxangle[4] = max(maxangle[4],MAGy)
                #maxangle[5] = max(maxangle[5],MAGz)
#            print("x: "+str(MAGx)+" y: "+str(MAGy)+" z: "+str(MAGz)+ "   "+str(maxangle))
            if MAGx==0 and MAGy==0:
                time.sleep(0.2)
                mag = te.mpu9250.readMagnet()
                MAGx = mag['x']
                MAGy = mag['y']
                MAGz = mag['z']
                if MAGx == 0:
                    print("peter"+str(MAGx))
                    time.sleep(0.2)
                    mag = te.mpu9250.readMagnet()
                    MAGx = mag['x']
                    MAGy = mag['y']
                    MAGz = mag['z']
 #               print("xx: "+str(MAGx)+" y: "+str(MAGy)+" z: "+str(MAGz))
                    time.sleep(0.2)
                    if MAGx == 0:
                        print("peter1"+ str(MAGx))
    except:
        print("cound not get measure")
        ACCx = 1
        ACCy = 1
        ACCz = 1
        GYRx = 1
        GYRy = 1
        GYRz = 1
        MAGx = 1
        MAGy = 1
        MAGz = 1

    MAGx -= (te.magXmin + te.magXmax) /2
    MAGy -= (te.magYmin + te.magYmax) /2
    MAGz -= (te.magZmin + te.magZmax) /2

#    b = datetime.datetime.now() - a
#    a = datetime.datetime.now()
#    LP = b.microseconds/(1000000*1.0)
#    outputString = "Loop Time %5.2f " % ( LP )

    rate_gyr_x =  GYRx * te.G_GAIN
    rate_gyr_y =  GYRy * te.G_GAIN
    rate_gyr_z =  GYRz * te.G_GAIN

#    te.gyroXangle+=rate_gyr_x*LP
#    te.gyroYangle+=rate_gyr_y*LP
#    te.gyroZangle+=rate_gyr_z*LP

    AccXangle =  (math.atan2(ACCy,ACCz)*te.RAD_TO_DEG)
    AccYangle =  (math.atan2(ACCz,ACCx)+te.M_PI)*te.RAD_TO_DEG

    if AccYangle > 90:
        AccYangle -= 270.0
    else:
        AccYangle += 90.0

#    CFangleX=te.AA*(te.CFangleX+rate_gyr_x*LP) +(1 - te.AA) * AccXangle
#    CFangleY=te.AA*(te.CFangleY+rate_gyr_y*LP) +(1 - te.AA) * AccYangle

    heading = 180 * math.atan2(MAGy,MAGx)/te.M_PI

    if heading < 0:
 #       print("heading")
        heading += 360

    accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
    accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)

    pitch = math.asin(accXnorm)
    roll = -math.asin(accYnorm/math.cos(pitch))

    magXcomp = MAGx*math.cos(pitch)+MAGz*math.sin(pitch)
    magYcomp = MAGx*math.sin(roll)*math.sin(pitch)+MAGy*math.cos(roll)-MAGz*math.sin(roll)*math.cos(pitch)   #LSM9DS0
    tiltCompensatedHeading = 180 * math.atan2(magYcomp,magXcomp)/te.M_PI
    #print("heading smaller than 0")

    #if tiltCompensatedHeading < 0:
    #    tiltCompensatedHeading += 360
    #if 1:                       #Change to '0' to stop showing the angles from the accelerometer
    #     outputString1= "# ACCX Angle "+str(AccXangle)+" ACCY Angle"+str(AccYangle) #  " % (AccXangle, AccYangle)
    #if 1:                       #Change to '0' to stop  showing the angles from the gyro
    #     outputString2="\t# GRYX Angle "+str(te.gyroXangle)+"  GYRY Angle "+str(te.gyroYangle)+"  GYRZ Angle"+str(te.gyroZangle) # " % (gyroXangle,gyroYangle,gyroZangle)
    #if 1:                       #Change to '0' to stop  showing the angles from the complementary filter
    #     outputString3="\t# CFangleX Angle "+str(CFangleX)+"   CFangleY Angle"+str(CFangleY) #" % (CFangleX,CFangleY)
    #if 1:                       #Change to '0' to stop  showing the heading
    #     outputString4 ="\t# HEADING "+str(heading)+"  tiltCompensatedHeading "+str(tiltCompensatedHeading) #" % (heading,tiltCompensatedHeading)
#    print(outputString4)
#    print("peter34")
    heading = 360-(tiltCompensatedHeading + 180)
    arr1.pop(0)
    arr2.pop(0)
    arr1.append(np.cos(heading/180*np.pi))
    arr2.append(np.sin(heading/180*np.pi))
    ans = (np.arctan2(np.sum(arr2), np.sum(arr1)) * 180 / np.pi +360 ) % 360
#    return 360-(tiltCompensatedHeading + 180)
    return ans
#    return maxangle
    #time.sleep(0.3)


def main():
#    print("Hello World!")
    i = 0
    #maxangle= [1000,1000,1000,-1000,-1000,-1000]
    maxangle = 0
    #avgHeading = [0,0,0,0,0,0,0,0,0,0]
    #arr1       = [0,0,0,0,0,0,0,0,0,0]
    #arr2       = [0,0,0,0,0,0,0,0,0,0]
    while True:
        try:
#            print("peter")
#            if GPIO.input(10) == GPIO.LOW:
             te =  test()
             maxangle = measure(te,maxangle)
#            avgHeading.pop(0)
#            avgHeading.append(maxangle)
#            arr1.pop(0)
#            arr2.pop(0)
#            arr1.append(np.cos(maxangle/180*np.pi))
#            arr2.append(np.sin(maxangle/180*np.pi))
#            ans = (np.arctan2(np.sum(arr2), np.sum(arr1)) * 180 / np.pi +360 ) % 360
            #print(avgHeading)
#            print("heading: "+str(int(maxangle))+"avgHeaed: "+str(int(sum(avgHeading)/(len(avgHeading))))+"  ans: "+str(int(ans)))
             print("heading: "+str(int(maxangle)))
             time.sleep(0.2)
             i = i + 1
#            else:
#                time.sleep(1)
#                print("calibration")
        except KeyboardInterrupt:
            print("Bye")
            sys.exit()

if __name__ == "__main__":
    main()



