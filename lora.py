import binascii
import pycom
import socket
import time
import struct
from network import LoRa

# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff

# Turn off heartbeat LED
pycom.heartbeat(False)

# Initialize LoRaWAN radio
lora = LoRa(mode=LoRa.LORAWAN)

# Set network keys
app_eui = binascii.unhexlify('70B3D57ED0018FFF')
app_key = binascii.unhexlify('A693EDE05F217BB6283C0E6CAEFF512A')

# Join the network
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# Loop until joined
while not lora.has_joined():
    print('Not joined yet...')
    time.sleep(2)

print('Joined')

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(True)


def send_data_to_app(value):
    ba = bytearray(struct.pack("f", value))
    bytes =[ "0x%02x" % b for b in ba ]
    print(bytes, value)
    s.send(ba)
