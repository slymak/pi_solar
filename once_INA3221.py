#!/usr/bin/python3
import datetime
import sys
import board

from barbudor_ina3221.lite import INA3221

i2c_bus = board.I2C()
ina3221 = INA3221(i2c_bus)

ina3221.enable_channel(1)	# breadboard
ina3221.enable_channel(2)	# solar
ina3221.enable_channel(3)	# baterka


atmel = float("{:.2f}".format(ina3221.bus_voltage(1)))
ain = float("{:.2f}".format(ina3221.current(1) * 1000))
solar = float("{:.2f}".format(ina3221.bus_voltage(2)))
baterka = float("{:.2f}".format(ina3221.bus_voltage(3)))


dt = datetime.datetime.now()
datum = dt.strftime("%Y-%m-%d %H:%M")



print(f"{datum} atmel {atmel} solar {solar} baterka {baterka}")

