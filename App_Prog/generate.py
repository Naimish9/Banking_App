import mysql.connector
import re
import random
import decimal

#Account number generation:
def generate_account_number():
    return ''.join(random.choices('0123456789', k=random.randint(11, 14)))

#Card number generation:
def generate_card(self, card_type):
        card_number = ''.join(random.choices('0123456789', k=16))
        pin = ''.join(random.choices('0123456789', k=4))
        cvv = ''.join(random.choices('0123456789', k=3))
        return {"type": card_type, "number": card_number, "pin": pin, "cvv": cvv}