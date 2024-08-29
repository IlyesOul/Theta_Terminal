import pandas as pd
import yfinance as yf
import openpyxl
import talib as ta
import os
import numpy as np
import matplotlib.pyplot as plt

class RSI():
    self.ticker_symbol='AAPL'
    data=yf.download(ticker_symbol,start='2022-01-01',end='2023-01-01')
    excel_file='C:\\Users\\tmghi\\Theta_Terminal\\technical_analysis\\Stock_Historical_Data.xlsx'
    data.to_excel(excel_file,sheet_name='Historical Data',engine='openpyxl')
    print(f'Data exported to {excel_file}')
    df = pd.read_excel(excel_file)
    print()
    # Save to CSV
    df['RSI_14']=ta.RSI(df['Close'],14)
    plt.plot(df['RSI_14'])
    plt.xlabel('Date')
    plt.ylabel('RSI Values')
    plt.show()

if __name__ in __main__:
    