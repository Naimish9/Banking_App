import random

#Account number generation:
def generate_account_number():
    return ''.join(random.choices('0123456789', k=random.randint(11, 14)))

