import time
import busio
import board
import math 
import adafruit_mlx90393

I2C_BUS = busio.I2C(board.SCL, board.SDA)
SENSOR = adafruit_mlx90393.MLX90393(I2C_BUS, gain=adafruit_mlx90393.GAIN_5X)
#SENSOR = adafruit_mlx90393.MLX90393(I2C_BUS)

while True:
    MX, MY, MZ = SENSOR.magnetic
#    print("[{}]".format(time.monotonic()))
#    print("X: {} uT".format(MX))
#    print("Y: {} uT".format(MY))
#    print("Z: {} uT".format(MZ))
    theta2 = math.atan2(MX, MY) 
    print("atan2(1.2, 1.5) : ", theta2*180/math.pi) 
    # 12600 Y -12300
    # 11980 X -12700 
    # Display the status field if an error occured, etc.
    if SENSOR.last_status > adafruit_mlx90393.STATUS_OK:
        SENSOR.display_status()
    time.sleep(0.2)
