import requests
import json
import csv
import datetime
from data_collection.continuous import conversion_super


class time_series_converter(conversion_super.processor):

    # Initializes converter object and fields
    def __init__(self, default=True):
        if default:
            self.url = self.initialize_url()
        else:
            self.url = self.initialize_url(False, False)
        r = requests.get(self.url, headers={'User-agent': 'Mozilla/5.0'})
        self.r_json = r.json()
        print(self.url)
        self.ticker = self.r_json.get("chart").get("result")[0].get("meta").get("symbol")

    # Writing live data to JSON file
    def attain_data(self, file="data.json"):
        # Writing to JSON file
        ticker = "" + self.ticker
        with open(file, "w") as outfile:
            json.dump(self.r_json, outfile)

        with open(file, encoding='utf-8') as f:
            data = json.loads(f.read())

    # Converting JSON data to CSV
    def convert_data(self, csv_file="data.csv"):
        ticker = ""+self.ticker

        # Converting to CSV dataframe and writing
        header = ["Ticker", "Low", "Close", "High", "Open", "Volume", "Timestamp"]
        all_results = self.r_json.get("chart").get("result")[0].get("indicators").get("quote")[0]

        full_values = {"low": [],
                       "close": [],
                       "high": [],
                       "open": [],
                       "volume": [],
                       "timestamps": []}

        # Retrieving timestamps
        for item in self.r_json.get("chart").get("result")[0].get("timestamp"):
            full_values["timestamps"].append(item)

        # Filling the full_values dictionary with appropriate values
        for index in range(len(all_results.get("low"))):
            for curr_row in all_results:
                if curr_row != "timestamps":
                    full_values[curr_row].append(all_results.get(curr_row)[index])
            index += 1

        # Initializing and filling final 2d-array to write to file
        final_arr = []

        for index in range(len(full_values.get("volume"))):
            list_to_add = [ticker]
            for attribute in full_values:
                list_to_add.append(round(full_values.get(attribute)[index], 2))
            final_arr.append(list_to_add)

        # Writing final values to CSV file
        with open(csv_file, 'w') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(header)
            for index in range(len(final_arr)):
                csvwriter.writerow(final_arr[index])

    # Returns list of values of specified feature
    def get_feature_values(self, feature):
        # All JSON results
        all_results = self.r_json.get("chart").get("result")[0].get("indicators").get("quote")[0]

        # Values of specified values
        final_values = []
        for index in range(len(all_results.get("low"))):
            for curr_row in all_results:
                if curr_row == feature:
                    final_values.append(all_results.get(curr_row)[index])
        return final_values

    # Returns valid window ranges
    def get_valid_dates(self):
        dates = []

        for unix in self.r_json['chart']['result'][0]['timestamp']:
            date = datetime.datetime.fromtimestamp(unix)
            dates.append(date)

        return dates

    # Initializes query URL
    def initialize_url(self, name=True, day1=True, month1=True,year1=2022,day2=True, month2=True,year2=2022):
        if not name:
            name = input("What is the name of your stock? ")
        if not day1:
            print("This is the starting interval: ")
            self.prompt_date()
            unix_1 = self.to_unix()
            print("This is the ending interval: ")
            self.prompt_date()
            unix_2 = self.to_unix()

            url = f'https://query1.finance.yahoo.com/v8/finance/chart/msft?period1={unix_1}&period2={unix_2}&interval=1d&includeAdjustedClose=false'
        else:
            url = f'https://query1.finance.yahoo.com/v8/finance/chart/msft?period1={str(int(datetime.datetime.timestamp(datetime.datetime(2022,1,1))))}&period2={str(int(datetime.datetime.timestamp(datetime.datetime(2024,8,1))))}&interval=1d&includeAdjustedClose=false'
        return url

    # Prompts user for date-values
    def prompt_date(self):
        self.day = int(input("What is the day? (Start with 0 if single-digit) "))
        self.month = int(input("What is the month? (Start with 0 if single-digit) "))
        self.year = int(input("What is the year? "))

    # Returns unix_formatted date
    def to_unix(self):
        date2 = datetime.datetime(self.year, self.month, self.day)
        unix_timestamp = datetime.datetime.timestamp(date2)
        return str(int(unix_timestamp))

    # Returns valid window ranges
    def get_valid_dates(self):
        dates = []

        for unix in self.r_json['chart']['result'][0]['timestamp']:
            date = datetime.datetime.fromtimestamp(unix)
            dates.append(date)

        return dates