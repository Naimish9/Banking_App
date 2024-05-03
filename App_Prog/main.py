from options import sql_connect
from register_user import *


def main():
    connect = sql_connect()
    if connect:
        cursor = connect.cursor()
        while True:
            print("Welcome to ACN NetBanking:")

            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Choose an option from above to proceed: ")

            if choice == '1' or choice.lower() == 'register':
                register_user(cursor, connect)
            elif choice == '2' or choice.lower() == 'login':
                login_user(cursor, connect)
            elif choice == '3' or choice.lower() == 'exit':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        cursor.close()
        connect.close()


if __name__ == "__main__":
    main()


# Store user data in MySQL
# store_in_mysql(user, password)
# details_into_db(user_name, address, aadhar, mobile_no, password, account_number)

def details_into_db(cursor, connect, acc_no, user_name, address, aadhar, mobile_no, acc_pwd):
    try:
        sql_query = ("INSERT INTO acc_info (acc_no, user_name, address, aadhar_no, mobile_no, acc_pwd, acc_balance) "
                     "VALUES"
                     "(%s, %s, %s, %s, %s, %s, %s)")
        values = (acc_no, user_name, address, int(aadhar), int(mobile_no), acc_pwd, 0.0)
        cursor.execute(sql_query, values)
        connect.commit()
    except Exception as e:
        print("An error occurred:", e)
