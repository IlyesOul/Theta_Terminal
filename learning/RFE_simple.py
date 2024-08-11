from data_collection.continuous import simple_time_series
import learning_interface
from sklearn.ensemble import GradientBoostingRegressor
import matplotlib


class rfe_simple(learning_interface):

    def __init__(self, ticker):
        self.ticker = ticker

    # Function that handles data initialization in 'data.csv'
    def data_conversion(self):
        converter = simple_time_series.time_series_converter()
        converter.attain_data('data.json')
        converter.convert_data('data.csv')


    def training_optimization(self):

        ensemble = GradientBoostingRegressor()