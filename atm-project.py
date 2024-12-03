#!/usr/bin/python
import numpy as np 


# represent a user
class User:
    def __init__(self, username, pin, balance):
        self.username = username  # Public attribute
        self.__pin = pin  # Private attribute
        self.__balance = balance  # Private attribute
        self.transaction_history = []  # Store transaction history

    def authenticate(self, input_pin):
        """Check if the entered PIN matches the user's PIN."""
        return self.__pin == input_pin

    def change_pin(self, new_pin):
        """Change the user's PIN securely."""
        self.__pin = new_pin
        print("NEW PIN SAVED.")

    def get_balance(self):
        """Getter for the user's balance."""
        return self.__balance

    def set_balance(self, amount):
        """Setter for the user's balance."""
        self.__balance = amount

    def add_transaction(self, transaction):
        """Add a transaction to the user's history."""
        self.transaction_history.append(transaction)


# transaction logic
class Transaction:
    MIN_AMOUNT = 500  # Minimum amount
    RECEIPT_FEE = 3  # Fee for printing a receipt

    @staticmethod
    def validate_amount(amount):
        """Validate if the transaction amount is allowed."""
        if amount < Transaction.MIN_AMOUNT:
            print(f"MINIMUM AMOUNT IS {Transaction.MIN_AMOUNT} TAKA.")
            return False
        if amount % 500 != 0:
            print("AMOUNT MUST BE A MULTIPLE OF 500 TAKA.")
            return False
        return True


#  balance-related operations
class BalanceManager:
    def __init__(self, user):
        self.user = user

    def get_balance(self):
        """Display the user's current balance."""
        print(f"{self.user.username}, YOU HAVE {self.user.get_balance()} TAKA IN YOUR ACCOUNT.")

    def deduct(self, amount, description):
        """Deduct the specified amount from the user's balance."""
        if amount > self.user.get_balance():
            print("INSUFFICIENT BALANCE.")
            return False
        self.user.set_balance(self.user.get_balance() - amount)
        self.user.add_transaction(f"-{amount} TAKA: {description}")
        return True

    def add(self, amount, description):
        """Add the specified amount to the user's balance."""
        self.user.set_balance(self.user.get_balance() + amount)
        self.user.add_transaction(f"+{amount} TAKA: {description}")


# handle withdrawals
class Withdrawal:
    def __init__(self, balance_manager):
        self.balance_manager = balance_manager

    def withdraw(self, amount):
        """Perform a withdrawal after validating the amount."""
        if not Transaction.validate_amount(amount):
            return

        if self.balance_manager.deduct(amount, "Withdrawal"):
            print(f"WITHDRAWAL OF {amount} TAKA SUCCESSFUL.")
            try:
                receipt = input("WOULD YOU LIKE A RECEIPT FOR AN EXTRA 3 TAKA? (Y/N): ").strip().lower()
                if receipt == 'y':
                    if self.balance_manager.deduct(Transaction.RECEIPT_FEE, "Receipt Fee"):
                        print("RECEIPT PRINTED. EXTRA 3 TAKA DEDUCTED.")
                print(f"NEW BALANCE: {self.balance_manager.user.get_balance()} TAKA.")
            except Exception as e:
                print("AN ERROR OCCURRED WHILE PROCESSING YOUR RECEIPT REQUEST.", e)


# all account-related operations
class Account:
    def __init__(self, user):
        self.user = user
        self.balance_manager = BalanceManager(user)
        self.withdrawal = Withdrawal(self.balance_manager)

    def deposit(self, amount):
        """Handle deposits by validating the amount and adding it to the balance."""
        if Transaction.validate_amount(amount):
            self.balance_manager.add(amount, "Deposit")
            print(f"DEPOSIT SUCCESSFUL. NEW BALANCE: {self.user.get_balance()} TAKA.")

    def pay_bill(self, bill_type, amount):
        """Pay bills after validating the amount and deducting it from the balance."""
        if Transaction.validate_amount(amount) and self.balance_manager.deduct(amount, f"{bill_type.capitalize()} Bill Payment"):
            print(f"{bill_type.capitalize()} BILL PAYMENT OF {amount} TAKA SUCCESSFUL. NEW BALANCE: {self.user.get_balance()} TAKA.")

    def mobile_topup(self, phone_number, amount):
        """Perform a mobile top-up after validating the amount and deducting it."""
        if Transaction.validate_amount(amount) and self.balance_manager.deduct(amount, f"Mobile Top-up ({phone_number})"):
            print(f"MOBILE TOP-UP OF {amount} TAKA TO {phone_number} SUCCESSFUL. NEW BALANCE: {self.user.get_balance()} TAKA.")

    def fund_transfer(self, recipient_user, amount):
        """Perform a fund transfer and update both balances."""
        if Transaction.validate_amount(amount):
            if self.balance_manager.deduct(amount, f"Transfer to {recipient_user.username}"):
                recipient_user.set_balance(recipient_user.get_balance() + amount)
                recipient_user.add_transaction(f"+{amount} TAKA: Transfer from {self.user.username}")
                print(f"FUND TRANSFER OF {amount} TAKA TO {recipient_user.username} SUCCESSFUL.")
                print(f"NEW BALANCE: {self.user.get_balance()} TAKA.")

    def show_mini_statement(self):
        """Display the user's transaction history."""
        print("\nMINI STATEMENT:")
        if self.user.transaction_history:
            for transaction in self.user.transaction_history:
                print(transaction)
        else:
            print("NO TRANSACTIONS AVAILABLE.")


# manage the ATM system and user interactions
class ATM:
    def __init__(self):
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
        """Display the ATM title."""
        print("\n")
        print("=" * 50)
        print("      SRS ATM powered by Safekey Guardians")
        print("=" * 50)
        print("\n")

    def authenticate_user(self):
        """Authenticate the user by verifying username and PIN."""
        attempts = 0
        while attempts < 3:
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
        else:
            print("3 UNSUCCESSFUL ATTEMPTS. EXITING. YOUR CARD IS LOCKED.")
            exit()

    def check_pin(self):
        """Verify the user's PIN."""
        for _ in range(3):
            pin = input("PLEASE ENTER PIN: ")
            if self.current_user.authenticate(pin):
                return True
            print("INVALID PIN.")
        return False

    def main_menu(self):
        """Display the main menu and handle user options."""
        while True:
            print("\nSELECT OPTION: \nBalance Inquiry (B) \nMini Statement (M) \nWithdraw (W) \nDeposit (D) \nChange PIN (P) \nBill Pay (L) \nTop-up (T) \nFund Transfer (F) \nQuit (Q) \n")
            choice = input("SELECT AN OPTION: ").strip().lower()

            if choice == 'b':
                self.account.balance_manager.get_balance()
            elif choice == 'm':
                self.account.show_mini_statement()
            elif choice == 'w':
                self.handle_withdraw()
            elif choice == 'd':
                self.handle_deposit()
            elif choice == 'l':
                self.handle_bill_payment()
            elif choice == 'p':
                self.handle_change_pin()
            elif choice == 't':
                self.handle_topup()
            elif choice == 'f':
                self.handle_fund_transfer()
            elif choice == 'q':
                print("THANK YOU FOR USING SRS ATM. GOODBYE!")
                exit()
            else:
                print("INVALID OPTION. PLEASE TRY AGAIN.")

    def handle_withdraw(self):
        """Handle withdrawal process."""
        try:
            amount = int(input("ENTER AMOUNT TO WITHDRAW: "))
            self.account.withdrawal.withdraw(amount)
        except ValueError:
            print("INVALID AMOUNT ENTERED.")

    def handle_deposit(self):
        """Handle deposit process."""
        try:
            amount = int(input("ENTER AMOUNT TO DEPOSIT: "))
            self.account.deposit(amount)
        except ValueError:
            print("INVALID AMOUNT ENTERED.")

    def handle_change_pin(self):
        """Allow the user to change their PIN."""
        try:
            new_pin = input("ENTER NEW PIN: ").strip()
            self.current_user.change_pin(new_pin)
        except Exception as e:
            print("AN ERROR OCCURRED WHILE CHANGING THE PIN.", e)

    def handle_bill_payment(self):
        """Handle bill payment options."""
        try:
            bill_types = {
                1: "Electricity",
                2: "Water",
                3: "Internet",
                4: "Gas",
                5: "Telephone",
                6: "TV",
                7: "Others"
            }

            print("\nBILL TYPES:")
            for key, value in bill_types.items():
                print(f"{key}. {value}")

            choice = int(input("SELECT BILL TYPE (1-7): "))
            if choice in bill_types:
                if choice == 7:  # If the user selects "Others"
                    bill_type = input("ENTER THE NAME OF THE BILL TYPE: ").strip().capitalize()
                else:
                    bill_type = bill_types[choice]

                amount = int(input(f"ENTER AMOUNT FOR {bill_type.upper()} BILL: "))
                self.account.pay_bill(bill_type, amount)
            else:
                print("INVALID BILL TYPE SELECTED.")
        except ValueError:
            print("INVALID INPUT. PLEASE ENTER A VALID NUMBER.")

    def handle_topup(self):
        """Handle mobile top-up process."""
        try:
            phone_number = input("ENTER PHONE NUMBER: ").strip()
            amount = int(input("ENTER AMOUNT TO TOP-UP: "))
            self.account.mobile_topup(phone_number, amount)
        except ValueError:
            print("INVALID AMOUNT ENTERED.")

    def handle_fund_transfer(self):
        """Handle fund transfer process."""
        try:
            recipient_username = input("ENTER RECIPIENT USERNAME: ").lower()
            if recipient_username in self.users and recipient_username != self.current_user.username:
                recipient_user = self.users[recipient_username]
                amount = int(input(f"ENTER AMOUNT TO TRANSFER TO {recipient_username.capitalize()}: "))
                self.account.fund_transfer(recipient_user, amount)
            else:
                print("INVALID RECIPIENT.")
        except ValueError:
            print("INVALID AMOUNT ENTERED.")


# Main program execution
if __name__ == "__main__":
    atm = ATM()
    atm.start()
