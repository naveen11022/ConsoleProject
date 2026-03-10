import json
from Admin.bank import Admin
FILE = "user.json"


class User:
    def __init__(self, name="", email="", pin=0, balance=0):
        self.name = name
        self.email = email
        self.__pin = pin
        self.__balance = balance

    def create_user(self):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        for user in data:
            if user["email"] == self.email:
                print("User already exists.")
                return

        data.append(self.to_dict())

        with open(FILE, "w") as f:
            json.dump(data, f, indent=4)

        print("Account created successfully.")

    def login(self, email, pin):
        with open(FILE, "r") as f:
            data = json.load(f)

        for user in data:
            if user["email"] == email and user["pin"] == pin:
                self.name = user["name"]
                self.email = user["email"]
                self.__pin = user["pin"]
                self.__balance = user["balance"]
                print("Login successful.")
                return True

        print("Invalid email or PIN.")
        return False

    def deposit(self, amount):
        self.__balance += amount
        print(f"Deposited: {amount}")
        self.update_user()

    def withdraw(self, amount):
        if Admin.TotalAmount < amount:
            print("Bank has insufficient funds.")
            return
        if amount > self.__balance:
            print("Insufficient balance.")
            return

        self.__balance -= amount
        print(f"Withdrawn: {amount}")
        self.update_user()

    def check_balance(self):
        print(f"Current Balance: {self.__balance}")

    def change_pin(self, new_pin):
        self.__pin = new_pin
        self.update_user()
        print("PIN changed successfully.")

    def update_user(self):
        with open(FILE, "r") as f:
            data = json.load(f)

        for user in data:
            if user["email"] == self.email:
                user["balance"] = self.__balance
                user["pin"] = self.__pin

        with open(FILE, "w") as f:
            json.dump(data, f, indent=4)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "pin": self.__pin,
            "balance": self.__balance
        }


choice = 0

while choice != 3:
    print("\nWelcome to Bank Management System")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        name = input("Enter name: ")
        email = input("Enter email: ")
        pin = int(input("Enter 4-digit PIN: "))

        user = User(name, email, pin)
        user.create_user()

    elif choice == 2:
        email = input("Enter email: ")
        pin = int(input("Enter PIN: "))

        user = User()

        if user.login(email, pin):

            while True:
                print("\n1 Deposit")
                print("2 Withdraw")
                print("3 Check Balance")
                print("4 Change PIN")
                print("5 Logout")

                option = int(input("Enter option: "))

                if option == 1:
                    amount = int(input("Enter amount: "))
                    user.deposit(amount)

                elif option == 2:
                    amount = int(input("Enter amount: "))
                    user.withdraw(amount)

                elif option == 3:
                    user.check_balance()

                elif option == 4:
                    new_pin = int(input("Enter new PIN: "))
                    user.change_pin(new_pin)

                elif option == 5:
                    print("Logged out.")
                    break

    elif choice == 3:
        print("Exiting program...")