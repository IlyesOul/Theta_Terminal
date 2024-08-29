from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from datetime import datetime
import pytz

# Your Alpha Vantage API Key
Key = 'I9FDJSQIMYT4TXDX'

# Initialize the TechIndicators object with the API key
techInd = TechIndicators(key=Key, output_format='pandas')
timeSeries = TimeSeries(key=Key, output_format='pandas')

# Fetch EMA data for AAPL with a specific time period
symbol = 'AAPL'
time_period = 10
interval = '5min'
series_type = 'open'

# Call get_ema with the correct parameters
bband, meta_data = techInd.get_bbands(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type)

# Fetch the stock price data (intraday with 60min interval in this case)
stock_data, stock_meta_data = timeSeries.get_intraday(symbol=symbol, interval=interval, outputsize='full')
#print(stock_data.head())

print(bband)
print(stock_data)