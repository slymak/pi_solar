#!/usr/bin/python3
battery_value = 13
solar_value = 13.8


f = open("/home/pi/pi_solar/battery_value", "w")
f.write(str(battery_value))
f.close


f = open("/home/pi/pi_solar/solar_value", "w")
f.write(str(solar_value))
f.close
