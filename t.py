
if False:
    from datetime import datetime, timezone
    import pytz
    utc_dt=datetime.now(timezone.utc)
    JST=pytz.timezone('EasternTime')
    output = "{}".format(utc_dt.astimezone(JST).isoformat())
    time = output.split("T")[-1]
    timeList = time.split(":")
    timeOut = timeList[0]+":"+timeList[1]
    print(timeOut + " " + JST.zone)


if False:
    import yaml
    config = yaml.safe_load(open("takushi/static/takushi/keys/keys.yml"))
    print(config['weatherApi'])

    import requests
    api_url = "http://api.weatherapi.com/v1/current.json"
    api_url += "?key="+config['weatherApi']
    api_url += "&q=Osaka&aqi=yes"
    print("api_url = "+api_url)

    response = requests.get(api_url)
    responseJSON = response.json()
    print("name = "+ responseJSON['location']['name'])
    print("localtime = "+responseJSON['location']['localtime'])
    print("temp_c = "+str(responseJSON['current']['temp_c']))
    print("temp_f = "+str(responseJSON['current']['temp_f']))
    print("humidity = "+str(responseJSON['current']['humidity']))


import yfinance as yf
import time

start_time = time.time()
msft = yf.Ticker("MSFT")
print(msft.info['currentPrice'])
print("--- %s seconds ---" % (time.time() - start_time))


# msft.info

# hist = msft.history(period="max")
# print(hist)
#
# print(msft.institutional_holders)
