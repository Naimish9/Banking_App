import mysql.connector
import random
import decimal


def show_options(user):
    print("\nOptions:")
    print("1. Display Account Information")
    print("2. Add funds")
    print("3. Add Beneficiary")
    print("4. Beneficiaries List")
    print("5. Add Card")
    print("6. List of Cards")
    print("7. Transfer Funds")
    print("8. View Transactions")
    print("9. Change PIN")
    print("10. Update Information")
    print("0. Exit")

    choice = input("Enter your choice: ")
    if choice == '1':
        show_account_info(user)
    elif choice == '2':
        initiate_deposit(user)
    elif choice == '3':
        add_beneficiary(user)
    elif choice == '4':
        list_beneficiaries(user)
    elif choice == '5':
        add_card(user)
    elif choice == '6':
        list_cards(user)
    elif choice == '7':
        transfer_funds(user)
    elif choice == '8':
        view_transactions(user)
    elif choice == '9':
        change_pin(user)
    elif choice == '10':
        update_info(user)
    elif choice == '0':
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")
        show_options(user)


#1. Display Account Information
def show_account_info(user):
    print("Account Information:")
    print("Account Number:", user[0])
    print("Balance:", user[-1])

    show_options(user)

    if user[-1] == 0:
        print("It looks like your account balance is 0. Would you like to make an initial deposit? (yes/no)")
        decision = input().lower()
        if decision == 'yes':
            initiate_deposit(user)
            print("Transection Successfull!")
            show_options(user)
        else:
            show_options(user)


# 2. Add funds
def initiate_deposit(user):
    deposit_amount = int(input("Enter deposit amount: "))
    if deposit_amount < 1:
        print("Deposit a valid amount(>0)")
        return

    balance_add(deposit_amount, user[0], user)


#3. Add Beneficiaries
def add_beneficiary(user):
    # global connection, cursor
    print("Add Beneficiary Details:")
    while True:
        #username = user[1]
        benef_name = input("Enter beneficiary name: ")
        benef_account_number = int(input("Enter beneficiary account number: "))
        benef_ifsc = input("Enter beneficiary IFSC Code: ")

        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123",
                                                 database="Bank_Sch")

            cursor = connection.cursor()

            # Check if the beneficiary account number and name match in the users table
            cursor.execute("SELECT * FROM acc_info WHERE acc_no = %s AND user_name = %s",
                           (benef_account_number, benef_name))
            beneficiary_data = cursor.fetchone()
            if beneficiary_data is None:
                print("Beneficiary account number does not match the provided name.")
                retry = input("Do you want to retry? (yes/no): ").lower()
                if retry != 'yes':
                    break
                continue

            # Check if the benef_ifsc exists in the Benf table
            cursor.execute("SELECT * FROM BankIFSC WHERE IFSC_Code = %s", (benef_ifsc,))
            if not cursor.fetchone():
                print("Beneficiary IFSC Code does not exist in the database.")
                retry = input("Do you want to retry? (yes/no): ").lower()
                if retry != 'yes':
                    break
                continue

            # Insert the beneficiary into the beneficiaries table
            sql = "INSERT INTO Benf (user_name, benf_name, benf_acc_no, Benf_ifsc) VALUES (%s, %s, %s, %s)"
            val = (user[1], benef_name, benef_account_number, benef_ifsc)
            cursor.execute(sql, val)
            connection.commit()
            print("Beneficiary added successfully!")
            break

        except mysql.connector.Error as error:
            print("Error while adding beneficiary:", error)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    list_beneficiaries(user)


#4. Print Beneficiaries List
def list_beneficiaries(user):
    print("List of Beneficiaries:")
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123", database="Bank_Sch")

        cursor = connection.cursor()

        sql = "SELECT * FROM Benf WHERE user_name = %s"
        cursor.execute(sql, (user[1],))
        beneficiaries = cursor.fetchall()

        if beneficiaries:
            for beneficiary in beneficiaries:
                print(
                    f"Beneficiary Name: {beneficiary[1]}, Account Number: {beneficiary[2]}, IFSC Code: {beneficiary[3]}")
        else:
            print("No beneficiaries found.")

    except mysql.connector.Error as error:
        print("Error while fetching beneficiaries:", error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    show_options(user)


# 5. Add Card
def add_card(user):
    while True:
        card_type = input("Choose the card type, Debit or Credit: ")
        temp_num = ''.join(random.choices('0123456789', k=12))
        if card_type.lower() == "debit":
            card_numb = '4126' + temp_num
        elif card_type.lower() == "credit":
            card_numb = '4141' + temp_num
        pin = ''.join(random.choices('0123456789', k=4))
        cvv = ''.join(random.choices('0123456789', k=3))

        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123",
                                                 database="Bank_Sch")

            cursor = connection.cursor()

            # Insert the beneficiary into the beneficiaries table
            sql = "INSERT INTO card (card_no, card_type, cvv, pin, user_name) VALUES (%s, %s, %s, %s, %s)"
            val = (card_numb, card_type, cvv, pin, user[1])
            cursor.execute(sql, val)
            connection.commit()
            print(f"{card_type.upper()} added successfully!")

        except mysql.connector.Error as error:
            print("Error while adding card:", error)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        list_cards(user)


#6. Show Cards
def list_cards(user):
    print("List of Cards:")
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123", database="Bank_Sch")

        cursor = connection.cursor()

        sql = "SELECT * FROM card WHERE user_name = %s"
        cursor.execute(sql, (user[1],))
        cards = cursor.fetchall()

        if cards:
            for card in cards:
                print(f"Card Number: {card[1]}, Card Type: {card[2]}, CVV: {card[4]}, PIN: {card[3]}")
        else:
            print("No cards found.")

    except mysql.connector.Error as error:
        print("Error while fetching cards:", error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    show_options(user)


# 7. Transfer Funds
def transfer_funds(user):
    beneficiary_number = input("Enter beneficiary account number: ")

    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123", database="Bank_Sch")
        cursor = connection.cursor()

        # Check if the beneficiary account exists in the Beneficiaries table
        query = "SELECT * FROM Benf WHERE user_name = %s AND benf_acc_no = %s"
        cursor.execute(query, (user[1], beneficiary_number))
        beneficiary = cursor.fetchone()
        if not beneficiary:
            print("Beneficiary account not found. Please add the beneficiary first.")
            show_options(user)
            return

        amount = decimal.Decimal(input("Enter amount to transfer: "))
        if amount <= 0:
            print("Invalid amount. Please enter a positive value.")
            return

            # Check if the user has sufficient balance
        query = "SELECT acc_balance FROM acc_info WHERE user_name = %s"
        cursor.execute(query, (user[1],))
        sender_balance = cursor.fetchone()[0]
        if sender_balance < amount:
            print("Insufficient balance. Transaction aborted.")
            return

        # Consume any unread results before executing the update query
        cursor.fetchall()

        # Deduct the transferred amount from the sender's account balance
        new_sender_balance = sender_balance - amount
        update_sender_query = "UPDATE acc_info SET acc_balance = %s WHERE user_name = %s"
        cursor.execute(update_sender_query, (new_sender_balance, user[1]))
        connection.commit()  # Consume the result

        # Add the transferred amount to the beneficiary's account balance
        update_beneficiary_query = "UPDATE acc_info SET acc_balance = acc_balance + %s WHERE user_name = %s"
        cursor.execute(update_beneficiary_query, (amount, beneficiary[0]))

        # Insert transaction record
        insert_transaction_query = "INSERT INTO transaction (sender_acc_no, benf_acc_no, amount) VALUES (%s, %s, %s)"
        cursor.execute(insert_transaction_query, (user[0], beneficiary[2], amount))

        connection.commit()
        print("Funds transferred successfully.")

    except mysql.connector.Error as error:
        print("Error while Updating transaction:", error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    show_options(user)


# 8. View Transaction
def view_transactions(user):
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123", database="Bank_Sch")
        cursor = connection.cursor()
        # SQL query to fetch transaction details along with sender and beneficiary names for a specific user
        query = """
        SELECT t.idtransaction, u.user_name AS sender_name, b.benf_name,
              t.amount, t.tr_timestamp
        FROM transaction t
        INNER JOIN acc_info u ON t.sender_acc_no = u.acc_no
        INNER JOIN Benf b ON t.benf_acc_no = b.benf_acc_no
        WHERE t.sender_acc_no = %s OR t.benf_acc_no = %s
        """

        # Execute the query with user_id as parameter
        cursor.execute(query, (user[0], user[0]))

        # Fetch all rows
        transactions = cursor.fetchall()

        # Check if transactions are not found
        if not transactions:
            print("No transactions found.")
        else:
            # Print column headers
            print("{:<15} {:<20} {:<20} {:<10} {:<25}".format(
                "Transaction ID", "Sender Name", "Beneficiary Name", "Amount", "Transaction Date"))
            print("=" * 90)

            # Print each transaction
            for transaction in transactions:
                # Determine if the user is the sender or beneficiary
                if transaction[1] == user[0]:  # User is the sender
                    user_role = "Sender"
                else:  # User is the beneficiary
                    user_role = "Beneficiary"

                # Format the transaction date
                transaction_date = transaction[4].strftime("%Y-%m-%d %H:%M:%S")

                print("{:<15} {:<20} {:<20} {:<10} {:<25}".format(
                    transaction[0], transaction[1], transaction[2], transaction[3], transaction_date))


    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    show_options(user)


# 9. Change Pin
def change_pin(user):
    card_number = int(input("Enter card number: "))

    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123", database="Bank_Sch")
        cursor = connection.cursor()

        # Check if the card exists in the database
        query = "SELECT * FROM card WHERE card_no = %s"
        cursor.execute(query, (card_number,))
        card = cursor.fetchone()

        if not card:
            print("Card not found. Please enter valid card details.")
            return
            show_options(user)
        else:
            old_pin = int(card[3])
            print('Old pin is: ', old_pin)

        while True:
            new_pin = input("Enter new PIN: ")
            if len(new_pin) != 4:
                print("Please enter 4 digit PIN.")
                continue

            if old_pin == new_pin:
                print("Entered Old PIN. Please enter new PIN.")

            if not new_pin.isdigit():
                print("Invalid PIN. Please enter only digits.")
                continue
            break

            # Ensure PIN consists of only digits
            if not new_pin.isdigit():
                print("Invalid PIN. Please enter only digits.")
                continue
            break

        # Update the PIN
        query = "UPDATE card SET pin = %s WHERE card_no = %s"
        data = (new_pin, card_number)
        cursor.execute(query, data)
        connection.commit()
        print("PIN changed successfully.")

    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    show_options(user)


#10. Update Information
def update_info(user):
    print(f"Update Account Information of {user[0]}:")
    new_address = input("Enter new address: ")

    # Loop until a valid mobile number is entered
    while True:
        new_mobile = input("Enter new mobile number: ")
        if len(new_mobile) == 10 and new_mobile.isdigit() and new_mobile[0] in ['6', '7', '8', '9']:
            break
        else:
            print("Invalid mobile number. Mobile number must be 10 digits starting with 7, 8, or 9.")

    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123", database="Bank_Sch")
        cursor = connection.cursor()

        # Update the address and mobile number in the database
        cursor.execute("UPDATE acc_info SET address = %s, mobile_no = %s WHERE user_name = %s",
                       (new_address, new_mobile, user[1]))
        connection.commit()
        print("Account information updated successfully!")

        # user[2] = new_address
        # user[4] = new_mobile

    except mysql.connector.Error as error:
        print("Error while updating account information:", error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    show_options(user)


#DB Connection:
#Connection to load data:
def sql_connect_load(sql_query, values=None):
    # global connection, cursor
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123", database="Bank_Sch")

        cursor = connection.cursor()

        if values is not None:
            cursor.execute(sql_query, values)
        else:
            cursor.execute(sql_query)

        connection.commit()
        print("Query executed successfully!")

    except mysql.connector.Error as error:
        print("Error while executing SQL query:", error)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


#Connection to fetch data:
def fetch_data(sql_query, values=None):
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123", database="Bank_Sch")

        cursor = connection.cursor()

        if values is not None:
            cursor.execute(sql_query, values)
        else:
            cursor.execute(sql_query)

        #For fetching the data
        data = cursor.fetchone()
        return data

    except mysql.connector.Error as error:
        print("Error while executing SQL query:", error)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


#Connection to add balance:
def balance_add(deposit_amount, acc_no, user):
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123", database="Bank_Sch")

        cursor = connection.cursor()

        # Update the user's balance in the database
        cursor.execute("UPDATE acc_info SET acc_balance = acc_balance + %s WHERE acc_no = %s", (deposit_amount, acc_no))
        connection.commit()

        # Fetch and print the updated balance
        cursor.execute("SELECT acc_balance FROM acc_info WHERE acc_no = %s", (acc_no,))
        updated_balance = cursor.fetchone()[0]
        print(f"Your account has been credited with {deposit_amount}. New balance is {updated_balance}.")


    except mysql.connector.Error as error:
        print("Error while executing SQL query:", error)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            show_options(user)
