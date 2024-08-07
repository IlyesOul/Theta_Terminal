import matplotlib.pyplot as mlp
from data_collection.continuous import simple_time_series
import pandas as pd

# Import conversion file & prepare data (functional)
conversion = simple_time_series.time_series_converter()
conversion.attain_data()
conversion.convert_data()

data = pd.read_csv("data.csv")
print(data.head(32))
