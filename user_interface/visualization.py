import matplotlib.pyplot as plt
from data_collection.continuous import simple_time_series
import pandas as pd
import datetime
import numpy as np

# Import conversion file & prepare data (functional)
conversion = simple_time_series.time_series_converter()
conversion.attain_data()
conversion.convert_data()

# Attain plotting data
data = pd.read_csv('data.csv')
prices = data["Open"]
dates = data["Timestamp"]

for i in range(len(data)):
    dates[i] = datetime.datetime.fromtimestamp(dates[i])

plt.plot(dates, prices, c='red')
plt.title("Daily Opening MSFT Prices 1/1/2022-8/1/2024")

plt.xlabel("Dates")
plt.ylabel("Price")
plt.show()
