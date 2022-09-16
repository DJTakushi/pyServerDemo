import requests
from datetime import datetime, timezone
import json
import os
BASEURL_DEFAULT = "https://www.takushi.us/"
# BASEURL_DEFAULT = "http://localhost:8000/"
openWeatherApiKey = os.environ.get('openWeatherApiKey')
SAVEDATA = True

def printDict(d):
    for k in d.keys():
        print("["+k+"] = "+str(d[k]))

class weatherUpdater():
    def __init__(self, baseUrl = BASEURL_DEFAULT):
        self.baseUrl = baseUrl+"neatApi/"
        print("self.baseUrl = "+self.baseUrl)
    def getCurrentDataJson(self):
        apiUrl = self.baseUrl + "cities"
        response = requests.get(apiUrl)
        output = response.json()
        print(output)
        return output
    def updateDataJson(self, data_p):
        api_url = "https://api.openweathermap.org/data/2.5/weather?"
        api_url += "appid=" + openWeatherApiKey
        api_url += "&lat="+str(data_p['latitude'])
        api_url += "&lon="+str(data_p['longitude'])
        response = requests.get(api_url)
        data = response.json()
        # print("data from API:")
        # printDict(data)

        data_p['lastRefresh'] = datetime.now(timezone.utc).isoformat()
        data_p['tz_int']=data['timezone']
        data_p['temp_c']=data['main']['temp']-273.15
        data_p['temp_f']=1.8*(data['main']['temp'])-459.67
        data_p['humidity']=data['main']['humidity']
        data_p['conditionIcon']="http://openweathermap.org/img/wn/"+data['weather'][0]['icon']+"@2x.png"


    def sendDataJson(self, data_p):
        headers = {"Content-Type": "application/json"}
        apiUrl = self.baseUrl + "city/" + data_p['name']
        print("apiUrl = "+apiUrl)
        response = requests.put(apiUrl, json=data_p, headers = headers)
        print("sendDataJson response code: "+str(response.status_code))

    def update(self):
        data = self.getCurrentDataJson()
        for i in data:
            self.updateDataJson(i)
            print("data updated to:")
            printDict(i)
            self.sendDataJson(i)
        if SAVEDATA:
            with open('dataWeather.json','w') as f:
                json.dump(data, f)


if __name__ == "__main__":
    baseUrl_env = os.environ.get('takushiBaseUrl')
    if baseUrl_env:
        wu = weatherUpdater(baseUrl_env)
    else:
        wu = weatherUpdater()
    wu.update()
