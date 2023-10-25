#!/usr/bin/python3
from datetime import datetime
import wetteronline
w = wetteronline.weather("wetter/nove-mesto-pod-smrkem")


#l = wetteronline.location("Nové Město pod Smrkem")
#print(l.url)
#print(l.autosuggests)

#print(w.temperature_now)
#print(w.forecast_24h[list(w.forecast_24h)[0]])

#for i in w.forecast_24h:
#    print(i, w.forecast_24h[i])
#    print()
#print(type(w.forecast_24h))

#single = w.forecast_24h[list(w.forecast_24h)[0]]
#print(list(w.forecast_24h)[0])
#for i in list(single):
#    print(f"{i}: {single[i]}")

#with open("outfile2.html", "w") as f:
#    f.write(w.debug_raw_html)

#with open("outfile3.html", "w") as f:
#    f.write(str(w.forecast_24h))

#print(w.forecast_4d)

dts = datetime.now()
dt  = dts.strftime('%Y-%m-%d %H:%M')



def extract_sunhours(weather_data):
  sun_hours = []
  for date in weather_data:
    sun_hours.append(weather_data[date]['sunHours'])
  return sun_hours

sun_hours = extract_sunhours(w.forecast_4d)
first_hour = sun_hours[0]

print(f"{dt} {first_hour}")

if first_hour == 0:
  battery_value = 12.9
  solar_value = 13.6
elif first_hour == 1:
  battery_value = 12.8
  solar_value = 13.5
elif first_hour == 2:
  battery_value = 12.7
  solar_value = 13.4
elif first_hour == 3:
  battery_value = 12.5
  solar_value = 13.2
elif first_hour == 4:
  battery_value = 12.5
  solar_value = 13.1
elif first_hour == 5:
  battery_value = 12.5
  solar_value = 13
elif first_hour == 6:
  battery_value = 12.2
  solar_value = 13.2
elif first_hour > 7:
  battery_value = 12.1
  solar_value = 12.8

f = open("battery_value", "w")
f.write(str(battery_value))
f.close


f = open("solar_value", "w")
f.write(str(solar_value))
f.close

