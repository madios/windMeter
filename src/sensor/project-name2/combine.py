import numpy as np

import imuheadingTest2
import testI2CMLX
import time

def getWindDirection():
    arr1 = [0, 0]
    arr2 = [0, 0]


    imu = imuheadingTest2.test()
    mlx1 = testI2CMLX.mlx()
    heading = (imuheadingTest2.measure(imu,0))
    #heading = 10

#    arr1[0]  =  np.cos(heading/180*np.pi)
#    arr2[0]  =  np.sin(heading/180*np.pi)

    dir = (testI2CMLX.measure(mlx1)-45)%360
    #dir = 300

#    arr1[1]  = np.cos(dir/180*np.pi)
#    arr2[1]  = np.sin(dir/180*np.pi)
#    print(heading)
#    print(dir)
#    ans = np.arctan2(np.sum(arr2), np.sum(arr1)) * 180 / np.pi 

    ans = heading + dir
    ans = ans % 360

    if ans <0:
        ans = ans + 360
#    print(ans)
    print("head: "+str('{0:.0f}'.format(heading))+" dir: "+str('{0:.0f}'.format(dir))+" combine: "+str('{0:.0f}'.format(ans)))
    return ans

def main():
    while True:
        peter = getWindDirection()
#        print(peter) 
        time.sleep(0.2)


if __name__ == "__main__":
    main()

