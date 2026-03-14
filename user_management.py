import json
from datetime import datetime,timedelta


class UserManagement:

    members_file = "data.json"
    checkout_file = "checkout.json"
    books_file = "books.json"

    def __init__(self, user_id):
        self.user_id = user_id

    def view_books(self):

        books = self.load_books()

        if not books:
            print("No books available")
            return

        print("\nAvailable Books\n")

        for book in books:
            print(f"Book ID : {book['bookid']}")
            print(f"Title   : {book.get('name', 'N/A')}")
            print(f"Author  : {book.get('authorname', 'N/A')}")
            print(f"Year    : {book.get('DOP', 'N/A')}")
            print(f"Quantity: {book.get('quantity', 'N/A')}")
            print("-" * 30)

    def load_members(self):
        try:
            with open(self.members_file, "r") as f:
                return json.load(f)
        except:
            return []

    def load_checkout(self):
        try:
            with open(self.checkout_file, "r") as f:
                return json.load(f)
        except:
            return []

    def save_checkout(self, data):
        with open(self.checkout_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_books(self):
        try:
            with open(self.books_file, "r") as f:
                return json.load(f)
        except:
            return []

    def save_books(self, data):
        with open(self.books_file, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def user_choice():
        print("\nWelcome to User Management System")
        print("Please choose an option:")
        print("1.View All Books")
        print("2.Add Book")
        print("3.Checkout Book")
        print("4.Return Book")
        print("5.Exit")
        return input("Enter your choice: ")

    def minimum_deposit(self, user_id):

        users = self.load_members()

        for user in users:
            if user["id"] == user_id and user["deposit"] > 499:
                return True

        print("Insufficient funds")
        return False

    def maximum_books(self, user_id):

        checkouts = self.load_checkout()

        for user in checkouts:
            if user["user_id"] == user_id:
                if len(user["checkout_details"]) >= 3:
                    print("You have already Borrowed maximum 3 books")
                    return False

        return True

    def isvalid(self, user_id, book_id):

        checkouts = self.load_checkout()

        for checkout in checkouts:
            if checkout["user_id"] == user_id:
                for b in checkout["checkout_details"]:
                    if b["book_id"] == book_id:
                        print("Book Already Borrowed")
                        return False

        return True

    def quantity(self, book_id):

        books = self.load_books()

        for book in books:
            if book["bookid"] == book_id:
                if book["quantity"] <= 0:
                    print("Book Not Available")
                    return False
                return True

        print("Book ID not found")
        return False

    def reduce_quantity(self, book_id):

        books = self.load_books()

        for book in books:
            if book["bookid"] == book_id:
                book["quantity"] -= 1

        self.save_books(books)

    def increase_quantity(self, book_id):

        books = self.load_books()

        for book in books:
            if book["bookid"] == book_id:
                book["quantity"] += 1

        self.save_books(books)

    def add_book(self, user_id, book):

        book_id = book["book_id"]

        if (self.minimum_deposit(user_id)
                and self.maximum_books(user_id)
                and self.isvalid(user_id, book_id)
                and self.quantity(book_id)):

            checkouts = self.load_checkout()
            checkout_date = datetime.today()
            book_details = {
                "book_id": book_id,
                "due_date": (checkout_date+timedelta(days=14)).strftime('%Y-%m-%d'),
                "return_date": "",
                "book_checkout_date": datetime.today().strftime('%Y-%m-%d')
            }

            user_found = False

            for user in checkouts:
                if user["user_id"] == user_id:
                    user["checkout_details"].append(book_details)
                    user_found = True
                    break

            if not user_found:
                new_checkout = {
                    "user_id": user_id,
                    "checkout_details": [book_details]
                }
                checkouts.append(new_checkout)

            self.save_checkout(checkouts)
            self.reduce_quantity(book_id)

            print("Book Added Successfully")

        else:
            print("Book cannot be added")

    def return_book(self, user_id, book_id):

        checkouts = self.load_checkout()

        for user in checkouts:
            if user["user_id"] == user_id:
                user["checkout_details"] = [
                    book for book in user["checkout_details"]
                    if book["book_id"] != book_id
                ]

                self.increase_quantity(book_id)
                print("Book Returned")

        self.save_checkout(checkouts)
