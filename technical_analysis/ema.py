from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime
import pytz
#from data_collection.continuous import simple_time_series

class ema_indicator:
    def __init__(self, symbol, time_period, interval, series_type):
        # Your Alpha Vantage API Key
        self.Key = 'EXNB75FRYOME205S'

        # Initialize the TechIndicators object with the API key
        self.techInd = TechIndicators(key=self.Key, output_format='pandas')
        self.timeSeries = TimeSeries(key=self.Key, output_format='pandas')
        # Fetch EMA data for AAPL with a specific time period
        self.symbol = symbol
        self.time_period = time_period
        self.interval = interval
        self.series_type = series_type

        # Call get_ema with the correct parameters
        self.ema, self.meta_data = self.techInd.get_ema(symbol=self.symbol, interval=self.interval, time_period=self.time_period, series_type=self.series_type)

        # Fetch the stock price data (intraday with 60min interval in this case)
        self.stock_data, self.stock_meta_data = self.timeSeries.get_intraday(symbol=self.symbol, interval=self.interval, outputsize='full')
        #print(self.stock_data.head())

        # Assuming the EMA column is named 'EMA', adjust if necessary
        self.ema_column = self.ema[f'EMA']

    def position(self):
        result = []
        for i in range(300,-1,-1):
            date = self.ema.index[i]
            ema_value = self.ema_column.iloc[i]

            if date in self.stock_data.index:
                stock_price = self.stock_data.loc[date]['4. close']  # Adjust based on the column name for closing price
            else:
                stock_price = 'N/A'
            
            buy_ratio = stock_price/800.0
            sell_ratio = buy_ratio * 5
            sign = ''

            if stock_price > ema_value and (stock_price - ema_value) < buy_ratio:
                sign = 'BUY (OVER EMA)'
            elif stock_price > ema_value and (stock_price - ema_value) > sell_ratio:
                sign = 'SELL (OVER EMA)'
            elif stock_price < ema_value and (ema_value - stock_price) < buy_ratio:
                sign = 'SELL (UNDER EMA)'
            elif stock_price < ema_value and (ema_value - stock_price) > sell_ratio:
                sign = 'BUY (UNDER EMA)'
            else:
                sign = 'HOLD'

            #result.append(f"Date: {date}, EMA: {ema_value}, Stock Price: {stock_price}, Sign: {sign}")
            result.append(sign)
        return result
    
    def entry(self):
        ind = ema_indicator('AAPL',10,'60min','close')
        data = ind.position()
        position = False
        sign = ''
        num = 300

        for i in data:
            date = self.ema.index[num]
            ema_value = self.ema_column.iloc[num]
            if date in self.stock_data.index:
                stock_price = self.stock_data.loc[date]['4. close'] 
            else:
                stock_price = 'N/A'

            if (i == 'BUY (UNDER EMA)' or i == 'BUY (OVER EMA)') and position == False:
                position = True
                sign  = 'BOUGHT'
            elif (i == 'SELL (UNDER EMA)' or i == 'SELL (OVER EMA)') and position == True:
                position = False
                sign = 'SOLD'
            else:
                sign = 'HELD'
            num-=1
            print(f"Date: {date}, EMA: {ema_value}, Stock Price: {stock_price}, Sign: {sign}")
            #print(sign)

ind = ema_indicator('AAPL',10,'60min','close')
ind.entry()
