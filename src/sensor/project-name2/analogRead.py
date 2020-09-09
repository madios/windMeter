import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class analogRead:

    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    # Create the ADC object using the I2C bus
    ads = ADS.ADS1015(i2c)

def __init__(self):
    self.instance_var1 = 10
def measure(te):
    # Create single-ended input on channel 0
    chan = AnalogIn(te.ads, ADS.P0)

    # Create differential input between channel 0 and 1
    #chan = AnalogIn(ads, ADS.P0, ADS.P1)

#    print("{:>5}\t{:>5}".format('raw', 'v'))
    return chan.voltage/5*32.4  
#   chan.value
def main():
    te =  analogRead()
    peter = measure(te)
    print(peter) 


if __name__ == "__main__":
    main()
