#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

solar = 22  #ze solaru
load = 23  # zarovka
in3 = 24
grid = 25  # 230V

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(solar, GPIO.OUT)
GPIO.setup(load, GPIO.OUT)
GPIO.setup(grid, GPIO.OUT)

				# ON
GPIO.output(solar, GPIO.LOW)
#GPIO.output(load, GPIO.LOW)
GPIO.output(grid, GPIO.LOW)
#time.sleep(3)
				# off
#GPIO.output(solar, GPIO.HIGH)
GPIO.output(load, GPIO.HIGH)
#GPIO.output(grid, GPIO.HIGH)

#GPIO.cleanup()


