# --------------Welcome to Banking Application-----------------

# Problem Statement:
I have created a banking-based program to replicate the operations that a real-time bank performs.

# Solution:
A banking application program is created that performs the below-mentioned operations:
1. Display Account Information
2. Add funds
3. Add Beneficiary
4. Beneficiaries List 
5. Add Card
6. List of Cards
7. Transfer Funds
8. View Transactions
9. Change PIN
10. Update Information
0. Exit

# Database:
The program uses the below mentioned 5 tables:
1. acc_info (acc_no, user_name, address, aadhar_no, mobile_no, acc_pwd, acc_balance)
2. Benf (user_name, benf_name, benf_acc_no, Benf_ifsc)
3. card (user_name, card_no, card_type, pin, cvv)
4. transaction (idtransaction, sender_acc_no, benf_acc_no, amount, tr_timestamp)
5. BankIFSC (IFSC_Code)

# How to run:
1. Clone the repository to your local machine.
2. Install the required dependencies (mysql-connector-python).
3. Set up MySQL database with the required schema. You can find the database schema in the 'BA_Database_Schema' file.
4. Update the MySQL connection details in the code (host, user, password, database) to match your local setup.

# Program Flow:
1. Main window:
	Contains the below operations:
	A. Register: All the users have to register, if they have not. Then only they can choose the 2nd operation.
	B. Login: Users can login after registering with their required details.
		Once the user have logged in they can perform multiple operations.
	C. Exit: If user doesn't want to proceed 
