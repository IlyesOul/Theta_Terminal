from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime
import pytz

class macd_indicator:
    def __init__(self, symbol, time_period, interval, series_type):
        # Your Alpha Vantage API Key
        self.Key = 'XGVG6WD2XG2YOLIH'

        # Initialize the TechIndicators object with the API key
        self.techInd = TechIndicators(key=self.Key, output_format='pandas')
        self.timeSeries = TimeSeries(key=self.Key, output_format='pandas')

        # Fetch data for ticker with a specific time period
        self.symbol = symbol
        self.time_period = time_period
        self.interval = interval
        self.series_type = series_type

        # Call get_ema with the correct parameters
        self.ema12, self.meta_data = self.techInd.get_ema(symbol=self.symbol, interval=self.interval, time_period=12, series_type=self.series_type)
        self.ema26, self.meta_data = self.techInd.get_ema(symbol=self.symbol, interval=self.interval, time_period=26, series_type=self.series_type)
        self.ema200, self.meta_data = self.techInd.get_ema(symbol=self.symbol, interval=self.interval, time_period=200, series_type=self.series_type)


        # Fetch the stock price data (intraday with 60min interval in this case)
        self.stock_data, self.stock_meta_data = self.timeSeries.get_intraday(symbol=self.symbol, interval=self.interval, outputsize='full')
        
        # setting the ema and stock price to a lists
        self.ema12_column = self.ema12[f'EMA']
        self.ema26_column = self.ema26[f'EMA']
        self.ema200_column = self.ema200[f'EMA']
        self.stock_price = self.stock_data[f'4. close']


        # calculate the MACD, signal line, and the histogram with the dates
        self.macd_list = []
        self.date_list = []
        min_length = min(len(self.ema12_column), len(self.ema26_column))

        for i in range(min_length-1,-1,-1):
            macd = self.ema12_column.iloc[i] - self.ema26_column.iloc[i]
            self.macd_list.append(macd)
            self.date_list.append(self.ema12.index[i])

        prices = pd.Series(self.macd_list)
        self.signal_line_list = prices.ewm(span=9, adjust=False).mean()
        self.histogram = []

        for i in range(min_length):
            self.histogram.append(self.macd_list[i] - self.signal_line_list.iloc[i])
        
        
    def run(self):
        n = 500

        for i in range(n,-1,-1):
            bullish = False
            bearish = False

            if self.stock_price.iloc[i] >= self.ema200_column.iloc[i]:
                bullish = True
                
            else:
                bearish = True

            print(f"date: {self.date_list[n-i]}, ema12: {self.ema12_column.iloc[i]}, ema26: {self.ema26_column.iloc[i]}, stock price: {self.stock_price.iloc[i]},")

ind = macd_indicator('AAPL', 10, '15min', 'close')
ind.run()
