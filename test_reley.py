#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

in1 = 22  #ze solaru
in2 = 23  # zarovka
in3 = 24  
in4 = 25  # 230V

GPIO.setmode(GPIO.BCM)
#GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
#GPIO.setup(in3, GPIO.OUT)
#GPIO.setup(in4, GPIO.OUT)


#GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
#GPIO.output(in3, GPIO.LOW)
#GPIO.output(in4, GPIO.LOW)
#time.sleep(3)

#GPIO.output(in1, GPIO.HIGH)
#GPIO.output(in2, GPIO.HIGH)
#GPIO.output(in3, GPIO.HIGH)
#GPIO.output(in4, GPIO.HIGH)

#GPIO.cleanup()


