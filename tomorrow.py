#!/usr/bin/python3
#curl -s 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=50.925&lon=15.238'|json_pp
#curl --compressed --request GET --url 'https://api.tomorrow.io/v4/timelines?location=50.924757488151194,15.238067189496318&fields=cloudCover&timesteps=1h&units=metric&apikey=VwAfGkpWOeQvt0m7bqMILpjyz8Iqz6vY'

import json
import requests
#from urllib.request import Request, urlopen

# Read forecast
url='https://api.tomorrow.io/v4/timelines'

querystring = {
"location":"50.924757488151194, 15.238067189496318",
"fields":["temperature","cloudCover"],
"units":"metric",
"timestamps":"2d",
"apikey":"VwAfGkpWOeQvt0m7bqMILpjyz8Iqz6vY"
}

response = requests.request("GET", url, params=querystring)
#print(response.text)

#t = response.json()['data']['timelines'][0]['intervals'][0]['values']['temperature']
#print(t)

results = response.json()['data']['timelines'][0]['intervals']
for daily_result in results:
    date = daily_result['startTime'][0:13]
    cloud = round(daily_result['values']['cloudCover'])
    temp = round(daily_result['values']['temperature'])
    print(date," teplota ",temp," cloud " ,cloud)



#url = "https://api.met.no/weatherapi/locationforecast/2.0/complete?lat=59.911491&lon=10.757933"
#req = Request(url)
#req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Python/3.10.5')
#content: bytes = urlopen(req).read()

# Convert to JSON
#json_str: str = content.decode('utf8').replace("'", '"')
#json_data = json.loads(json_str)

# Print data
#type = json_data['properties']['timeseries'][0]['data']['instant']['details']
#print(f"{type}")




#data = requests.get(url, headers=HEADERS).json()
#return data['properties']['timeseries'][0]['data']['instant']['details']
