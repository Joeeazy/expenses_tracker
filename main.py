import pandas as panda
import csv
from datetime import datetime

class CSV:
    CSV_FILE = "financial_data.csv"
    COLUMNS = ["DATE", "AMOUNT", "CATEGORY", "DESCRIPTION"]

    # will have access to the class itself
    @classmethod
    def initialize_csv(cls):
        #try to read the csv file
        try:
            panda.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            # if file is not found create the dataFrame(top columns) below 
            dataframe = panda.DataFrame(columns=cls.COLUMNS)
            # export the dataframe to the cv file
            dataframe.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    #add data to the file
    def add_entries(cls, date, amount, category, description):
        # use csv writer to write dictionaries into the csv file
        new_entry = {
           "DATE": date,
           "AMOUNT": amount,
           "CATEGORY": category,
           "DESCRIPTION": description
        }
        # with keyword(context manager) = automatically closes the file and handles any memory leaks
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            # csv.DictWriter = TAKES A DICT and writes it into a csv file in append mode
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            #adds the new entry
            writer.writerow(new_entry)
        print("Entries added successfully")

CSV.initialize_csv()
CSV.add_entries("15-11-2024", 130.50, "Income", "Salary")