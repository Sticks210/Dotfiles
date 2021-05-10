try:
    import struct
except ImportError:
    import ustruct as struct

# Connect the sensor TX pin to the board 25 pin
#                    RX pin to the board 26 pin
# For use with a microcontroller board:
import machine
uart = machine.UART(1, baudrate=9600, tx=18, rx=17, timeout=2000)

buffer = []
from time import sleep
from umqtt.simple import MQTTClient

SERVER = '192.168.0.24'
CLIENT_ID = 'ESP32_PMS5003_Sensor'
TOPIC0 = 'sensors/particles/pm10_std'
TOPIC1 = 'sensors/particles/pm25_std'
TOPIC2 = 'sensors/particles/pm100_std'
TOPIC3 = 'sensors/particles/03um'
TOPIC4 = 'sensors/particles/05um'
TOPIC5 = 'sensors/particles/10um'
TOPIC6 = 'sensors/particles/25um'
TOPIC7 = 'sensors/particles/50um'
TOPIC8 = 'sensors/particles/100um'

client = MQTTClient(CLIENT_ID, SERVER)
client.connect()

while True:
    data = uart.read(32)  # read up to 32 bytes
    data = list(data)
    # print("read: ", data)          # this is a bytearray type

    buffer += data

    while buffer and buffer[0] != 0x42:
        buffer.pop(0)

    if len(buffer) > 200:
        buffer = []  # avoid an overrun if all bad data
    if len(buffer) < 32:
        continue

    if buffer[1] != 0x4d:
        buffer.pop(0)
        continue

    frame_len = struct.unpack(">H", bytes(buffer[2:4]))[0]
    if frame_len != 28:
        buffer = []
        continue

    frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))

    pm10_standard, pm25_standard, pm100_standard, pm10_env, \
        pm25_env, pm100_env, particles_03um, particles_05um, particles_10um, \
        particles_25um, particles_50um, particles_100um, skip, checksum = frame

    check = sum(buffer[0:30])

    if check != checksum:
        buffer = []
        continue

    msg0 = (b'PM 1.0 standard: {}'.format(pm10_standard))
    msg1 = (b'PM 2.5 standard: {}'.format(pm25_standard))
    msg2 = (b'PM 10 standard: {}'.format(pm100_env))
    msg3 = (b'Particles > 0.3um / 0.1L air: {}'.format(particles_03um))
    msg4 = (b'Particles > 0.5um / 0.1L air: {}'.format(particles_05um))
    msg5 = (b'Particles > 1.0um / 0.1L air: {}'.format(particles_10um))
    msg6 = (b'Particles > 2.5um / 0.1L air: {}'.format(particles_25um))
    msg7 = (b'Particles > 5.0um / 0.1L air: {}'.format(particles_50um))
    msg8 = (b'Particles > 10um / 0.1L air: {}'.format(particles_100um))
    client.publish(TOPIC0, msg0)
    client.publish(TOPIC1, msg1)
    client.publish(TOPIC2, msg2)
    client.publish(TOPIC3, msg3)
    client.publish(TOPIC4, msg4)
    client.publish(TOPIC5, msg5)
    client.publish(TOPIC6, msg6)
    client.publish(TOPIC7, msg7)
    client.publish(TOPIC8, msg8)

    print("Concentration Units (standard)")
    print("---------------------------------------")
    print("PM 1.0: %d\tPM2.5: %d\tPM10: %d" %
          (pm10_standard, pm25_standard, pm100_standard))
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", particles_03um)
    print("Particles > 0.5um / 0.1L air:", particles_05um)
    print("Particles > 1.0um / 0.1L air:", particles_10um)
    print("Particles > 2.5um / 0.1L air:", particles_25um)
    print("Particles > 5.0um / 0.1L air:", particles_50um)
    print("Particles > 10 um / 0.1L air:", particles_100um)
    print("---------------------------------------")

    buffer = buffer[32:]
    # print("Buffer ", buffer)
