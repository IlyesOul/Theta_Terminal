from abc import ABC, abstractmethod


class learning_continuous_class(ABC):

    # Constructor that MUST accept stock ticker for query
    @abstractmethod
    def __init__(self, ticker):
        self.ticker = ticker
        pass

    # Method that handles data initialization
    @abstractmethod
    def data_conversion(self):
        pass

    # Function to handle the visualization of predictions
    @ abstractmethod
    def visualization(self):
        pass

    # Function to train the model on data and optimize its hyperparameters
    @abstractmethod
    def training_optimization(self):
        pass

    # Function to evaluate and test the model
    @abstractmethod
    def testing(self):
        pass

    # Function to assess the given company
    @abstractmethod
    def assess(self):
        pass
