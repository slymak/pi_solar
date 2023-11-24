#!/usr/bin/python3
battery_value = 12.7
solar_value = 13.6


f = open("/home/pi/pi_solar/battery_value", "w")
f.write(str(battery_value))
f.close


f = open("/home/pi/pi_solar/solar_value", "w")
f.write(str(solar_value))
f.close
