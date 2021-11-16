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

    def __init__(self, assetname):
        self._assetname = assetname
        empty_lst = []
        self._kline_data = [[] for i in range(NUM_OF_COLS)]


    @property
    def Timestamps(self):
        return self._kline_data[TIMESTAMP]

    def addTimestamp(self, timestamp):
        self._kline_data[TIMESTAMP].append(timestamp)

    @Timestamps.setter
    def Timestamps(self, timestamps):
        self._kline_data[TIMESTAMP] = timestamps


    @property
    def openPrices(self):
        return self._kline_data[OPEN]

    def addOpenPrice(self, openprice):
        sze = len(self._kline_data)
        self._kline_data[OPEN].append(openprice)

    @openPrices.setter
    def openPrices(self, openprices):
        self._kline_data[OPEN] = openprices


    @property
    def highPrices(self):
        return self._kline_data[HIGH]

    def addHighPrice(self, highprice):
        self._kline_data[HIGH].append(highprice)

    @highPrices.setter
    def highPrices(self, highprices):
        self._kline_data[HIGH] = highprices

    
    @property
    def lowPrices(self):
        return self._kline_data[LOW]

    def addLowPrice(self, lowprice):
        self._kline_data[LOW].append(lowprice)

    @lowPrices.setter
    def lowPrices(self, lowprices):
        self._kline_data[LOW] = lowprices


    @property
    def closePrices(self):
        return self._kline_data[CLOSE]

    def addClosePrice(self, closeprice):
        self._kline_data[CLOSE].append(closeprice)

    @closePrices.setter
    def closePrices(self, closeprices):
        self._kline_data[CLOSE] = closeprices


    # @property
    # def Volumes(self):
    #     return self._kline_data[VOLUME]

    # def addVolume(self, volume):
    #     self._kline_data[VOLUME].append(volume)

    # @Volumes.setter
    # def closePrices(self, volumes):
    #     self._kline_data[VOLUME] = volumes

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



    


    

