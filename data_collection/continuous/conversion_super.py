from abc import ABC, abstractmethod


# Define abstract class "processor"
class processor(ABC):

    # Function that initializes API call url
    @ abstractmethod
    def initialize_url(self):
        pass

    # Function that executes API call and writes data to JSON file
    @ abstractmethod
    def attain_data(self, file="data.json"):
        pass

    # Function that writes API JSON response to CSV file
    @ abstractmethod
    def convert_data(self, csv="data.csv"):
        pass

    # Function that prompts user for window
    @abstractmethod
    def prompt_date(self):
        pass

    # Function that obtains dates in range
    @abstractmethod
    def get_valid_dates(self):
        pass