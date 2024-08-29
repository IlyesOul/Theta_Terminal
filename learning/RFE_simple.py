from data_collection.continuous import simple_time_series
from learning_interface import learning_continuous_class
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import RandomizedSearchCV
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np


class rfe_simple(learning_continuous_class):

    def __init__(self, ticker):
        """
        Initializes a new instance of the rfe_simple class.

        Args:
            ticker (str): The ticker symbol for the stock.

        """
        self.predicted_values = None
        self.ticker = ticker
        self.x = None
        self.y = None
        self.converter = None

    # Function that handles data initialization in 'data.csv'
    def data_conversion(self):
        """
        Converts data from 'data.json' to 'data.csv' and splits it into X and Y data.


        Returns:
            x (pandas.DataFrame): The input features for the stock.
            y (pandas.Series): The target values for the stock.
        """
        self.converter = simple_time_series.time_series_converter()
        self.converter.attain_data('data.json')
        self.converter.convert_data('data.csv')

        # Split X and Y data
        data = pd.read_csv('data.csv')

        x = data.drop(["Open"], axis=1)
        x = data.drop(["Ticker"], axis=1)
        y = pd.read_csv('data.csv')["Open"]

        # Scale X and Y accordingly
        scalar = MinMaxScaler()
        self.x = scalar.fit_transform(x)
        self.y = y

        return x, y

    # Function that will return a reference to an optimized GBR
    def training_optimization(self):
        """
        Trains a Gradient Boosting Regressor on scaled data using a randomized search
        over specified hyperparameters.

        Returns:
            GradientBoostingRegressor: The best estimator found by the randomized search.
        """

        # Define ensemble and train on scaled data
        ensemble = GradientBoostingRegressor()
        scalar = MinMaxScaler()

        x_train = scalar.fit_transform(self.x[:int(len(self.x)*(2/3))])

        searchcv = RandomizedSearchCV(ensemble, {
            "learning_rate": [.1, 1, 1.5, 5],
            "n_estimators": [25, 50, 75, 100, 150],
            "max_depth": [15, 35, 50, 75],
            "max_leaf_nodes": [5,12,18,25,40]
        })

        searchcv.fit(X=x_train, y=self.y[:int(len(self.y) * (2 / 3))].values)

        return searchcv.best_estimator_

    # Function to evaluate optimized GBR performance
    def evaluation(self):
        """
        Evaluates the performance of the trained Gradient Boosting Regressor (GBR) on the testing data.

        Returns:
            tuple: A tuple containing the score of the GBR on the testing data and the mean absolute error between the predicted values and the actual values.

        Raises:
            None
        """

        # Initialize GBR and data
        gbr = self.training_optimization()
        scalar = MinMaxScaler()
        x_test_scaled = scalar.fit_transform(self.x[int(len(self.x)*(2/3)):])

        # Evaluation stats on testing data
        self.predicted_values = gbr.predict(x_test_scaled)
        print(self.predicted_values[:10])
        print(self.y[int(len(self.y)*(2/3)):int(len(self.y)*(2/3))+10])
        return gbr.score(x_test_scaled, self.y[int(len(self.y)*(2/3)):]), mean_absolute_error(self.predicted_values, self.y[int(len(self.y)*(2/3)):])

    # Function to visualize given predictions
    def visualization(self):
        """
        Visualizes the predicted values and the real values.

        This function plots the predicted values and the real values on a graph. The predicted values are plotted against the dates obtained from the `converter.get_valid_dates()` method, starting from the 2/3rd position. The real values are plotted against the same dates. The graph is titled "Real Opening Prices vs Predicted Prices" and has a legend displaying the labels "Predictions" and "Real Values". The graph is displayed using `plt.show()`.

        Parameters:
            None

        Returns:
            None
        """

        # Attain predictions and real values
        predictions = self.predicted_values
        real_values = self.y

        # Obtain valid dates
        dates = self.converter.get_valid_dates()

        # Plot predictions and real values
        plt.plot(dates[int(len(dates)*(2/3)):], np.add(predictions, 100), label="Predictions", c='blue')
        plt.plot(dates, real_values, label="Real Values", c='red')
        plt.title("Real Opening Prices vs Predicted Prices")
        plt.legend()
        plt.show()

    # Assessment function
    def assess(self):
        """
        Assess the object's state and return a score or evaluation metric.

        This method does not take any parameters and does not return anything. It is intended to be overridden by subclasses to provide specific assessment functionality.

        Returns:
            None
        """
        pass

# Testing
if __name__ == "__main__":
    test = rfe_simple("MFST")
    test.data_conversion()
    test.training_optimization()
    score, mae = test.evaluation()
    print(f"MAE: {mae}; SCORE: {score}")
    test.visualization()
