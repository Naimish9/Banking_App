from options import sql_connect_load
from register_user import *

'''
#to clear screen
#import os
#to cell in notebook
#from IPython.display import clear_output
#import datetime
#import getpass
#import pandas as pd
'''


def main():
    while True:
        print("Welcome to ACN NetBanking:")

        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option from above to proceed: ")

        if choice == '1' or choice.lower() == 'register':
            register_user()
        elif choice == '2' or choice.lower() == 'login':
            login_user()
        elif choice == '3' or choice.lower() == 'exit':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


# Store user data in MySQL
# store_in_mysql(user, password)
# details_into_db(user_name, address, aadhar, mobile_no, password, account_number)

def details_into_db(acc_no, user_name, address, aadhar, mobile_no, acc_pwd):
    sql_query = ("INSERT INTO acc_info (acc_no, user_name, address, aadhar_no, mobile_no, acc_pwd, acc_balance) VALUES "
                 "(%s, %s, %s, %s, %s, %s, %s)")
    values = (acc_no, user_name, address, int(aadhar), int(mobile_no), acc_pwd, 0.0)
    sql_connect_load(sql_query, values)
