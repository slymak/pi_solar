#!/usr/bin/python3
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

def extract_sunhours(weather_data):
  sun_hours = []
  for date in weather_data:
    sun_hours.append(weather_data[date]['sunHours'])
  return sun_hours

sun_hours = extract_sunhours(w.forecast_4d)
first_hour = str(sun_hours[0])

# print(first_hour)

if first_hour == 0:
  baterry_value = 12.8
  solar_value = 13.6
elif first_hour == 1:
  baterry_value = 12.6
  solar_value = 13.5
elif first_hour == 2:
  baterry_value = 12.4
  solar_value = 13.3
elif first_hour == 3:
  baterry_value = 12.3
  solar_value = 13.1
elif first_hour > 3:
  baterry_value = 12.1
  solar_value = 12.8  

f = open("baterry_value", "w")
f.write(str(baterry_value))
f.close


f = open("solar_value", "w")
f.write(str(solar_value))
f.close
