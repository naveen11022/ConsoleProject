class Admin:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self):
        email = input("Enter Admin Email ID: ")
        password = input("Enter Password: ")

        if email == self.email and password == self.password:
            print("\nLogin Successful!")
            self.admin_menu()
        else:
            print("Invalid Email or Password")

    def admin_menu(self):
        print("\nWelcome Administrator")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. View Books")
        print("4. Logout")


