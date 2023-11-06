import time

import requests
import pprint #제이슨 파일 출력 하려면 필요
import json #제이슨 파일형태로 url이 들어옴

while True:

    url1 = "https://api.upbit.com/v1/ticker"
    param = {"markets": "KRW-BTC"}
    response = requests.get(url1, params=param)

#print(response.text)
    result =response.json()
    print(result[0]["trade_price"])

    time.sleep(3)

