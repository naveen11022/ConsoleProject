import json
import uuid
from datetime import datetime

BOOKS_FILE = "books.json"
MEMBERS_FILE = "data.json"
CHECKOUT_FILE = "checkout.json"


class Admin:

    def __init__(self, user_id):
        self.user_id = user_id

    # ─── Loaders / Savers ────────────────────────────────────────────────────

    def load_books(self):
        try:
            with open(BOOKS_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    def save_books(self, data):
        with open(BOOKS_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_members(self):
        try:
            with open(MEMBERS_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    def save_members(self, data):
        with open(MEMBERS_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_checkout(self):
        try:
            with open(CHECKOUT_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    # ─── Menu ────────────────────────────────────────────────────────────────

    @staticmethod
    def admin_choice():
        print("\n--- Admin Menu ---")
        print("1.  Add Book")
        print("2.  Remove Book")
        print("3.  Modify Book")
        print("4.  List Books (sorted)")
        print("5.  Search Book")
        print("6.  Add Borrower")
        print("7.  Add Admin")
        print("8.  Promote Existing User to Admin")
        print("9.  Manage Borrower Fine Limit")
        print("10. View All Borrowers")
        print("11. Reports")
        print("12. Logout")
        return input("Enter your choice: ").strip()

    # ─── Book Management ─────────────────────────────────────────────────────

    def add_book(self):
        books = self.load_books()
        existing_ids = [b["bookid"] for b in books]

        try:
            book_id = int(input("Enter Book ID: "))
        except ValueError:
            print("Invalid Book ID")
            return

        if book_id in existing_ids:
            print("Book ID already exists.")
            return

        name = input("Enter Book Name: ").strip()
        isbn = input("Enter ISBN: ").strip()
        author = input("Enter Author Name: ").strip()
        dop = input("Enter Date of Publication (YYYY-MM-DD): ").strip()

        try:
            quantity = int(input("Enter Quantity: "))
            cost = float(input("Enter Book Cost (Rs.): "))
        except ValueError:
            print("Invalid quantity or cost")
            return

        book = {
            "bookid": book_id,
            "name": name,
            "ISBN": isbn,
            "authorname": author,
            "DOP": dop,
            "quantity": quantity,
            "cost": cost,
            "borrow_count": 0
        }
        books.append(book)
        self.save_books(books)
        print(f"Book '{name}' added successfully.")

    def remove_book(self):
        books = self.load_books()
        try:
            book_id = int(input("Enter Book ID to remove: "))
        except ValueError:
            print("Invalid Book ID")
            return

        updated = [b for b in books if b["bookid"] != book_id]
        if len(updated) == len(books):
            print("Book ID not found.")
            return

        self.save_books(updated)
        print(f"Book ID {book_id} removed.")

    def modify_book(self):
        books = self.load_books()
        try:
            book_id = int(input("Enter Book ID to modify: "))
        except ValueError:
            print("Invalid Book ID")
            return

        for book in books:
            if book["bookid"] == book_id:
                print(f"Current Name: {book.get('name')}")
                print(f"Current Quantity: {book.get('quantity')}")
                print(f"Current Cost: {book.get('cost', 'N/A')}")
                print(f"Current Author: {book.get('authorname')}")

                print("\nWhat to modify?")
                print("1. Name")
                print("2. Quantity")
                print("3. Cost")
                print("4. Author")
                print("5. All")
                mod = input("Choice: ").strip()

                if mod in ("1", "5"):
                    book["name"] = input("New Name: ").strip() or book["name"]
                if mod in ("2", "5"):
                    try:
                        book["quantity"] = int(input("New Quantity: "))
                    except ValueError:
                        print("Invalid quantity, skipping.")
                if mod in ("3", "5"):
                    try:
                        book["cost"] = float(input("New Cost: "))
                    except ValueError:
                        print("Invalid cost, skipping.")
                if mod in ("4", "5"):
                    book["authorname"] = input("New Author: ").strip() or book["authorname"]

                self.save_books(books)
                print("Book updated successfully.")
                return

        print("Book ID not found.")

    def list_books(self):
        books = self.load_books()
        if not books:
            print("No books found.")
            return

        print("Sort by: 1. Name  2. Available Quantity")
        sort_choice = input("Choice: ").strip()

        if sort_choice == "1":
            books = sorted(books, key=lambda b: b.get("name", "").lower())
        elif sort_choice == "2":
            books = sorted(books, key=lambda b: b.get("quantity", 0))
        else:
            print("Invalid sort choice, showing unsorted.")

        print(f"\n{'ID':<6} {'Title':<45} {'Author':<25} {'ISBN':<16} {'Qty':<5} {'Cost':<8}")
        print("-" * 108)
        for book in books:
            print(f"{book['bookid']:<6} {book.get('name','N/A'):<45} {book.get('authorname','N/A'):<25} "
                  f"{book.get('ISBN','N/A'):<16} {book.get('quantity','N/A'):<5} {book.get('cost','N/A'):<8}")

    def search_book(self):
        query = input("Enter Book Name or ISBN to search: ").strip().lower()
        books = self.load_books()
        results = [b for b in books if query in b.get("name", "").lower() or query == str(b.get("ISBN", ""))]

        if not results:
            print("No books found.")
            return

        print(f"\n{'ID':<6} {'Title':<45} {'Author':<25} {'ISBN':<16} {'Qty':<5} {'Cost':<8}")
        print("-" * 108)
        for book in results:
            print(f"{book['bookid']:<6} {book.get('name','N/A'):<45} {book.get('authorname','N/A'):<25} "
                  f"{book.get('ISBN','N/A'):<16} {book.get('quantity','N/A'):<5} {book.get('cost','N/A'):<8}")

    # ─── User Management ─────────────────────────────────────────────────────

    def add_borrower(self):
        from Borrow import Borrower
        email = input("Enter Borrower Email: ").strip()
        if "@" not in email:
            print("Invalid email.")
            return
        password = input("Enter Password: ").strip()
        user = Borrower(email, password, admin=False)
        user.create_user()

    def add_admin(self):
        from Borrow import Borrower
        email = input("Enter Admin Email: ").strip()
        password = input("Enter Password: ").strip()
        user = Borrower(email, password, admin=True)
        user.create_user()

    def promote_to_admin(self):
        email = input("Enter Borrower Email to promote: ").strip()
        members = self.load_members()
        for user in members:
            if user["username"] == email:
                user["admin"] = True
                self.save_members(members)
                print(f"{email} promoted to Admin.")
                return
        print("User not found.")

    def manage_fine_limit(self):
        email = input("Enter Borrower Email: ").strip()
        members = self.load_members()
        for user in members:
            if user["username"] == email:
                print(f"Current fine limit: Rs.{user.get('fine_limit', 500)}")
                try:
                    new_limit = float(input("Enter new fine limit: "))
                    user["fine_limit"] = new_limit
                    self.save_members(members)
                    print("Fine limit updated.")
                except ValueError:
                    print("Invalid amount.")
                return
        print("User not found.")

    def view_all_borrowers(self):
        members = self.load_members()
        borrowers = [u for u in members if not u.get("admin", False)]
        if not borrowers:
            print("No borrowers found.")
            return

        print(f"\n{'Email':<35} {'Deposit':<10} {'Fine Limit':<12} {'Admin':<6}")
        print("-" * 65)
        for u in borrowers:
            print(f"{u.get('username','N/A'):<35} Rs.{u.get('deposit',0):<8} Rs.{u.get('fine_limit',500):<10} {str(u.get('admin',False)):<6}")

    # ─── Reports ─────────────────────────────────────────────────────────────

    def reports_menu(self):
        while True:
            print("\n--- Reports ---")
            print("1. Books with low quantity (need refill)")
            print("2. Books never borrowed")
            print("3. Heavily borrowed books")
            print("4. Students with outstanding (unreturned) books as on date")
            print("5. Status of a book by ISBN")
            print("6. Back")
            r = input("Choice: ").strip()

            if r == "1":
                self.report_low_quantity()
            elif r == "2":
                self.report_never_borrowed()
            elif r == "3":
                self.report_heavily_borrowed()
            elif r == "4":
                self.report_outstanding_books()
            elif r == "5":
                self.report_book_status_by_isbn()
            elif r == "6":
                break
            else:
                print("Invalid choice")

    def report_low_quantity(self):
        try:
            threshold = int(input("Enter low quantity threshold (default 3): ") or "3")
        except ValueError:
            threshold = 3

        books = self.load_books()
        low = [b for b in books if b.get("quantity", 0) <= threshold]
        if not low:
            print("All books have sufficient quantity.")
            return

        print(f"\n--- Books with quantity <= {threshold} ---")
        print(f"{'ID':<6} {'Title':<45} {'Qty':<5}")
        print("-" * 58)
        for b in low:
            print(f"{b['bookid']:<6} {b.get('name','N/A'):<45} {b.get('quantity',0):<5}")

    def report_never_borrowed(self):
        checkouts = self.load_checkout()
        borrowed_ids = set()
        for c in checkouts:
            for b in c.get("checkout_details", []):
                borrowed_ids.add(b["book_id"])

        members = self.load_members()
        for u in members:
            for h in u.get("borrow_history", []):
                borrowed_ids.add(h["book_id"])

        books = self.load_books()
        never = [b for b in books if b["bookid"] not in borrowed_ids]

        if not never:
            print("All books have been borrowed at least once.")
            return

        print("\n--- Books Never Borrowed ---")
        print(f"{'ID':<6} {'Title':<45} {'Qty':<5}")
        print("-" * 58)
        for b in never:
            print(f"{b['bookid']:<6} {b.get('name','N/A'):<45} {b.get('quantity',0):<5}")

    def report_heavily_borrowed(self):
        books = self.load_books()
        checkouts = self.load_checkout()
        members = self.load_members()

        borrow_count = {b["bookid"]: b.get("borrow_count", 0) for b in books}

        # Count from active checkouts
        for c in checkouts:
            for b in c.get("checkout_details", []):
                borrow_count[b["book_id"]] = borrow_count.get(b["book_id"], 0) + 1

        # Count from history
        for u in members:
            for h in u.get("borrow_history", []):
                borrow_count[h["book_id"]] = borrow_count.get(h["book_id"], 0) + 1

        sorted_books = sorted(books, key=lambda b: borrow_count.get(b["bookid"], 0), reverse=True)

        print("\n--- Heavily Borrowed Books ---")
        print(f"{'ID':<6} {'Title':<45} {'Borrow Count':<14}")
        print("-" * 67)
        for b in sorted_books[:10]:
            count = borrow_count.get(b["bookid"], 0)
            if count > 0:
                print(f"{b['bookid']:<6} {b.get('name','N/A'):<45} {count:<14}")

    def report_outstanding_books(self):
        date_str = input("Enter date (DD/MM/YYYY): ").strip()
        try:
            as_on = datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            print("Invalid date format.")
            return

        checkouts = self.load_checkout()
        members = self.load_members()
        member_map = {u["user_id"]: u["username"] for u in members}

        print(f"\n--- Students with unreturned books as on {date_str} ---")
        print(f"{'Student':<35} {'Book ID':<10} {'Checkout Date':<15} {'Due Date':<12}")
        print("-" * 75)

        found = False
        for c in checkouts:
            for b in c.get("checkout_details", []):
                checkout_dt = datetime.strptime(b["book_checkout_date"], "%Y-%m-%d")
                if checkout_dt <= as_on and not b.get("return_date"):
                    email = member_map.get(c["user_id"], "Unknown")
                    print(f"{email:<35} {b['book_id']:<10} {b['book_checkout_date']:<15} {b['due_date']:<12}")
                    found = True

        if not found:
            print("No outstanding books found for this date.")

    def report_book_status_by_isbn(self):
        isbn = input("Enter ISBN: ").strip()
        books = self.load_books()
        book = next((b for b in books if str(b.get("ISBN", "")) == isbn), None)

        if not book:
            print("Book not found.")
            return

        print(f"\n--- Book Status ---")
        print(f"Title   : {book.get('name')}")
        print(f"Author  : {book.get('authorname')}")
        print(f"ISBN    : {book.get('ISBN')}")
        print(f"Quantity: {book.get('quantity')}")
        print(f"Cost    : Rs.{book.get('cost', 'N/A')}")

        checkouts = self.load_checkout()
        members = self.load_members()
        member_map = {u["user_id"]: u["username"] for u in members}

        print("\nCurrently borrowed by:")
        found = False
        for c in checkouts:
            for b in c.get("checkout_details", []):
                if b["book_id"] == book["bookid"]:
                    email = member_map.get(c["user_id"], "Unknown")
                    due = b.get("due_date", "N/A")
                    print(f"  Student : {email}")
                    print(f"  Due Date: {due}")
                    found = True

        if not found:
            print("  This book is currently available in the rack.")
