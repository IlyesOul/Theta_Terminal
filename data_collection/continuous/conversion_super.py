from abc import ABC, abstractmethod


# Define abstract class "processor"
class processor(ABC):

    # Function that initializes API call url
    @ abstractmethod
    def initialize_url(self):
        pass

    # Function that executes API call and writes data to JSON file
    @ abstractmethod
    def attain_data(self, url, file="data.json"):
        pass

    # Function that writes API JSON response to CSV file
    @ abstractmethod
    def convert_data(self, json="data.json", csv="data.csv"):
        pass
