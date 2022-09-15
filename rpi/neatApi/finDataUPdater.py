import requests
import yfinance as yf
from datetime import datetime, timezone
import json

# TODO:
# [ ]  BASE_URL management
#    - default to production unless a param is passed during init)
#    - default to production unless an environment variable is set
#    - default to localhost unless AWS is identified
# [ ] rename file to something like 'neatApiUpdater'
# [ ] package for use by other modules
# [ ] split this into a subrepository or move to neatApi
# [ ] unit tests
# [ ] rebuild this in C++
# [ ] dockerize / Docker Compose
BASE_URL = "https://www.takushi.us/neatApi/"
BASE_URL = "http://localhost:8000/neatApi/"
SAVEDATA = True
class finDataUpdater():
    def getCurrentDataJson(self):
        apiUrl = BASE_URL + "fins"
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
        apiUrl = BASE_URL + "fin/" + data_p['name']
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
    fdu = finDataUpdater()
    fdu.update()
