import requests
import yfinance as yf
from datetime import datetime

LOCAL_TZ = datetime.now().astimezone().tzinfo
BASE_URL = "https://www.takushi.us/neatApi/"
class finDataUpdater():
    def getCurrentDataJson(self):
        apiUrl = BASE_URL + "fins"
        response = requests.get(apiUrl)
        output = response.json()
        print(output)
        return output


    def updateDataJson(self, data):
        for i in data:
            symbol = i['name']
            print("Processing " + symbol+":")
            # print(i)
            data_i = yf.Ticker(symbol).info
            for key in i.keys():
                if key in data_i:
                    i[key] = data_i[key]
                    print("set i["+ key + "] to "+ str(i[key]))
            i['lastRefresh'] = datetime.now(LOCAL_TZ)
        return data

    def sendDataJson(self, data):
        apiUrl = BASE_URL + "fins"
        response = requests.put(BASE_URL, data = data)
        print("sendDataJson response code: "+str(response.status_code))

    def update(self):
        data = self.getCurrentDataJson()
        data = self.updateDataJson(data)
        self.sendDataJson(data)

if __name__ == "__main__":
    fdu = finDataUpdater()
    fdu.update()
