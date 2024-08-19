from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import pandas as pd


# Your Alpha Vantage API Key
Key = '1WCNX62EOULHYZUW'

# Initialize the TechIndicators object with the API key
techInd = TechIndicators(key=Key, output_format='pandas')
timeSeries = TimeSeries(key=Key, output_format='pandas')
# Fetch EMA data for AAPL with a specific time period
symbol = 'AAPL'
time_period = 10
interval = '60min'
series_type = 'close'

# Call get_ema with the correct parameters
ema, meta_data = techInd.get_ema(symbol=symbol, interval=interval, time_period=time_period, series_type=series_type)

# Fetch the stock price data (intraday with 60min interval in this case)
stock_data, stock_meta_data = timeSeries.get_intraday(symbol=symbol, interval=interval, outputsize='full')
#print(stock_data.head())

# Assuming the EMA column is named 'EMA', adjust if necessary
ema_column = ema[f'EMA']


for i in range(300,-1,-1):
    #print(ema_column.iloc[i])
    date = ema.index[i]
    ema_value = ema_column.iloc[i]

    if date in stock_data.index:
        stock_price = stock_data.loc[date]['4. close']  # Adjust based on the column name for closing price
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

    print(f"Date: {date}, EMA: {ema_value}, Stock Price: {stock_price}, Sign: {sign}")
    


