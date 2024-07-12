# This file handles all functions that handles
#  getting information from the user in the cl

from datetime import datetime

date_format = "%d-%m-%y"

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    # if user doesnt input the date generate date in string format
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    # check for date validity and parse it to the required format
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please Enter the date in dd-mm-yyyy format")
        # recurse for proper date innput
        return get_date(prompt, allow_default=False)


def get_amount():
    try:
        #convert amount into a float number
        amount= float(input("Enter the amount: "))
        # check for amount validity
        if amount <= 0:
            raise ValueError("Amount must be a non-negative or non-zero value")
        return amount
    except ValueError as e:
        print(e)
        # recurse untill correct amount value is gotten
        return get_amount()

def get_category():
    pass

def get_description():
    pass