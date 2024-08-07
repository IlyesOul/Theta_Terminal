from data_collection.continuous import simple_time_series
import learning_interface

class rfe_simple(learning_interface):

    def __init__(self, ticker):
        self.ticker = ticker

# Allahukbar