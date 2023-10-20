#!/usr/bin/python3 -u
import time
from datetime import datetime
import logging
logging.basicConfig(format='%(asctime)s - %(message)s',filename='/var/www/html/digivoltnovakov/logs/solar.log')

import sys
import board
from barbudor_ina3221.lite import INA3221
i2c_bus = board.I2C()
ina3221 = INA3221(i2c_bus)

import RPi.GPIO as GPIO
pinsolar = 22           #solar
pinload = 23           #load h4 bulb 4A
pinrele3 = 24           #not use
pingrid = 25           #grid 230v

############ using values from wetter.py
batf = open("baterry_value","r")
battery_value = float(batf.read())

solarf = open("solar_value","r")
solar_value = float(solarf.read())


#reley
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinsolar, GPIO.OUT)
GPIO.setup(pinload, GPIO.OUT)
GPIO.setup(pingrid, GPIO.OUT)


# def read_ina():
ina3221.enable_channel(1)
ina3221.enable_channel(2)
ina3221.enable_channel(3)

atmel = float("{:.2f}".format(ina3221.bus_voltage(1)))
solar = float("{:.2f}".format(ina3221.bus_voltage(2)))
baterry = float("{:.2f}".format(ina3221.bus_voltage(3)))

time.sleep(1)
dts = datetime.now()
dt  = dts.strftime('%Y-%m-%d %H:%M')

statusgrid = GPIO.input(pingrid)
if statusgrid:
    grid_on = True
    grid_off = False
else:
    grid_on = False
    grid_off = True
    print(f"{dt}   grid ma grid_on {grid_on} grid_off {grid_off} ")

statusload = GPIO.input(pinload)
if statusload:
    load_on = False
    load_off = True
    print(f"{dt}   load ma on {load_on} _off {load_off} ")
else:
    load_on = True
    load_off = False

statussolar = GPIO.input(pinsolar)
if statussolar:
    solar_on = True
    solar_off = False
else:
    solar_on = True
    solar_off = False
    print(f"{dt}   solar ma _on {solar_on} off {solar_off} ")


#---------------- main -------------------------


################# grid on ##############################################

if grid_on == True and solar > baterry and solar > solar_value:
    GPIO.output(pingrid, GPIO.LOW)
    print(f"{dt} 230V off, prave se sit vypla {baterry}")
    logging.warning(f" 230V switch off now, solar {solar} battery {baterry}")
    
# ################# off grid ###############################################


if grid_on == False and baterry > 13.6 and load_off == True:
    GPIO.output(pinload, GPIO.LOW)
    print(f"{dt} load switch ON, baterka ma: {baterry} ze solaru jde:{solar}")
    logging.warning(f" load switch ON now, solar {solar} battery {baterry}")
    
if grid_on == False and baterry > 13.9 and solar_on == True:
    GPIO.output(pinsolar, GPIO.HIGH)
    print(f"{dt} solar switch off now, baterka ma: {baterry} solar je:{solar}")
    logging.warning(f" solar switch off now, solar {solar} battery {baterry}")
    
if grid_on == False and baterry < 13.3 and solar_off == True:
    GPIO.output(pinsolar, GPIO.LOW)
    print(f"{dt} solar switch ON now, baterka ma: {baterry} solar je:{solar}")
    logging.warning(f" solar switch ON now, solar {solar} battery {baterry}")
    
if grid_on == False and baterry < 12.8 and load_on == True:
    GPIO.output(pinload, GPIO.HIGH)
    print(f"{dt} load switch off,baterka ma: {baterry} solar je:{solar}")
    logging.warning(f" load switch off now, solar {solar} battery {baterry}")
    
if grid_on == False and baterry < battery_value:
    GPIO.output(pingrid, GPIO.HIGH)
    print(f"{dt} zapiname 230V zacina grid_on")
    logging.warning(f" grid switch ON now, solar {solar} battery {baterry}")
