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

#dwf time and output
time.sleep(1)
dts = datetime.now()
dt  = dts.strftime('%Y-%m-%d %H:%M')

statusgrid = GPIO.input(pingrid)
if statusgrid:
    grid_on = True
    grid_off = False
    grid_graph =  12.6
    #print(f"{dt}  grid ON U set {solar_value} U real {solar} bat set {battery_value} real {battery}")
else:
    grid_on = False
    grid_off = True
    grid_graph = 12.4
    print(f"{dt}  grid_off U set {solar_value} U real {solar} bat set {battery_value} real {battery}")

statusload = GPIO.input(pinload)
if statusload:
    load_on = False
    load_off = True
    load_graph = 12.8
else:
    load_on = True
    load_off = False
    load_graph = 13
    print(f"{dt}   load on ma {load_on} U set {solar_value} U real {solar} bat set {battery_value} real {battery}")

statussolar = GPIO.input(pinsolar)
if statussolar:
    solar_on = False
    solar_off = True
    solar_graph = 14.2
    print(f"{dt} solar on {solar_on} volty set {solar_value} real {solar} baterka set {battery_value} real {battery}")
else:
    solar_on = True
    solar_off = False
    solar_graph = 14


# writes values into files
output = open("/var/www/html/digivoltnovakov/output", "a")
#output.write(str(dt) + " " + str(solar) + " " + str(battery) +"\n")
output.write(f"{dt} {solar} {battery} {grid_graph} {load_graph} {solar_graph}\n")
output.close

#---------------- main -------------------------
################# grid on ##############################################

if grid_on == True and solar_on == True and solar > battery and solar > solar_value:
    GPIO.output(pingrid, GPIO.LOW)
    print(f"{dt} 230V off, prave se sit vypla U set {solar_value} U real {solar} bat set {battery_value} real {battery}")
    logging.warning(f" 230V switch off, solar set {solar_value} real {solar} battery set {battery_value} real {battery}")
    
# ################# off grid ###############################################


if grid_on == False and battery > 13.6 and load_off == True:
    GPIO.output(pinload, GPIO.LOW)
    print(f"{dt} LOAD switch ON, baterka ma: {battery} ze solaru jde:{solar}")
    logging.warning(f" load switch ON now, solar {solar} battery {battery}")
    
if grid_on == False and battery > 14.1 and solar_on == True:
    GPIO.output(pinsolar, GPIO.HIGH)
    print(f"{dt} SOLAR switch off, baterka ma: {battery} solar je:{solar}")
    logging.warning(f" solar switch off now, solar {solar} battery {battery}")
    
if grid_on == False and battery < 13 and solar_off == True:
    GPIO.output(pinsolar, GPIO.LOW)
    print(f"{dt} solar switch ON now, baterka ma: {battery} solar je:{solar}")
    logging.warning(f" solar switch ON now, solar {solar} battery {battery}")
    
if grid_on == False and battery < 12.8 and load_on == True:
    GPIO.output(pinload, GPIO.HIGH)
    print(f"{dt} load switch off,baterka ma: {battery} solar je:{solar}")
    logging.warning(f" load switch off now, solar {solar} battery {battery}")
    
if grid_on == False and battery < battery_value:
    GPIO.output(pingrid, GPIO.HIGH)
    print(f"{dt} zapiname 230V grid_on U set {solar_value} U real {solar} bat set {battery_value} real {battery}")
    logging.warning(f" grid switch ON now, solar {solar} battery {battery}")

