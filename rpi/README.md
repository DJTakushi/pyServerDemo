# rpi
A Raspberry Pi is a useful tool for handling tasks.

For example, the yfinance python package takes a lot of time to execute.  Getting a single ticker takes 2+ seconds, which scales up with the eight tickers I currently display.  

Originally I simply had Django doing these updates in the view handling, but that resulted in unacceptable delays in page requests.  AWS Lambda functions offered a clear solution that I implmented for a while.  Reliance on AWS isn't ideal though, and outside of the free-tier trial, I calculated that these Lambda functions could cost me a few bucks each month.  A 20s task run every minute would be:
```
r=$0.0000000021 (Amazon's rate per ms)
r*1000*20*60*24*365/12) = $1.84/month
```
It was a nearly trivial amount, but not the best solution, especially if I were to scale.

The BETTER solution seems to periodically update the data on my own device and update the Django site through an API.  I put the call in `update5min.py`, and run that every 5 min from crontab with the line:
```
*/5 * * * * python /home/danny/takushi/rpi/update5min.py
```

Open Weather has also been selected as the weather data supplier.
According to the pricing page ([https://openweathermap.org/price](https://openweathermap.org/price)), 60 calls/minute is in the Free tier.

The Current Api docs are at [https://openweathermap.org/current](https://openweathermap.org/current)
