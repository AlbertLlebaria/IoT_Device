from machine import UART
import os

print("Running boot")
uart = UART(0, 115200)
os.dupterm(uart)
