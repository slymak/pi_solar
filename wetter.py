#!/usr/bin/python3
import wetteronline

#l = wetteronline.location("Nové Město pod Smrkem")
#print(l.url)
#print(l.autosuggests)
w = wetteronline.weather("wetter/nove-mesto-pod-smrkem")

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

print(sun_hours)

#f = open("sunhours.txt", "w")
#f.write(",".join(sun_hours))
#f.close
#print(type(w.forecast_4d["18.10."]["sunHours"]))
