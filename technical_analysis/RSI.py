import pandas as pd
import yfinance as yf
import openpyxl
import talib as ta
import os
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

class RSI_Indicator():
    def __init__(self,symbol,time_period, interval, series_type):
        self.ticker_symbol=symbol
        self.time=time_period
        self.inter=interval
        self.series=series_type
        self.data=yf.download(self.ticker_symbol,start='2023-01-01',end='2024-01-01')
        self.excel_file='C:\\Users\\tmghi\\Theta_Terminal\\technical_analysis\\Stock_Historical_Data.xlsx'
        self.data.to_excel(self.excel_file,sheet_name='Historical Data',engine='openpyxl')
        self.label='RSI_'+str(self.time)
    
        
    def load_data(self):
        print(f'Data exported to {self.excel_file}')
        self.data = pd.read_excel(self.excel_file)
        self.data[self.label]=ta.RSI(self.data[self.series],self.time)
        print(self.data)
        self.graph()
        
    def graph(self):
        plt.plot(self.data[self.label])
        plt.xlabel('Index')
        plt.ylabel('RSI Values')
        plt.show()

if __name__ in '__main__':
    share=RSI_Indicator('AAPL',5,60,'Close')
    share.load_data()
    