import sys
import time

import requests
import pyupbit

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



form_class = uic.loadUiType("ui/coinPriceUi.ui")[0]


class CoinViewThread(QThread):  # 시그널 클래스

    # 시그널 함수 정의
    coinDataSent = pyqtSignal(float, float, float, float, float, float, float, float)
    alarmDataSent = pyqtSignal(float) #알람용 현재가격 시그널

    def __init__(self, ticker):
        #메인윈도우에서 시그널 클래스로 객체를 선언할때 티커를 인수로 전달
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:
            url = "https://api.upbit.com/v1/ticker"

            param = {"markets": f"KRW-{self.ticker}"}

            response = requests.get(url, params=param)

            result = response.json()

            trade_price = result[0]['trade_price']  # 비트코인의 현재가격
            signed_change_rate = result[0]['signed_change_rate']  # 부호가 있는 변화율
            acc_trade_price_24h = result[0]['acc_trade_price_24h']  # 24시간 누적 거래대금
            acc_trade_volume_24h = result[0]['acc_trade_volume_24h']  # 24시간 거래량
            high_price = result[0]['high_price']  # 최고가
            low_price = result[0]['low_price']  # 최저가
            prev_closing_price = result[0]['prev_closing_price']  # 전일종가
            trade_volume = result[0]['trade_volume']  # 최근 거래량

            # 슬롯에 코인정보 보내주는 함수 호출
            self.coinDataSent.emit(float(trade_price),
                                   float(signed_change_rate),
                                   float(acc_trade_price_24h),
                                   float(acc_trade_volume_24h),
                                   float(high_price),
                                   float(low_price),
                                   float(prev_closing_price),
                                   float(trade_volume))

            self.alarmDataSent.emit(float(trade_price))#알람용 호출

            time.sleep(1)  # api 호출 딜레이(1초마다 한번씩 업비트 호출)

    def close(self):  # close 함수가 호출되면 run 함수(while문)이 멈춤
        self.alive = False


class MainWindow(QMainWindow, form_class):  # 슬롯 클래스

    def __init__(self, ticker="BTC"):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Coin Price Overview')
        self.setWindowIcon(QIcon('icon/coin1.png.png'))
        self.statusBar().showMessage('ver 0.5')
        self.ticker =ticker

        self.cvt = CoinViewThread(ticker)  # 시그널 클래스로 객체 선언
        self.cvt.coinDataSent.connect(self.fillCoinData)
        self.cvt.alarmDataSent.connect(self.alarmcheck)

        self.cvt.start()  # 시그널 함수의 쓰레드를 시작
        self.coin_combobox_setting() #콤보박스 초기화 셋팅 함수

        self.alarmButton.clicked.connect(self.alarmbutton)
        #알람버튼이 클릭되면 알람시작
        
    def coin_combobox_setting(self):
        tickerlist = pyupbit.get_tickers(fiat="KRW")
        coinTickerList = []
        for ticker in tickerlist:
            #print(ticker[4:])  # 리스트에서 1개씩 뺌/슬라이싱으로 KRW-'제외

            coinTickerList.append(ticker[4:])
        #print(coinTickerList)  # 특정값만 뽑아냄

        coinTickerList.remove("BTC")#티커리스트에서 BTC제거

        coinTickerList = sorted(coinTickerList) #BTC제거 정렬
        coinTickerList=["BTC"]+coinTickerList #BTC가 제일 첫번째

        self.coin_comboBox.addItems(coinTickerList)
        self.coin_comboBox.currentIndexChanged.connect(self.coin_select_combobox)
        #콤보박스의 메뉴 값이 변경되었을때 호출될 함수 설정
    
    def coin_select_combobox(self):
        coin_ticker = self.coin_comboBox.currentText()#콤보박스에서 현재 선택된 티커 텍스트 가져오기
        #print(coin_ticker)
        self.ticker = coin_ticker
        #콤보박스에서 사용자가 선택한 코인 티커 값으로 셀프.티커 값으로 변경
        self.coin_ticker_label.setText(coin_ticker)
        self.cvt.close() #while 문 종료
        self.cvt = CoinViewThread(coin_ticker)
        #새로운 코인 티커로 다시 시그널 클래스 객체선언
        self.cvt.coinDataSent.connect(self.fillCoinData)
        self.cvt.alarmDataSent.connect(self.alarmcheck)
        #다시 시그널 함수 호출
        self.cvt.start()  # 시그널 함수의 쓰레드를 시작
    
    
    # 시그널클래스에서 보내준 코인정보를 ui에 출력해주는 슬롯 함수
    def fillCoinData(self, trade_price, signed_change_rate, acc_trade_price_24h,
                     acc_trade_volume_24h, high_price, low_price, prev_closing_price, trade_volume):
        self.coin_price_label.setText(f"{trade_price:,.0f}원")  # 코인의 현재가 출력
        self.coin_changelate_label.setText(f"{signed_change_rate:+.2f}")  # 가격변화율->소수2자리까지만 표시
        self.acc_trade_price_label.setText(f"{acc_trade_price_24h:,.0f}")  # 24시간 누적 거래금액
        self.acc_trade_volume_label.setText(f"{acc_trade_volume_24h:.4f}")  # 24시간 거래량
        self.high_price_label.setText(f"{high_price:,.0f}")  # 당일 고가
        self.low_price_label.setText(f"{low_price:,.0f}")  # 당일 저가
        self.prev_closing_price_label.setText(f"{prev_closing_price:,.0f}")  # 전일 종가
        self.trade_volume_label.setText(f"{trade_volume:.4f}")  # 최근 거래량
        self.updateStyle()

    def updateStyle(self):
        if '-' in self.coin_changelate_label.text():
            self.coin_changelate_label.setStyleSheet("background-color:blue;color:white;")
            self.coin_price_label.setStyleSheet("color:blue;")
        else:
            self.coin_changelate_label.setStyleSheet("background-color:red;color:white;")
            self.coin_price_label.setStyleSheet("color:red;")




    def alarmbutton(self):
        self.alarmFlag = 0
        if self.alarmButton.text() == '알람시작':#버튼의 텍스트 변경됨
            self.alarmButton.setText('알람중지')#버튼의 텍스트 변경됨
        else:
            self.alarmButton.setText('알람시작')#버튼의 텍스트 변경됨

    def alarmcheck(self,trade_price ):
        if self.alarmButton.text() =='알람중지':
            if self.alarm_price1.text() == '' or self.alarm_price2.text()=='':
                if self.alarmFlag == 0:
                    self.alarmFlag = 1
                    QMessageBox.warning(self, '입력오류', '알람금액을 모두 입력한 후 알람버튼 눌러주세요~!!!')
                    self.alarmButton.setText('알람시작')
            else:
                #print(self.alarmFlag)
                alarm_1=float(self.alarm_price1.text())
                alarm_2=float(self.alarm_price2.text())

            if trade_price>=alarm_1:
                    self.alarmFlag = 1
                    QMessageBox.warning(self,'매도가격도달',f'얼른{self.ticker}매도하세요~!!!')



            if trade_price<=alarm_2:
                    self.alarmFlag = 1
                    QMessageBox.warning(self, '매수가격도달', f'얼른{self.ticker}매수하세요~!!!')





if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

