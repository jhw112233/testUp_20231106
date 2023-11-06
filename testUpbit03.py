import time

import requests
import pprint #제이슨 파일 출력 하려면 필요
import json #제이슨 파일형태로 url이 들어옴


url1 = "https://api.upbit.com/v1/ticker"
param = {"markets": "KRW-BTC"}
response = requests.get(url1, params=param)
result =response.json()
print(result[0]["trade_price"]) #코인의 현재가격
print(result[0]["signed_change_rate"]) #코인의 부호가 있는 변화율
print(result[0]["acc_trade_price_24h"]) #코인의 24시간 누적거래대금
print(result[0]["acc_trade_volume_24h"]) #코인의 24시간 누적 거래량
print(result[0]["high_price"]) #코인의 최고가
print(result[0]["low_price"]) #코인의 최저가
print(result[0]["prev_closing_price"]) #코인의 전일종가
print(result[0]["trade_volume"]) #코인의 가장최근 거래량


#trade_price, 최고가, 최저가, 전일종가, 가장최근 거래량,부호가 있는 변화율, 24시간 누적거래대금, 24시간 누적 거래량
#불러옴

#코인의 종류를 고르면, 그 코인의 8가지 정보를 출력//