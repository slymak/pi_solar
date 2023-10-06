#!/usr/bin/python3 -u
pause = 63

import time
import datetime
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

#reley
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinsolar, GPIO.OUT)
GPIO.setup(pinload, GPIO.OUT)
GPIO.setup(pingrid, GPIO.OUT)


def read_ina():
    ina3221.enable_channel(1)
    ina3221.enable_channel(2)
    ina3221.enable_channel(3)

    atmel = float("{:.2f}".format(ina3221.bus_voltage(1)))
    solar = float("{:.2f}".format(ina3221.bus_voltage(2)))
    baterry = float("{:.2f}".format(ina3221.bus_voltage(3)))

    time.sleep(1)

    status = GPIO.input(pingrid)
    if status:
        grid_on = True
        grid_off = False
    else:
        grid_on = False
        grid_off = True
        print(f"   grid ma grid_on {grid_on} grid_off {grid_off} ")

    status = GPIO.input(pinload)
    if status:
        load_on = False
        load_off = True
        print(f"   load ma on {load_on} _off {load_off} ")
    else:
        load_on = True
        load_off = False

    status = GPIO.input(pinsolar)
    if status:
        solar_on = True
        solar_off = False
    else:
        solar_on = True
        solar_off = False
        print(f"   solar ma _on {solar_on} off {solar_off} ")

    ina = dict()
    ina['atmel'] = atmel
    ina['solar'] = solar
    ina['baterry'] = baterry
    ina['grid_on'] = grid_on
    ina['grid_off'] = grid_off
    ina['load_on'] = load_on
    ina['load_off'] = load_off
    ina['solar_on'] = solar_on
    ina['solar_off'] = solar_off

    return ina

#---------------- main -------------------------
while True:
    read_ina()
    ina = read_ina()
################# grid on ##############################################
    while ina['grid_on']:
        print(f" 230V ON while baterka ma: {ina['baterry']} ze solaru jde:{ina['solar']}")
        time.sleep(pause)
        read_ina()
        ina = read_ina()
        if ina['solar'] > ina['baterry'] and ina['solar'] > 13.0:
            GPIO.output(pingrid, GPIO.LOW)
            print(f" 230V off, prave se sit vypla {ina['baterry']}")
            logging.warning(f" 230V switch off now, solar {ina['solar']} battery {ina['baterry']}")
            time.sleep(3)
            read_ina()
            ina = read_ina()

        if ina['grid_off'] == True:
            break

################# off grid ###############################################
    while ina['grid_off']:
        print(f"off 230V neni, bat {ina['baterry']} sol {ina['solar']}")
        time.sleep(pause)
        read_ina()
        ina = read_ina()

        if ina['baterry'] > 13.2 and ina['load_off'] == True:
            GPIO.output(pinload, GPIO.LOW)
            print(f" load switch ON, baterka ma: {ina['baterry']} ze solaru jde:{ina['solar']}")
            logging.warning(f" load switch ON now, solar {ina['solar']} battery {ina['baterry']}")
            time.sleep(pause)
            read_ina()
            ina = read_ina()
            time.sleep(3)

        if ina['baterry'] > 13.4 and ina['solar_on'] == True:
            GPIO.output(pinsolar, GPIO.HIGH)
            print(f" solar switch off now, baterka ma: {ina['baterry']} solar je:{ina['solar']}")
            logging.warning(f" solar switch off now, solar {ina['solar']} battery {ina['baterry']}")
            time.sleep(pause)
            read_ina()
            ina = read_ina()
            time.sleep(3)

        if ina['baterry'] < 13.3 and ina['solar_off'] == True:
            GPIO.output(pinsolar, GPIO.LOW)
            print(f" solar switch ON now, baterka ma: {ina['baterry']} solar je:{ina['solar']}")
            logging.warning(f" solar switch ON now, solar {ina['solar']} battery {ina['baterry']}")
            time.sleep(pause)
            read_ina()
            ina = read_ina()
            time.sleep(3)

        if ina['baterry'] < 12.7 and ina['load_on'] == True:
            GPIO.output(pinload, GPIO.HIGH)
            print(f" load switch off,baterka ma: {ina['baterry']} solar je:{ina['solar']}")
            logging.warning(f" load switch off now, solar {ina['solar']} battery {ina['baterry']}")
            time.sleep(pause)
            read_ina()
            ina = read_ina()
            time.sleep(3)

        if ina['baterry'] < 12.4:
            GPIO.output(pingrid, GPIO.HIGH)
            print(f" zapiname 230V zacina grid_on")
            logging.warning(f" grid switch ON now, solar {ina['solar']} battery {ina['baterry']}")
            time.sleep(pause)
            read_ina()
            ina = read_ina()
            time.sleep(3)

        if ina['grid_on'] == True:
            break





# except KeyboardInterrupt:
#     print("intentionaly interrupted ")
#     GPIO.cleanup()
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(pingrid, GPIO.OUT)
#     GPIO.output(pingrid, GPIO.HIGH)
# else:
    # print("konec po else")
