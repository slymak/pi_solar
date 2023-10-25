#!/usr/bin/python3 -u
import time
from datetime import datetime
import logging
logging.basicConfig(format='%(asctime)s - %(message)s',filename='/var/www/html/digivoltnovakov/logs/controlpin')

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
batf = open("/home/pi/pi_solar/battery_value","r")
battery_value = float(batf.read())
batf.close()

solarf = open("/home/pi/pi_solar/solar_value","r")
solar_value = float(solarf.read())
solarf.close()

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
battery = float("{:.2f}".format(ina3221.bus_voltage(3)))

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
    print(f"{dt}  grid_off {grid_off} ")

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
    print(f"{dt} solar on {solar_on} volty set {solar_value} real {solar} baterka set {battery_value} real {battery}")

#---------------- main -------------------------


################# grid on ##############################################

if grid_on == True and solar > battery and solar > solar_value:
    GPIO.output(pingrid, GPIO.LOW)
    print(f"{dt} 230V off, prave se sit vypla {battery}")
    logging.warning(f" 230V switch off, solar set {solar_value} real {solar} battery set {battery_value} real {battery}")
    
# ################# off grid ###############################################


if grid_on == False and battery > 13.6 and load_off == True:
    GPIO.output(pinload, GPIO.LOW)
    print(f"{dt} LOAD switch ON, baterka ma: {battery} ze solaru jde:{solar}")
    logging.warning(f" load switch ON now, solar {solar} battery {battery}")
    
if grid_on == False and battery > 13.9 and solar_on == True:
    GPIO.output(pinsolar, GPIO.HIGH)
    print(f"{dt} SOLAR switch off, baterka ma: {battery} solar je:{solar}")
    logging.warning(f" solar switch off now, solar {solar} battery {battery}")
    
if grid_on == False and battery < 13.3 and solar_off == True:
    GPIO.output(pinsolar, GPIO.LOW)
    print(f"{dt} solar switch ON now, baterka ma: {battery} solar je:{solar}")
    logging.warning(f" solar switch ON now, solar {solar} battery {battery}")
    
if grid_on == False and battery < 12.8 and load_on == True:
    GPIO.output(pinload, GPIO.HIGH)
    print(f"{dt} load switch off,baterka ma: {battery} solar je:{solar}")
    logging.warning(f" load switch off now, solar {solar} battery {battery}")
    
if grid_on == False and battery < battery_value:
    GPIO.output(pingrid, GPIO.HIGH)
    print(f"{dt} zapiname 230V zacina grid_on")
    logging.warning(f" grid switch ON now, solar {solar} battery {battery}")
