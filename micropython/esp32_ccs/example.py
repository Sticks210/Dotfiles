from machine import Pin, I2C
try
    import struct
except ImportError:
    import ustruct as struct
import time
import CCS811

from umqtt.simple import MQTTClient
SERVER = '192.168.0.24'
CLIENT_ID = 'ESP32_CCS811_Sensor'
TOPIC0 = 'sensors/co2'
TOPIC1 = 'sensors/tvoc'

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()

i2c = I2C(scl=Pin(27), sda=Pin(26), freq=115600, timeout=1200)
s = CCS811.CCS811(i2c=i2c, addr=90)
time.sleep(10)
while True:
    if s.data_ready():
        print('eCO2: %d ppm, TVOC: %d ppb' % (s.eCO2, s.tVOC))
        client.publish(TOPIC0, s.eCO2)
        client.publish(TOPIC1, s.tVOC)
        time.sleep(2)
    else:
        time.sleep(10)
