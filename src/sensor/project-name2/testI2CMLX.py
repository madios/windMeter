# This example shows using two TSL2491 light sensors attached to TCA9548A channels 0 and 1.
# Use with other I2C sensors would be similar.
import time
import board
import busio
import adafruit_tca9548a
import adafruit_mlx90393
import math

class mlx:
    i2c = busio.I2C(board.SCL, board.SDA)
    tca = adafruit_tca9548a.TCA9548A(i2c)


    def __init__(self):
        self.instance_var1 = 10

def measure(te):
    SENSOR = adafruit_mlx90393.MLX90393(te.tca[0], gain=adafruit_mlx90393.GAIN_5X)
    theta1 = 0
    try:
       MX, MY, MZ = SENSOR.magnetic
       theta1 = math.atan2(MX, MY)
       theta1 = theta1*180/math.pi  
#       print(" ", theta1) 
       if SENSOR.last_status > adafruit_mlx90393.STATUS_OK:
          SENSOR.display_status()
#       time.sleep(0.2)

    except:
       print("error")
    return theta1+180

def main():
#    print("Hello World!")
    te =  mlx()
    peter = measure(te)
    print(peter)

if __name__ == "__main__":
    main()
