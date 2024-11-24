#!/usr/bin/python
import numpy as np  # Importing numpy for calculations


# Class to represent a user
class User:
    def __init__(self, username, pin, balance):
        self.username = username
        self.pin = pin
        self.balance = balance

    def authenticate(self, input_pin):
        return self.pin == input_pin

    def change_pin(self, new_pin):
        self.pin = new_pin
        print("NEW PIN SAVED.")


# Class for transaction validation logic
class Transaction:
    MIN_AMOUNT = 500  # Minimum transaction amount
    RECEIPT_FEE = 3   # Fee for printing a receipt

    @staticmethod
    def validate_amount(amount):
        if amount < Transaction.MIN_AMOUNT:
            print(f"MINIMUM AMOUNT IS {Transaction.MIN_AMOUNT} TAKA.")
            return False
        if amount % 500 != 0:
            print("AMOUNT MUST BE A MULTIPLE OF 500 TAKA.")
            return False
        return True


# Class to handle user balance-related operations
class BalanceManager:
    def __init__(self, user):
        self.user = user

    def get_balance(self):
        print(f"{self.user.username}, YOU HAVE {self.user.balance} TAKA IN YOUR ACCOUNT.")

    def deduct(self, amount):
        if amount > self.user.balance:
            print("INSUFFICIENT BALANCE.")
            return False
        self.user.balance -= amount
        return True

    def add(self, amount):
        self.user.balance += amount


# Class to handle withdrawals
class Withdrawal:
    def __init__(self, balance_manager):
        self.balance_manager = balance_manager

    def withdraw(self, amount):
        if not Transaction.validate_amount(amount):
            return
        if self.balance_manager.deduct(amount):
            print(f"WITHDRAWAL OF {amount} TAKA SUCCESSFUL.")
            try:
                # Ask if the user wants a receipt
                receipt = input("WOULD YOU LIKE A RECEIPT FOR AN EXTRA 3 TAKA? (Y/N): ").strip().lower()
                if receipt == 'y':
                    if self.balance_manager.deduct(Transaction.RECEIPT_FEE):
                        print("RECEIPT PRINTED. EXTRA 3 TAKA DEDUCTED.")
                print(f"NEW BALANCE: {self.balance_manager.user.balance} TAKA.")
            except Exception as e:
                print("AN ERROR OCCURRED WHILE PROCESSING YOUR RECEIPT REQUEST.", e)


# Class for all account-related operations
class Account:
    def __init__(self, user):
        self.user = user
        self.balance_manager = BalanceManager(user)
        self.withdrawal = Withdrawal(self.balance_manager)

    def deposit(self, amount):
        if Transaction.validate_amount(amount):
            self.balance_manager.add(amount)
            print(f"DEPOSIT SUCCESSFUL. NEW BALANCE: {self.user.balance} TAKA.")

    def pay_bill(self, bill_type, amount):
        if Transaction.validate_amount(amount) and self.balance_manager.deduct(amount):
            print(f"{bill_type.capitalize()} BILL PAYMENT OF {amount} TAKA SUCCESSFUL. NEW BALANCE: {self.user.balance} TAKA.")

    def mobile_topup(self, phone_number, amount):
        if Transaction.validate_amount(amount) and self.balance_manager.deduct(amount):
            print(f"MOBILE TOP-UP OF {amount} TAKA TO {phone_number} SUCCESSFUL. NEW BALANCE: {self.user.balance} TAKA.")

    def fund_transfer(self, recipient_user, amount):
        if Transaction.validate_amount(amount):
            if self.balance_manager.deduct(amount):
                recipient_user.balance += amount
                print(f"FUND TRANSFER OF {amount} TAKA TO {recipient_user.username} SUCCESSFUL. NEW BALANCE: {self.user.balance} TAKA.")


# Class to manage the ATM system and user interactions
class ATM:
    def __init__(self):
        # Adding users: shehab, ritu, and saba
        self.users = {
            'shehab': User('shehab', '1722', 50000),
            'ritu': User('ritu', '1740', 60000),
            'saba': User('saba', '1631', 65000),
        }
        self.current_user = None
        self.account = None

    def start(self):
        self.show_title()
        self.authenticate_user()
        self.main_menu()

    def show_title(self):
        print("\n")
        print("="*40)
        print("      SRS ATM powered by Safekey Guardians")
        print("="*40)
        print("\n")

    def authenticate_user(self):
        attempts = 0
        while attempts < 3:
            try:
                username = input("\nENTER USER NAME: ").lower()
                if username in self.users:
                    self.current_user = self.users[username]
                    if self.check_pin():
                        print("LOGIN SUCCESSFUL.")
                        self.account = Account(self.current_user)
                        break
                else:
                    print("INVALID USERNAME.")
                    attempts += 1
            except Exception as e:
                print("AN ERROR OCCURRED WHILE AUTHENTICATING. PLEASE TRY AGAIN.", e)
        else:
            print("3 UNSUCCESSFUL ATTEMPTS. EXITING. YOUR CARD IS LOCKED.")
            exit()

    def check_pin(self):
        for _ in range(3):
            try:
                pin = input("PLEASE ENTER PIN: ")
                if self.current_user.authenticate(pin):
                    return True
                else:
                    print("INVALID PIN.")
            except Exception as e:
                print("AN ERROR OCCURRED WHILE VALIDATING PIN.", e)
        return False

    def main_menu(self):
        while True:
            try:
                response = input("\nSELECT OPTION: \nStatement (S) \nWithdraw (W) \nDeposit (D) \nChange PIN (P) \nBill Pay (B) \nMobile Top-up (T) \nFund Transfer (F) \nShow Total Balances (ST) \nQuit (Q) \n: ").lower()
                if response == 's':
                    self.account.balance_manager.get_balance()
                elif response == 'w':
                    self.handle_withdraw()
                elif response == 'd':
                    self.handle_deposit()
                elif response == 'p':
                    self.handle_change_pin()
                elif response == 'b':
                    self.handle_bill_payment()
                elif response == 't':
                    self.handle_topup()
                elif response == 'f':
                    self.handle_fund_transfer()
                elif response == 'st':  # New option for showing total balances
                    self.show_total_balances()
                elif response == 'q':
                    print("THANK YOU FOR USING THE ATM. GOODBYE!")
                    exit()
                else:
                    print("INVALID OPTION.")
            except Exception as e:
                print("AN ERROR OCCURRED WHILE PROCESSING YOUR REQUEST.", e)

    def handle_withdraw(self):
        try:
            amount = int(input("ENTER AMOUNT TO WITHDRAW: "))
            self.account.withdrawal.withdraw(amount)
        except ValueError:
            print("INVALID AMOUNT. PLEASE ENTER A NUMBER.")
        except Exception as e:
            print("AN ERROR OCCURRED WHILE PROCESSING YOUR WITHDRAWAL.", e)

    def handle_deposit(self):
        try:
            amount = int(input("ENTER AMOUNT TO DEPOSIT: "))
            self.account.deposit(amount)
        except ValueError:
            print("INVALID AMOUNT. PLEASE ENTER A NUMBER.")
        except Exception as e:
            print("AN ERROR OCCURRED WHILE PROCESSING YOUR DEPOSIT.", e)

    def handle_change_pin(self):
        try:
            new_pin = input("ENTER A NEW PIN: ")
            if len(new_pin) == 4 and new_pin.isdigit() and new_pin != self.current_user.pin:
                confirm_pin = input("CONFIRM NEW PIN: ")
                if confirm_pin == new_pin:
                    self.current_user.change_pin(new_pin)
                else:
                    print("PIN MISMATCH.")
            else:
                print("NEW PIN MUST BE 4 DIGITS AND DIFFERENT FROM CURRENT PIN.")
        except Exception as e:
            print("AN ERROR OCCURRED WHILE CHANGING YOUR PIN.", e)

    def handle_bill_payment(self):
        try:
            bill_type = input("SELECT BILL TYPE (Electricity/Water/Gas): ").lower()
            if bill_type in ['electricity', 'water', 'gas']:
                amount = int(input(f"ENTER {bill_type.capitalize()} BILL AMOUNT: "))
                self.account.pay_bill(bill_type, amount)
            else:
                print("INVALID BILL TYPE.")
        except ValueError:
            print("INVALID AMOUNT. PLEASE ENTER A NUMBER.")
        except Exception as e:
            print("AN ERROR OCCURRED WHILE PROCESSING BILL PAYMENT.", e)

    def handle_topup(self):
        try:
            phone_number = input("ENTER PHONE NUMBER FOR TOP-UP: ")
            amount = int(input("ENTER TOP-UP AMOUNT: "))
            self.account.mobile_topup(phone_number, amount)
        except ValueError:
            print("INVALID AMOUNT. PLEASE ENTER A NUMBER.")
        except Exception as e:
            print("AN ERROR OCCURRED WHILE PROCESSING TOP-UP.", e)

    def handle_fund_transfer(self):
        try:
            recipient_name = input("ENTER RECIPIENT USERNAME: ").lower()
            if recipient_name in self.users and recipient_name != self.current_user.username:
                recipient_user = self.users[recipient_name]
                amount = int(input("ENTER AMOUNT TO TRANSFER: "))
                self.account.fund_transfer(recipient_user, amount)
            else:
                print("INVALID RECIPIENT USERNAME.")
        except ValueError:
            print("INVALID AMOUNT. PLEASE ENTER A NUMBER.")
        except Exception as e:
            print("AN ERROR OCCURRED WHILE PROCESSING FUND TRANSFER.", e)

    def show_total_balances(self):
        try:
            balances = [user.balance for user in self.users.values()]
            total_balance = np.sum(balances)
            print(f"TOTAL BALANCE OF ALL USERS: {total_balance} TAKA.")
        except Exception as e:
            print("AN ERROR OCCURRED WHILE CALCULATING TOTAL BALANCE.", e)


# Instantiate and start the ATM
try:
    atm = ATM()
    atm.start()
except Exception as e:
    print("AN UNEXPECTED ERROR OCCURRED. PLEASE TRY AGAIN LATER.", e)
