import os 
from binance.client import Client
from binance.streams import BinanceSocketManager
from twisted.internet import reactor
import time
import smtplib
import csv
import collections

#TOHLCV
TIMESTAMP = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
VOLUME = 5
NUM_OF_COLS = 6

class HistoricPrices:
    TIMESTAMP = 0
    OPEN = 1
    HIGH = 2
    LOW = 3
    CLOSE = 4
    VOLUME = 5
    NUM_OF_COLS = 6

    movingAverage = []

    def __init__(self, assetname, firstpair_bal, secondpair_bal):
        self._assetname = assetname
        self._firstpair_bal = firstpair_bal
        self._secondpair_bal = secondpair_bal
        self._kline_data = [[] for i in range(NUM_OF_COLS)]

    @property
    def TradingPair(self):
        return self._assetname
    @TradingPair.setter
    def TradingPair(self,  trading_pair):
        self._assetname = trading_pair

    @property
    def firstTradingPairBalance(self):
        return self._firstpair_bal
    @firstTradingPairBalance.setter
    def firstTradingPairBalance(self,  firstpair_bal):
        self._firstpair_bal = firstpair_bal

    @property
    def secondTradingPairBalance(self):
        return self._secondpair_bal
    @secondTradingPairBalance.setter
    def secondTradingPairBalance(self,  secondpair_bal):
        self._secondpair_bal = secondpair_bal

    @property
    def Timestamps(self):
        return self._kline_data[self.TIMESTAMP]
    def addTimestamp(self, timestamp):
        self._kline_data[self.TIMESTAMP].append(timestamp)
    @Timestamps.setter
    def Timestamps(self, timestamps):
        self._kline_data[self.TIMESTAMP] = timestamps

    @property
    def openPrices(self):
        return self._kline_data[self.OPEN]
    def addOpenPrice(self, openprice):
        self._kline_data[self.OPEN].append(openprice)
    @openPrices.setter
    def openPrices(self, openprices):
        self._kline_data[self.OPEN] = openprices

    @property
    def highPrices(self):
        return self._kline_data[self.HIGH]
    def addHighPrice(self, highprice):
        self._kline_data[self.HIGH].append(highprice)
    @highPrices.setter
    def highPrices(self, highprices):
        self._kline_data[self.HIGH] = highprices

    @property
    def lowPrices(self):
        return self._kline_data[self.LOW]
    def addLowPrice(self, lowprice):
        self._kline_data[self.LOW].append(lowprice)
    @lowPrices.setter
    def lowPrices(self, lowprices):
        self._kline_data[self.LOW] = lowprices


    @property
    def closePrices(self):
        return self._kline_data[self.CLOSE]
    def addClosePrice(self, closeprice):
        self._kline_data[self.CLOSE].append(closeprice)
    @closePrices.setter
    def closePrices(self, closeprices):
        self._kline_data[self.CLOSE] = closeprices


    @property
    def Volumes(self):
        return self._kline_data[self.VOLUME]
    def addVolume(self, volume):
        self._kline_data[self.VOLUME].append(volume)
    @Volumes.setter
    def Volumes(self, volumes):
        self._kline_data[self.VOLUME] = volumes

    def createMovingAverage(self, prices, interval): # length = 20, interval is 5
        self.movingAverage = []
        sum = 0
        tempvals = collections.deque()
        for fillnull in range(interval):
            tempvals.append(0)
            
        for price_index in range(len(prices)):
            sum = 0
            prices[price_index]
            tempvals.append(prices[price_index])
            if len(tempvals) == interval:
                for price_index_sum in range(len(tempvals)):
                    sum += tempvals[price_index_sum]
                self.movingAverage.append(sum/interval)
                tempvals.popleft()
        return self.movingAverage

    def sellFirstOfFirstValue(self, amount, price, fee):
        if amount >= self.firstTradingPairBalance:
            self.secondTradingPairBalance += ((100-fee)/100) * self.firstTradingPairBalance * price
            self.firstTradingPairBalance -= self.firstTradingPairBalance
        elif amount < self.firstTradingPairBalance and amount > 0:
            self.secondTradingPairBalance += ((100-fee)/100) * amount * price
            self.firstTradingPairBalance -= amount
        
    def buyFirstOfSecondValue(self, amount, price, fee):
        if amount >= self.secondTradingPairBalance:
            self.firstTradingPairBalance += ((100-fee)/100) * (self.secondTradingPairBalance / price)
            self.secondTradingPairBalance -= self.secondTradingPairBalance
        elif amount < self.secondTradingPairBalance and amount > 0:
            self.firstTradingPairBalance += ((100-fee)/100) * (amount / price)
            self.secondTradingPairBalance -= amount
    
    def sellFirstOfSecondValue(self, amount, price, fee):
        if amount/price >= self.firstTradingPairBalance:
            self.secondTradingPairBalance += ((100-fee)/100) * (self.firstTradingPairBalance * price)
            self.firstTradingPairBalance -= self.firstTradingPairBalance
        elif amount/price < self.firstTradingPairBalance:
            self.secondTradingPairBalance += ((100-fee)/100) * amount
            self.firstTradingPairBalance -= amount / price

    def buyFirstOfFirstValue(self, amount, price, fee):
        if amount*price >= self.secondTradingPairBalance:
            self.firstTradingPairBalance += ((100-fee)/100) * self.secondTradingPairBalance/price
            self.secondTradingPairBalance -= self.secondTradingPairBalance
        elif amount*price < self.secondTradingPairBalance:
            self.firstTradingPairBalance += ((100-fee)/100) * amount
            self.secondTradingPairBalance -= amount * price


        # self.firstTradingPairBalance += (amount/price) * ((100-fee)/100)
        # self.secondTradingPairBalance -= amount



    






    


    

