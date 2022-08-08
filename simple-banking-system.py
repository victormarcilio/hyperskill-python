import random
import sqlite3

class Bank:
    def __init__(self):
        self.conn = start_database()
        self.cursor = self.conn.cursor()

    def create_account(self):
        card_number = self.generate_card_number()
        pin = generate_pin()
        query = f"INSERT INTO Card (number, pin) values( {card_number}, {pin})"
        self.cursor.execute(query)
        self.conn.commit()
        print("Your card has been created")
        print("Your card number:")
        print(card_number)
        print("Your card PIN:")
        print(pin)

    def main_loop(self):
        while True:
            choice = main_menu()
            if choice == 0:
                finish()
            if choice == 1:
                self.create_account()
            elif choice == 2:
                self.login()

    def generate_card_number(self):
        while True:
            random_number = "400000"
            while len(random_number) < 15:
                random_number = random_number + str(random.randint(0, 9))
            random_number += str(luhn_digit(random_number))
            query = f"SELECT * FROM Card WHERE number == {random_number}"
            self.cursor.execute(query)
            if not self.cursor.fetchone():
                return random_number

    def login(self):
        print("Enter your card number:")
        card = input()
        print("Enter your PIN:")
        pin = input()
        query = f"SELECT * from Card WHERE number == {card} AND pin == {pin}"
        result = self.cursor.execute(query).fetchone()
        if result:
            self.logged_in(card)
        else:
            print("Wrong card number or PIN!")

    def logged_in(self, card):
        print("You have successfully logged in!")
        while True:
            choice = int(logged_menu())
            if choice == 0:
                finish()
            elif choice == 1:
                print(f"Balance: {self.get_balance(card)[0]}")
            elif choice == 2:
                self.add_income(card)
            elif choice == 3:
                self.transfer(card)
            elif choice == 4:
                self.close_account(card)
                return
            elif choice == 5:
                print("You have successfully logged out!")
                return

    def get_balance(self, card_number):
        query = f"SELECT balance from card WHERE number == {card_number}"
        return self.cursor.execute(query).fetchone()[0]

    def close_account(self, card):
        query = f"DELETE from card where number = {card}"
        self.cursor.execute(query)
        self.conn.commit()
        print("The account has been closed!")

    def add_income(self, card):
        print("Enter income:")
        income = int(input())
        current_balance = self.get_balance(card)
        query = f"UPDATE Card set balance = {current_balance + income} where number == {card}"
        self.cursor.execute(query)
        self.conn.commit()
        print("Income was added")

    def transfer(self, card):
        print("Transfer")
        print("Enter card number:")
        receiver = input()
        if card == receiver:
            print("You can't transfer money to the same account!")
        elif not check_luhn(receiver):
            print("Probably you made a mistake in the card number. Please try again!")
        elif not self.account_exists(receiver):
            print("Such a card does not exist.")
        else:
            print("Enter how much money you want to transfer:")
            amount = int(input())
            amount_available = self.get_balance(card)
            if amount > amount_available:
                print("Not enough money!")
            else:
                self.transfer_transaction(amount, card, receiver)

    def transfer_transaction(self, amount, from_, to):
        sender_balance = self.get_balance(from_)
        receiver_balance = self.get_balance(to)
        self.update_balance(from_, sender_balance - amount)
        self.update_balance(to, receiver_balance + amount)
        self.conn.commit()
        print("Success!")

    def update_balance(self, card, new_amount):
        query = f"UPDATE card set balance = {new_amount} WHERE number = {card}"
        self.cursor.execute(query)

    def account_exists(self, card_number):
        query = f"SELECT * from card where number = {card_number}"
        return self.cursor.execute(query).fetchone() is not None


def start_database():
    conn = sqlite3.connect("card.s3db")
    create_card_table(conn)
    return conn


def create_card_table(conn):
    create_statement = """CREATE TABLE IF NOT EXISTS card(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            number TEXT,
                            pin TEXT,
                            balance INTEGER DEFAULT 0)"""
    conn.cursor().execute(create_statement)
    conn.commit()


def main_menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    return int(input())


def finish():
    print("Bye")
    exit()


def luhn_digit(number):
    digits = [int(digit) for digit in number]
    for i in range(0, len(digits), 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    remainder = sum(digits) % 10
    return 10 - remainder if remainder else 0


def generate_pin():
    return str(random.randint(10000, 19999))[1:]


def logged_menu():
    print("1. Balance")
    print("2. Add Income")
    print("3. Do transfer")
    print("4. Close Account")
    print("5. Log out")
    print("0. Exit")
    return input()


def check_luhn(receiver):
    return receiver[-1] == str(luhn_digit(receiver[:-1]))


Bank().main_loop()
