import mysql.connector
import random
import decimal


def show_options(cursor, connect, user):
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
        show_account_info(cursor, connect, user)
    elif choice == '2':
        initiate_deposit(cursor, connect, user)
    elif choice == '3':
        add_beneficiary(cursor, connect, user)
    elif choice == '4':
        list_beneficiaries(cursor, connect, user)
    elif choice == '5':
        add_card(cursor, connect, user)
    elif choice == '6':
        list_cards(cursor, connect, user)
    elif choice == '7':
        transfer_funds(cursor, connect, user)
    elif choice == '8':
        view_transactions(cursor, connect, user)
    elif choice == '9':
        change_pin(cursor, connect, user)
    elif choice == '10':
        update_info(cursor, connect, user)
    elif choice == '0':
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")
        show_options(cursor, connect, user)


#1. Display Account Information
def show_account_info(cursor, connect, user):
    query = "SELECT * FROM acc_info WHERE user_name = %s"
    cursor.execute(query, (user[1],))
    users = cursor.fetchone()
    print("Account Information:")
    print("Account Number:", users[0])
    print("Balance:", users[-1])

    if user[-1] == 0:
        print("It looks like your account balance is 0. Would you like to make an initial deposit? (yes/no)")
        decision = input().lower()
        if decision == 'yes':
            initiate_deposit(cursor, connect, user)
            print("Transection Successfull!")
            show_options(cursor, connect, user)
        else:
            show_options(cursor, connect, user)

    show_options(cursor, connect, user)

# 2. Add funds
def initiate_deposit(cursor, connect, user):
    deposit_amount = int(input("Enter deposit amount: "))
    if deposit_amount < 1:
        print("Deposit a valid amount(>0)")
        # show_options(cursor, connect, user)
        initiate_deposit(cursor, connect, user)

    balance_add(cursor, connect, user, deposit_amount, user[0])


#3. Add Beneficiaries
def add_beneficiary(cursor, connect, user):
    print("Add Beneficiary Details:")
    while True:
        #username = user[1]
        benef_name = input("Enter beneficiary name: ")
        benef_account_number = int(input("Enter beneficiary account number: "))
        benef_ifsc = input("Enter beneficiary IFSC Code: ")

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
        connect.commit()
        print("Beneficiary added successfully!")
        break

    list_beneficiaries(cursor, connect, user)


#4. Print Beneficiaries List
def list_beneficiaries(cursor, connect, user):
    print("List of Beneficiaries:")

    sql = "SELECT * FROM Benf WHERE user_name = %s"
    cursor.execute(sql, (user[1],))
    beneficiaries = cursor.fetchall()

    if beneficiaries:
        for beneficiary in beneficiaries:
            print(
                f"Beneficiary Name: {beneficiary[1]}, Account Number: {beneficiary[2]}, IFSC Code: {beneficiary[3]}")
    else:
        print("No beneficiaries found.")

    show_options(cursor, connect, user)


# 5. Add Card
def add_card(cursor, connect, user):
    while True:
        card_type = input("Choose the card type, Debit or Credit: ")
        temp_num = ''.join(random.choices('0123456789', k=12))
        if card_type.lower() == "debit":
            card_numb = '4126' + temp_num
        elif card_type.lower() == "credit":
            card_numb = '4141' + temp_num
        pin = ''.join(random.choices('0123456789', k=4))
        cvv = ''.join(random.choices('0123456789', k=3))

        sql = "INSERT INTO card (card_no, card_type, cvv, pin, user_name) VALUES (%s, %s, %s, %s, %s)"
        val = (card_numb, card_type, cvv, pin, user[1])
        cursor.execute(sql, val)
        connect.commit()
        print(f"{card_type.upper()} added successfully!")

        list_cards(cursor, connect, user)


#6. Show Cards
def list_cards(cursor, connect, user):
    print("List of Cards:")

    sql = "SELECT * FROM card WHERE user_name = %s"
    cursor.execute(sql, (user[1],))
    cards = cursor.fetchall()

    if cards:
        for card in cards:
            masked_card_number = str(card[1])[:4] + "*" * (len(str(card[1])) - 8) + str(card[1])[-4:]
            print(f"Card Number: {masked_card_number}, Card Type: {card[2]}")
    else:
        print("No cards found.")

    show_options(cursor, connect, user)


# 7. Transfer Funds
def transfer_funds(cursor, connect, user):
    beneficiary_number = input("Enter beneficiary account number: ")

    query = "SELECT * FROM Benf WHERE user_name = %s AND benf_acc_no = %s"
    cursor.execute(query, (user[1], beneficiary_number))
    beneficiary = cursor.fetchone()
    if not beneficiary:
        print("Beneficiary account not found. Please add the beneficiary first.")
        show_options(cursor, connect, user)
        return

    amount = decimal.Decimal(input("Enter amount to transfer: "))
    if amount <= 0:
        print("Invalid amount. Please enter a positive value.")
        return

        # Check if the user has sufficient balance
    query = "SELECT acc_balance FROM acc_info WHERE user_name = %s"
    cursor.execute(query, (user[1],))
    sender_balance = cursor.fetchone()

    if sender_balance[0] < amount:
        print("Insufficient balance. Transaction aborted.")
        return

    # Consume any unread results before executing the update query
    cursor.fetchall()

    # Deduct the transferred amount from the sender's account balance
    new_sender_balance = sender_balance[0] - amount
    update_sender_query = "UPDATE acc_info SET acc_balance = %s WHERE user_name = %s"
    cursor.execute(update_sender_query, (new_sender_balance, user[1]))
    connect.commit()  # Consume the result

    # Add the transferred amount to the beneficiary's account balance
    update_beneficiary_query = "UPDATE acc_info SET acc_balance = acc_balance + %s WHERE user_name = %s"
    cursor.execute(update_beneficiary_query, (amount, beneficiary[1]))
    connect.commit()  # Consume the result

    # Insert transaction record
    insert_transaction_query = "INSERT INTO transaction (sender_acc_no, benf_acc_no, amount) VALUES (%s, %s, %s)"
    cursor.execute(insert_transaction_query, (user[0], beneficiary[2], amount))
    connect.commit()

    print("Funds transferred successfully.")

    show_options(cursor, connect, user)


# 8. View Transaction
def view_transactions(cursor, connect, user):
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

    show_options(cursor, connect, user)


# 9. Change Pin
def change_pin(cursor, connect, user):
    card_number = int(input("Enter card number: "))

    # Check if the card exists in the database
    query = "SELECT * FROM card WHERE card_no = %s"
    cursor.execute(query, (card_number,))
    card = cursor.fetchone()

    if not card:
        print("Card not found. Please enter valid card details.")
        return
        show_options(cursor, connect, user)
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
    connect.commit()
    print("PIN changed successfully.")

    show_options(cursor, connect, user)


#10. Update Information
def update_info(cursor, connect, user):
    print(f"Update Account Information of {user[0]:}")
    new_address = input("Enter new address: ")

    # Loop until a valid mobile number is entered
    while True:
        new_mobile = input("Enter new mobile number: ")
        if len(new_mobile) == 10 and new_mobile.isdigit() and new_mobile[0] in ['6', '7', '8', '9']:
            break
        else:
            print("Invalid mobile number. Mobile number must be 10 digits starting with 7, 8, or 9.")

    cursor.execute("UPDATE acc_info SET address = %s, mobile_no = %s WHERE user_name = %s",
                   (new_address, new_mobile, user[1]))
    connect.commit()
    print("Account information updated successfully!")

    show_options(cursor, connect, user)


#DB Connection:
#Connection to load data:
def sql_connect():
    try:
        connection = mysql.connector.connect(host="localhost", user="root", password="Nine@123", database="Bank_Sch")
        return connection

    except mysql.connector.Error as error:
        print("Error connecting to MySQL database:", error)
        return None


#Connection to fetch data:
def fetch_data(cursor, sql_query, values=None):
    if values is not None:
        cursor.execute(sql_query, values)
    else:
        cursor.execute(sql_query)

    #For fetching the data
    data = cursor.fetchone()
    return data


#Connection to add balance:
def balance_add(cursor, connect, user, deposit_amount, acc_no):
    # Update the user's balance in the database
    cursor.execute("UPDATE acc_info SET acc_balance = acc_balance + %s WHERE acc_no = %s", (deposit_amount, acc_no))
    connect.commit()

    # Fetch and print the updated balance
    cursor.execute("SELECT acc_balance FROM acc_info WHERE acc_no = %s", (acc_no,))
    updated_balance = cursor.fetchone()[0]
    print(f"Your account has been credited with {deposit_amount}. New balance is {updated_balance}.")

    show_options(cursor, connect, user)
