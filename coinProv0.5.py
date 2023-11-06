import sys
import time

import requests
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


form_class = uic.loadUiType("ui/coinPriceUi.ui")[0]



class CoinViewThread(QThread):#시그널 클래스
    #시그널 함수 정의
    coinDataSent = pyqtSignal(float, float,float,float,float,float,float,float,)#8개 정보를 보낼것임.


    def __init__(self):
        super().__init__()
        self.alive = True

    def run(self):
        while self.alive:
            url1 = "https://api.upbit.com/v1/ticker"
            param = {"markets": "KRW-BTC"}
            response = requests.get(url1, params=param)
            result = response.json()

            trade_price = (result[0]["trade_price"])  # 코인의 현재가격
            signed_change_rate = (result[0]["signed_change_rate"])  # 코인의 부호가 있는 변화율
            acc_trade_price_24h = (result[0]["acc_trade_price_24h"])  # 코인의 24시간 누적거래대금
            acc_trade_volume_24h = (result[0]["acc_trade_volume_24h"])  # 코인의 24시간 누적 거래량
            high_price = (result[0]["high_price"])  # 코인의 최고가
            low_price = (result[0]["low_price"])  # 코인의 최저가
            prev_closing_price = (result[0]["prev_closing_price"])  # 코인의 전일종가
            trade_volume = (result[0]["trade_volume"])  # 코인의 가장최근 거래량


            #슬롯에 코인정보 보내주는 함수 호출
            self.coinDataSent.emit(float(trade_price),float(signed_change_rate),float(acc_trade_price_24h),
                                   float(acc_trade_volume_24h),float(high_price),float(low_price),
                                   float(prev_closing_price),float(trade_volume))


            time.sleep(1)#api 호출 딜레이(1초마다 한번씩 업비트에 호출)

    def close(self): #close함수가 호출되면 run 함수 (while)문이 멈춤
        self.alive = False #코인 변경시,프로그램이 멈추지 않으면서, 와일문을 멈추고 다시 런하도록..




class MainWindow(QMainWindow,form_class):#슬롯 클래스

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Coin Price Overview')
        self.setWindowIcon(QIcon('icon/coin1.png'))
        self.statusBar().showMessage('ver 0.5')

        self.cvt = CoinViewThread() #시그널 클래스로 객체 선언
        self.cvt.coinDataSent.connect(self.fillCoindata)
        self.cvt.start()#시그널 함수의 쓰레드를 시작


        #시그널 클래스에서 보내준 코인정보를 ui에 출력해주는 슬롯함수
    def fillCoindata(self,trade_price,signed_change_rate,acc_trade_price_24h,
                      acc_trade_volume_24h,high_price,low_price,prev_closing_price,trade_volume ):

            self.coin_price_label.setText(f"{trade_price:,.0f}")#코인 현재가 출력
            self.coin_changelate_label.setText(f"{signed_change_rate:+.2f}")  # 코인  부호가 있는 변화율/플러스일경우만 부호 붙음
            self.acc_trade_price_label.setText(f"{acc_trade_price_24h:,.0f}")  # 코인 24시간 누적거래대금
            self.acc_trade_volume_label.setText(f"{acc_trade_volume_24h:.4f}")  # 코인 24시간 누적 거래량
            self.high_price_label.setText(f"{high_price:,.0f}")  # 코인의 최고가
            self.low_price_label.setText(f"{low_price:,.0f}")  # 코인의 최저가
            self.prev_closing_price_label.setText(f"{prev_closing_price:,.0f}")  # 코인의 전일종가
            self.trade_volume.setText(f"{trade_volume:.4f}")  #  코인의 가장최근 거래량

if __name__== "__main__":
    app=QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())




