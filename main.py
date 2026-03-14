from validators import Validators
from Borrow import Borrower
from user_management import UserManagement
from Admin.Admin import Admin

print("=" * 40)
print("  Library Management System")
print("=" * 40)

while True:

    print("\nMain Menu")
    print("1. Register (Borrower)")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":

        while True:
            username = input("Enter your email: ").strip()
            if Validators.email_validator(username):
                break

        password = input("Enter your password: ").strip()
        user = Borrower(username, password)
        user.create_user()

    elif choice == "2":

        while True:
            username = input("Enter your email: ").strip()
            if Validators.email_validator(username):
                break

        password = input("Enter your password: ").strip()
        login_user = Borrower.login(username, password)

        if login_user is None:
            print("Login Failed")
            continue

        current_user = login_user["user_id"]
        is_admin = login_user["admin"]

        if is_admin:
            admin_obj = Admin(current_user)
            print(f"\nWelcome, Admin!")

            while True:
                admin_choice = Admin.admin_choice()

                if admin_choice == "1":
                    admin_obj.add_book()

                elif admin_choice == "2":
                    admin_obj.remove_book()

                elif admin_choice == "3":
                    admin_obj.modify_book()

                elif admin_choice == "4":
                    admin_obj.list_books()

                elif admin_choice == "5":
                    admin_obj.search_book()

                elif admin_choice == "6":
                    admin_obj.add_borrower()

                elif admin_choice == "7":
                    admin_obj.add_admin()

                elif admin_choice == "8":
                    admin_obj.promote_to_admin()

                elif admin_choice == "9":
                    admin_obj.manage_fine_limit()

                elif admin_choice == "10":
                    admin_obj.view_all_borrowers()

                elif admin_choice == "11":
                    admin_obj.reports_menu()

                elif admin_choice == "12":
                    print("Logging out...")
                    break

                else:
                    print("Invalid Choice")

        else:
            user_obj = UserManagement(current_user)
            print(f"\nWelcome, {username}!")

            while True:
                user_choice = UserManagement.user_choice()

                if user_choice == "1":
                    user_obj.view_books()

                elif user_choice == "2":
                    user_obj.search_book()

                elif user_choice == "3":
                    user_obj.view_books()
                    try:
                        book_id = int(input("Enter Book ID to checkout: "))
                        user_obj.add_book(current_user, {"book_id": book_id})
                    except ValueError:
                        print("Invalid Book ID")

                elif user_choice == "4":
                    user_obj.view_my_books(current_user)

                elif user_choice == "5":
                    user_obj.manage_book(current_user)

                elif user_choice == "6":
                    user_obj.view_history(current_user)

                elif user_choice == "7":
                    user_obj.report_card_lost(current_user)

                elif user_choice == "8":
                    print("Logging out...")
                    break

                else:
                    print("Invalid Choice")

    elif choice == "3":
        print("Exiting Library Management System. Goodbye!")
        break

    else:
        print("Invalid Choice")
