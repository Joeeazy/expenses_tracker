import pandas as panda
import csv
from datetime import datetime
from data_entry import get_description, get_amount, get_category, get_date
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "financial_data.csv"
    COLUMNS = ["date", "AMOUNT", "CATEGORY", "DESCRIPTION"]
    FORMAT = "%d-%m-%Y"

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
           "date": date,
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
        dataframe["date"] = panda.to_datetime(dataframe["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (dataframe["date"] >= start_date) & (dataframe["date"] <= end_date)

        filtered_dataframe = dataframe.loc[mask]

        if filtered_dataframe.empty:
            print("No transactions found were found in the given date range")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")

            print(filtered_dataframe.to_string(index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_dataframe[filtered_dataframe["CATEGORY"] == "Income"]["AMOUNT"].sum()
            total_expenses = filtered_dataframe[filtered_dataframe["CATEGORY"] == "Expense"]["AMOUNT"].sum()
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

def plot_transactions(dataframe):
    dataframe.set_index("date", inplace=True) # index is the way we locate and manipulate different rows
    #two dataframes income dataframe and expenses dataframe
    income_dataframe = (dataframe[dataframe["CATEGORY"] == "Income"].resample("D").sum().reindex(dataframe.index, fill_value=0))
    expenses_dataframe = (dataframe[dataframe["CATEGORY"] == "Expense"].resample("D").sum().reindex(dataframe.index, fill_value=0))

    plt.figure(figsize=(10, 5))
    plt.plot(income_dataframe.index, income_dataframe["AMOUNT"], label="Income", color="g")
    plt.plot(expenses_dataframe.index, expenses_dataframe["AMOUNT"], label="Expenses", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income And Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View Transactions and summary within the date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            dataframe = CSV.get_transactions(start_date, end_date)
            if input("Do You want to see a graph plot? (y/n): ").lower() == "y":
                plot_transactions(dataframe)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid Chice. Enter the 1, 2 or 3")

if __name__ == "__main__":
    main()



#add()
