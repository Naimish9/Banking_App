
from generate import generate_account_number
from main import details_into_db
from options import show_options, fetch_data
from validations import *

# User Inputs:
def register_user():

    max_attempts = 3  # Maximum number of attempts allowed
    attempts = {'username': 0, 'address': 0, 'aadhar': 0, 'mobile': 0, 'password': 0}

    # Get valid input from user
    while True:
        user_name = input("Enter username (alphabets only): ")
        attempts['username'] += 1
        if validate_username(user_name):
            break
        elif attempts['username'] >= max_attempts:
            print("Maximum attempts exceeded. Returning to main menu.")
            return
        else:
            print("Invalid username. Please enter alphabets only.")

    while True:
        address = input("Enter address (alphanumeric with special characters): ")
        attempts['address'] += 1
        if validate_address(address):
            break
        elif attempts['address'] >= max_attempts:
            print("Maximum attempts exceeded. Returning to main menu.")
            return
        else:
            print("Invalid address. Please enter alphanumeric characters with special characters.")

    while True:
        aadhar = input("Enter Aadhar number (12 digits with automatic gaps insertion after every 4 digits): ")
        attempts['aadhar'] += 1
        aadhar_with_gaps = validate_aadhar(aadhar)
        if aadhar_with_gaps:
            print("Aadhar number with automatic gaps insertion:")
            print(aadhar_with_gaps)
            break
        elif attempts['aadhar'] >= max_attempts:
            print("Maximum attempts exceeded. Returning to main menu.")
            return
        else:
            print("Invalid Aadhar number. Please enter 12 digits.")

    while True:
        mobile_no = input("Enter mobile number (10 digits): ")
        attempts['mobile'] += 1
        if validate_mobile(mobile_no):
            break
        elif attempts['mobile'] >= max_attempts:
            print("Maximum attempts exceeded. Returning to main menu.")
            return
        else:
            print("Invalid mobile number.")

    while True:
        acc_pwd = input("Enter password (minimum 8 characters, alphanumeric with special characters): ")
        attempts['password'] += 1
        if validate_password(acc_pwd):
            break
        elif attempts['password'] >= max_attempts:
            print("Maximum attempts exceeded. Returning to main menu.")
            return
        else:
            print("Invalid password. Password should be at least 8 characters long and contain alphanumeric "
                  "characters with special charcters.")

    register_user()
    # Display User details after registration
    #clean the window before displaying the details:
    #for o/p screen
    # os.system('clear')
    # fro notebook (not working, skipping to the input section)
    # clear_output(wait=True)

    print("Registration successful!")
    acc_no = generate_account_number()
    print("Your Account Number: ", acc_no)
    print("Your User Name: ", user_name)
    print("Your Address: ", address)
    print("Your Aadhar Number: ", aadhar)
    print("Your Mobile Number: ", mobile_no)
    print("Your Account Password: ", acc_pwd)
    # print("Your Balance: ",user_name)

    details_into_db(acc_no, user_name, address, aadhar, mobile_no, acc_pwd)


# User login:
def login_user():
    user_name = input("Enter username: ")
    password = input("Enter password: ")

    sql_query = "SELECT * FROM acc_info WHERE user_name = %s AND acc_pwd = %s"
    values = (user_name, password)

    user = fetch_data(sql_query, values)

    if user:
        print("Welcome,", user[1])
        # Assuming there's a function called show_options to display options
        show_options(user)
    else:
        print("Invalid username or password.")
