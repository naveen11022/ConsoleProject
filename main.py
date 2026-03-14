from validators import Validators
from Borrow import Borrower
from user_management import UserManagement

print("Library Management System")

while True:

    print("\nMenu")
    print("1.Create")
    print("2.Login")
    print("3.Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        while True:
            username = input("Enter your email: ")
            email_validator = Validators()

            if email_validator.email_validator(username):
                break
            else:
                print("Invalid Email")

        password = input("Enter your password: ")

        user = Borrower(username, password)
        user.create_user()

    elif choice == "2":

        while True:
            username = input("Enter your email: ")
            email_validator = Validators()

            if email_validator.email_validator(username):
                break
            else:
                print("Invalid Email")

        password = input("Enter your password: ")

        login_user = Borrower.login(username, password)

        if login_user is None:
            print("Login Failed")
            continue

        print("Login Successful")

        current_user = login_user["user_id"]

        user_obj = UserManagement(current_user)

        while True:

            user_choice = UserManagement.user_choice()

            if user_choice == "1":
                user_obj.view_books()

            elif user_choice == "2" or user_choice == "3":

                book_id = int(input("Enter Book ID: "))

                book = {"book_id": book_id}

                user_obj.add_book(current_user, book)

            elif user_choice == "4":

                book_id = int(input("Enter Book ID to return: "))
                user_obj.return_book(current_user, book_id)

            elif user_choice == "5":

                print("Logging out...")
                break

            else:
                print("Invalid Choice")

    elif choice == "3":
        print("Exiting Library Management System")
        break

    else:
        print("Invalid Choice")

