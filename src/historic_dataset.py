import os 
from binance.client import Client
from binance.streams import BinanceSocketManager
from twisted.internet import reactor
import time
import smtplib
import csv

class DatasetCreation:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client(api_key, api_secret)

    def createCsvDataset(self, trading_pair, interval, start_date, dataset_folder):
        bars = self.client.get_historical_klines(trading_pair, interval, start_date)
        start_date_split = start_date.split(' ')
        start_date_split[1] = start_date_split[1][:-1]
        filename = trading_pair + '_' + interval + '_' + start_date_split[0] + '_' + start_date_split[1] + '_' + start_date_split[2] + '.csv'
        with open(dataset_folder+filename, 'w', newline='') as emptyfile:
            wr = csv.writer(emptyfile)
            for line in bars:
                wr.writerow(line)
        return filename