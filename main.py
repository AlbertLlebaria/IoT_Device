from machine import I2C, Pin, Timer
from clock import Clock
from time import sleep_ms, ticks_ms, ticks_us
from array import array
import ads1x15
from lora import send_data_to_app
#yellow cable = SCL = PIN9
#green cable = SDA = PIN10

irq_busy = False
index_put = 0
ADC_RATE = 5

gain = 1
addr = 72
_BUFFERSIZE = const(512)

data = array("h", (0 for _ in range(_BUFFERSIZE)))
timestamp = array("L", (0 for _ in range(_BUFFERSIZE)))

i2c = I2C(0, pins=('P10','P9'))     # create and use non-default PIN assignments (P10=SDA, P11=SCL)
adc = ads1x15.ADS1115(i2c, addr, gain)

#
# Interrupt service routine for data acquisition
# called by a timer interrupt
#
def handler( adc = adc.read_rev, data=data, timestamp = timestamp, voltage = adc.raw_to_v):
    global index_put, irq_busy
    if irq_busy:
        return
    irq_busy = True
    if index_put < _BUFFERSIZE:
        timestamp[index_put] = ticks_us()
        raw = adc()
        v = voltage(raw)
        data[index_put] =raw
        index_put += 1
        send_data_to_app(v)
    irq_busy = False

adc.set_conv(7, 0) # start the first conversion
# set the conversion rate to 860 SPS = 1.16 ms; that leaves about
# 3 ms time for processing the data with a 5 ms timer
chrono = Clock(handler, 5)
