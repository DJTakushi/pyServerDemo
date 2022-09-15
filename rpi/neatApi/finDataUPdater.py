import requests
import yfinance as yf
from datetime import datetime, timezone
import json
import os
# TODO:
# [ ] package for use by other modules
# [ ] unit tests
# [ ] rebuild this in C++
# [ ] dockerize / Docker Compose


SAVEDATA = True
class finDataUpdater():

    def __init__(self, baseUrl = "https://www.takushi.us/"):
        self.baseUrl = baseUrl

    def getCurrentDataJson(self):
        apiUrl = self.baseUrl + "fins"
        response = requests.get(apiUrl)
        output = response.json()
        print(output)
        return output

    def updateDataJson(self, data):
        symbol = data['name']
        print("Processing " + symbol+":")
        data_t = yf.Ticker(symbol).info
        for key in data.keys():
            if key in data_t and key != "name": # do not use 'name' (bitcoin has a 'name' key)
                data[key] = data_t[key]
                print("set i["+ key + "] to "+ str(data[key]))
        data['lastRefresh'] = datetime.now(timezone.utc).isoformat()
        print("set i['lastRefresh'] to "+ data['lastRefresh'])
        return data

    def sendDataJson(self, data_p):
        headers = {"Content-Type": "application/json"}
        apiUrl = self.baseUrl + "fin/" + data_p['name']
        print("apiUrl = "+apiUrl)
        response = requests.put(apiUrl, json=data_p, headers = headers)
        print("sendDataJson response code: "+str(response.status_code))

    def update(self):
        data = self.getCurrentDataJson()
        for i in data:
            i = self.updateDataJson(i)
        if SAVEDATA:
            with open('data.json','w') as f:
                json.dump(data, f)
        for i in data:
            self.sendDataJson(i)

if __name__ == "__main__":
    baseUrl_t = ""
    baseUrl_env = os.environ.get('takushiBaseUrl')
    if baseUrl_env:
        baseUrl_t = baseUrl_env
    baseUrl_t += "neatApi/"

    fdu = finDataUpdater(baseUrl_t)
    fdu.update()
