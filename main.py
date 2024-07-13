import pandas as panda
import csv
from datetime import datetime
from data_entry import get_description, get_amount, get_category, get_date

class CSV:
    CSV_FILE = "financial_data.csv"
    COLUMNS = ["DATE", "AMOUNT", "CATEGORY", "DESCRIPTION"]
    FORMAT = "%d-%m-%y"

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

    @classmethod
    def get_transactions(cls, start_date, end_date):
        dataframe = panda.read_csv(cls.CSV_FILE)
        # convert date to date column object
        dataframe["DATE"] = panda.to_datetime(dataframe["DATE"], format=CSV.FORMAT)
        start_date=datetime.strptime(start_date, CSV.FORMAT)
        end_date=datetime.strptime(end_date, CSV.FORMAT)

        mask = (dataframe["DATE"] >= start_date) & (dataframe["DATE"] <= end_date)

        filtered_dataframe = dataframe.loc[mask]

        if filtered_dataframe.empty:
            print("No transactions found were found in the given date range")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")

            print(filtered_dataframe.to_string(index=False, formatters={"DATE": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_dataframe[filtered_dataframe["CATEGORY"] == "Income"]["AMOUNT"].sum()
            total_expenses = filtered_dataframe[filtered_dataframe["CATEGORY"] == "Expenses"]["AMOUNT"].sum()
            print("\nSummary")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expenses: ${total_expenses:.2f}")

        return filtered_dataframe

# function to call get_entries in order for data collection
def add():
    CSV.initialize_csv()
    date = get_date("Enter date of transaction or today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.add_entries(date, amount, category, description)

#add()
CSV.get_transactions("01-01-2023", "30-12-2024")