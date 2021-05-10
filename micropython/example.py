from machine import Pin, I2C
import time
import CCS811





def main():
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    s = CCS811.CCS811(i2c=i2c, addr=90)
    # time.sleep(20)
    while True:
        if s.data_ready():
            print('eCO2: %d ppm, TVOC: %d ppb' % (s.eCO2, s.tVOC))
            time.sleep(3)

main()
