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
        self.filename='Stock_Historical_Data.xlsx'
        self.excel_file=os.path.join(os.getcwd(),'technical_analysis\\',self.filename)
        self.data.to_excel(self.excel_file,sheet_name='Historical Data',engine='openpyxl')
        self.label='RSI_'+str(self.time)
    
        
    def load_data(self):
        print(f'Data exported to {self.excel_file}')
        self.data = pd.read_excel(self.excel_file)
        self.data[self.label]=ta.RSI(self.data[self.series],self.time)
        describe=self.data.describe()
        if describe.iloc[1,7].round()<=30:
            print("Stock is oversold and undervalued! RSI indicates a good time to buy.")
        elif describe.iloc[1,7].round()<70:
            print("Stock is neutral! RSI indicates not a good time to buy or sell.")
        else:
            print("Stock is overbought and overvalued! RSI indicates a good time to sell.")

        
    # def graph(self):
    #     plt.plot(self.data[self.label])
    #     plt.xlabel('Index')
    #     plt.ylabel('RSI Values')
    #     plt.show()

if __name__ in '__main__':
    share=RSI_Indicator('AAPL',5,60,'Close')
    share.load_data()
    