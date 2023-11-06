import time

import requests
import pprint #제이슨 파일 출력 하려면 필요
import json #제이슨 파일형태로 url이 들어옴

# while True:

url3 = "https://api.upbit.com/v1/market/all"
param = {"markets": "KRW-BTC"}
response = requests.get(url3, params=param)

#print(response.text)
result =response.json()
print(result[1]["english_name"])

url2 = "https://api.upbit.com/v1/market/all"
param = {"markets": "KRW-BTC"}
response = requests.get(url2, params=param)

print(response.text)


