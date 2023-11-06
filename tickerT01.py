import requests
import pyupbit



url = "https://api.upbit.com/v1/market/all?isDetails=false"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)

tickerlist = pyupbit.get_tickers(fiat="KRW")

print(tickerlist)

coinTickerList = []
for ticker in tickerlist:
    print(ticker[4:]) #리스트에서 1개씩 뺌/슬라이싱으로 KRW-'제외

    coinTickerList.append(ticker[4:])
print(coinTickerList) #특정값만 뽑아냄
