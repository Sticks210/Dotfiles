from time import sleep
from umqtt.simple import MQTTClient
import machine
import dht

SERVER = '192.168.0.24'
CLIENT_ID = 'ESP32_DHT21_Sensor'
TOPIC0 = 'sensors/temp'
TOPIC1 = 'sensors/humidity'

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()   # Connect to MQTT broker

sensor = dht.DHT11(machine.Pin(25))

while True:
    try:
        sensor.measure()   # Poll sensor
        t = sensor.temperature()
        h = sensor.humidity()
        if isinstance(t, int) and isinstance(h, int):  # Confirm sensor results are numeric
            msg0 = (b'{}'.format(t))
            msg1 = (b'{}'.format(h))
            client.publish(TOPIC0, msg0)  # Publish sensor data to MQTT topic
            client.publish(TOPIC1, msg1)
            print(msg0, "F  ", msg1, "\%")
        else:
            print('Invalid sensor readings.')
    except OSError:
        print('Failed to read sensor.')
    sleep(4)
