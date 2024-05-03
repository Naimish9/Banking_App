import re


#Registed User validation:

# Input validation functions
def validate_username(user_name):
    return bool(re.match(r'^[a-zA-Z\s]+$', user_name))


def validate_address(address):
    return bool(re.match(r'^[a-zA-Z0-9\s,-]+$', address))


def validate_aadhar(aadhar):
    aadhar = ''.join(filter(str.isdigit, aadhar))
    if len(aadhar) == 12:
        aadhar_with_gaps = ' '.join(aadhar[i:i + 4] for i in range(0, len(aadhar), 4))
        return aadhar_with_gaps
    else:
        return None


def validate_mobile(mobile):
    return bool(re.match(r'^[7-9][0-9]{9}$', mobile))


def validate_password(acc_pwd):
    return bool(re.match(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', acc_pwd))
