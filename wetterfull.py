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

dts = datetime.now()
dt  = dts.strftime('%Y-%m-%dt%H:%M')

f = open(f"/var/www/html/digivoltnovakov/logs/4day{dt}", "w")
f.write(str(w.forecast_4d))
f.close

#print(w.forecast_4d)

