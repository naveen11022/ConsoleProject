import json
from datetime import datetime


class UserManagement:

    members_file = "members.json"
    checkout_file = "checkout.json"
    books_file = "books.json"

    book_details = {
        "book_id": 345,
        "due_date": datetime.today().strftime('%Y-%m-%d'),
        "return_date": "",
        "book_checkout_date": datetime.today().strftime('%Y-%m-%d'),
    }

    return_details = {
        "return_date": datetime.today().strftime('%Y-%m-%d'),
    }

    def __init__(self, user_id):
        self.user_id = user_id

    def view_books(self):

        books = self.load_books()

        if not books:
            print("No books available")
            return

        print("\nAvailable Books\n")

        for book in books:
            print(f"Book ID : {book['book_id']}")
            print(f"Title   : {book.get('title', 'N/A')}")
            print(f"Author  : {book.get('author', 'N/A')}")
            print("-" * 30)

    def load_members(self):
        try:
            with open(self.members_file, "r") as f:
                return json.load(f)
        except:
            return []

    def save_members(self, data):
        with open(self.members_file, "w") as f:
            json.dump(data, f, indent=4)

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

    @staticmethod
    def user_choice():
        print("\nWelcome to User Management System")
        print("Please choose an option:")
        print("1.View All Books")
        print("2.Add Book")
        print("3.Checkout Book")
        print("4.Return Book")
        print("5.Exit")
        user_choice = input("Enter your choice: ")
        return user_choice

    def minimum_deposit(self, user_id):

        users = self.load_members()

        for user in users:
            if user["id"] == user_id:
                if user["deposit"] > 499:
                    return True

        print("Insufficient funds")
        return False

    def maximum_books(self, user_id):

        checkouts = self.load_checkout()

        for user in checkouts:
            if user["user_id"] == user_id:
                if len(user["checkout_details"]) < 3:
                    return True

        print("You have already Borrow maximum 3 books please drop any book and checkout again")
        return False

    def isvalid(self, user_id, book):

        checkouts = self.load_checkout()

        for checkout in checkouts:
            if checkout["user_id"] == user_id:
                for b in checkout["checkout_details"]:
                    if b["book_id"] == book["book_id"]:
                        print("Book Have Been Already Exists")
                        return False

        return True

    def add_book(self, user_id, book):

        if self.minimum_deposit(user_id) and self.maximum_books(user_id) and self.isvalid(user_id, book):

            checkouts = self.load_checkout()

            for user in checkouts:
                if user["user_id"] == user_id:
                    user["checkout_details"].append(book)
                    print("Added Book")

            self.save_checkout(checkouts)

            return True

    def return_book(self, user_id, book_id):

        checkouts = self.load_checkout()

        for user in checkouts:
            if user["user_id"] == user_id:

                for book in user["checkout_details"]:
                    if book["book_id"] == book_id:
                        book["return_date"] = self.return_details["return_date"]
                        print("Book Returned")

        self.save_checkout(checkouts)
        
