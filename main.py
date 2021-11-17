from binance.client import Client
from binance.streams import BinanceSocketManager
from twisted.internet import reactor
from src import historic_dataset
from src import historic_prices
import csv
from config import TEST_API_KEY
from config import TEST_API_SECRET
from config import API_KEY
from config import API_SECRET
from config import TEST_MODE
from config import CREATE_DATASET
from config import TRADING_PAIR_FIRST
from config import TRADING_PAIR_SECOND
from config import TIME_INTERVAL
from config import START_DATE_DAY
from config import START_DATE_MONTH
from config import START_DATE_YEAR
from config import DATASET_FOLDER

api_key = ''
api_secret = ''
if TEST_MODE == True:
    api_key = TEST_API_KEY
    api_secret = TEST_API_SECRET
else:
    api_key = API_KEY
    api_secret = API_SECRET

startdate_str = START_DATE_DAY + ' ' + START_DATE_MONTH + ', ' + START_DATE_YEAR

filename = ''
if CREATE_DATASET == True:
    Dataset = historic_dataset.DatasetCreation(api_key, api_secret)
    filename = Dataset.createCsvDataset(TRADING_PAIR_FIRST + TRADING_PAIR_SECOND, TIME_INTERVAL, startdate_str, DATASET_FOLDER)
    print('Data successfully written to ' + DATASET_FOLDER + filename + ' in format TOHLCV.')
else:
    filename = TRADING_PAIR_FIRST + TRADING_PAIR_SECOND + '_' + TIME_INTERVAL + '_' + START_DATE_DAY + '_' + START_DATE_MONTH + '_' + START_DATE_YEAR + '.csv'
    #print('Data successfully read from ' + DATASET_FOLDER + filename + ' in format TOHLCV.')

BTCUSDT = historic_prices.HistoricPrices(TRADING_PAIR_FIRST + TRADING_PAIR_SECOND)

print('Opening file for reading...')
with open(DATASET_FOLDER + filename) as dataset_csv:
    csv_reader = csv.reader(dataset_csv, delimiter=',')
    line_count = 0
    for row in csv_reader:
        BTCUSDT.addTimestamp(row[BTCUSDT.TIMESTAMP])
        BTCUSDT.addOpenPrice(float(row[BTCUSDT.OPEN]))
        BTCUSDT.addHighPrice(float(row[BTCUSDT.HIGH]))
        BTCUSDT.addLowPrice(float(row[BTCUSDT.LOW]))
        BTCUSDT.addClosePrice(float(row[BTCUSDT.CLOSE]))

print('CSV reading completed for ' + DATASET_FOLDER + filename)

second_pair_amount = 10000
first_pair_amount = (second_pair_amount/BTCUSDT.closePrices[0]) * .9999
first_pair_amount = (first_pair_amount * BTCUSDT.closePrices[-1]) * .9999
print('If you bought ' + str(second_pair_amount) + ' ' + TRADING_PAIR_SECOND + ' of ' + TRADING_PAIR_FIRST + ' on ' \
    + startdate_str + ' it would now be worth: ' + str(first_pair_amount) + ' ' + TRADING_PAIR_SECOND + '.')


########################## IF YOU BUY AND SELL EVERY INTERVAL ##############################
close_prices = BTCUSDT.closePrices
usdt_balance = 0.0
btc_balance = 10000/(close_prices[0])

for price_index in range(len(close_prices)):
    if price_index != 0 and price_index != len(close_prices) - 1:
        if close_prices[price_index] > close_prices[price_index-1]:
            if btc_balance > 50/close_prices[price_index]:
                btc_balance -= 50/close_prices[price_index]
                usdt_balance += 50
            else:
                usdt_balance += btc_balance * close_prices[price_index]
                btc_balance -= btc_balance
        if close_prices[price_index] < close_prices[price_index-1]:
            if usdt_balance > 50:
                btc_balance += 50/close_prices[price_index]
                usdt_balance -= 50
            else:
                btc_balance += usdt_balance/close_prices[price_index]
                usdt_balance -= usdt_balance
    elif price_index == len(close_prices) - 1:
        if btc_balance > 0:
            usdt_balance += btc_balance * close_prices[price_index]
            btc_balance -= btc_balance

print('Final USDT balance is: ' + str(usdt_balance) + ' and final BTC balance is ' \
    + str(btc_balance))
########################################################################################## 
############################ IF YOU TRADE ON MOVING AVERAGE ##############################
MAs5 = BTCUSDT.createMovingAverage(close_prices, 5)
MAs10 = BTCUSDT.createMovingAverage(close_prices, 10)

btc_balance = 0
usdt_balance = 10000

for price_index in range(len(MAs5)):
    if price_index == 10:
        if MAs5[price_index] < MAs10[price_index] and usdt_balance > 0:
            btc_balance = usdt_balance/close_prices[price_index]
            usdt_balance -= usdt_balance
    elif price_index > 10 and MAs5[price_index] < MAs10[price_index] and usdt_balance > 0:
        if MAs5[price_index] < MAs10[price_index]:
            btc_balance = usdt_balance/close_prices[price_index]
            usdt_balance -= usdt_balance
    elif price_index > 10 and MAs5[price_index] > MAs10[price_index] and btc_balance > 0:
        usdt_balance = btc_balance * close_prices[price_index]
        btc_balance -= btc_balance

i = 10
########################################################################################## 














