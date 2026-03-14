import json
from datetime import datetime, timedelta

MEMBERS_FILE = "data.json"
CHECKOUT_FILE = "checkout.json"
BOOKS_FILE = "books.json"

FINE_PER_DAY_BASE = 2
FINE_ESCALATION_DAYS = 10
CARD_LOST_FINE = 10
LOST_BOOK_FINE_PERCENT = 0.50
MIN_DEPOSIT = 500


class UserManagement:

    members_file = MEMBERS_FILE
    checkout_file = CHECKOUT_FILE
    books_file = BOOKS_FILE

    def __init__(self, user_id):
        self.user_id = user_id

    # ─── Loaders / Savers ────────────────────────────────────────────────────

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

    def save_books(self, data):
        with open(self.books_file, "w") as f:
            json.dump(data, f, indent=4)

    def get_user(self, user_id):
        for u in self.load_members():
            if u["user_id"] == user_id:
                return u
        return None

    def get_book(self, book_id):
        for b in self.load_books():
            if b["bookid"] == book_id:
                return b
        return None

    def get_checkout_record(self, user_id):
        for c in self.load_checkout():
            if c["user_id"] == user_id:
                return c
        return None

    # ─── Menu ────────────────────────────────────────────────────────────────

    @staticmethod
    def user_choice():
        print("\n--- Borrower Menu ---")
        print("1. View All Books")
        print("2. Search Book by Name or ISBN")
        print("3. Checkout Book")
        print("4. View My Borrowed Books")
        print("5. Return / Manage Book")
        print("6. View Fine & Borrow History")
        print("7. Report Card Lost")
        print("8. Logout")
        return input("Enter your choice: ").strip()

    # ─── View Books ──────────────────────────────────────────────────────────

    def view_books(self):
        books = self.load_books()
        if not books:
            print("No books available")
            return

        print("\n--- Available Books ---")
        print(f"{'ID':<6} {'Title':<45} {'Author':<25} {'ISBN':<16} {'Qty':<5}")
        print("-" * 100)
        for book in books:
            if book.get("quantity", 0) > 0:
                print(f"{book['bookid']:<6} {book.get('name','N/A'):<45} {book.get('authorname','N/A'):<25} {book.get('ISBN','N/A'):<16} {book.get('quantity','N/A'):<5}")

    # ─── Search Book ─────────────────────────────────────────────────────────

    def search_book(self):
        query = input("Enter Book Name or ISBN to search: ").strip().lower()
        books = self.load_books()
        results = [b for b in books if query in b.get("name", "").lower() or query == str(b.get("ISBN", ""))]
        if not results:
            print("No books found")
            return
        print(f"\n{'ID':<6} {'Title':<45} {'Author':<25} {'ISBN':<16} {'Qty':<5}")
        print("-" * 100)
        for book in results:
            print(f"{book['bookid']:<6} {book.get('name','N/A'):<45} {book.get('authorname','N/A'):<25} {book.get('ISBN','N/A'):<16} {book.get('quantity','N/A'):<5}")

    # ─── Validations ─────────────────────────────────────────────────────────

    def minimum_deposit(self, user_id):
        for user in self.load_members():
            if user["user_id"] == user_id and user["deposit"] >= MIN_DEPOSIT:
                return True
        print(f"Insufficient deposit. Minimum Rs.{MIN_DEPOSIT} required.")
        return False

    def maximum_books(self, user_id):
        record = self.get_checkout_record(user_id)
        if record and len(record["checkout_details"]) >= 3:
            print("You have already borrowed the maximum of 3 books.")
            return False
        return True

    def isvalid(self, user_id, book_id):
        record = self.get_checkout_record(user_id)
        if record:
            for b in record["checkout_details"]:
                if b["book_id"] == book_id:
                    print("You have already borrowed this book.")
                    return False
        return True

    def quantity_available(self, book_id):
        book = self.get_book(book_id)
        if not book:
            print("Book ID not found.")
            return False
        if book["quantity"] <= 0:
            print("Book not available (out of stock).")
            return False
        return True

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

    # ─── Checkout ────────────────────────────────────────────────────────────

    def add_book(self, user_id, book):
        book_id = book["book_id"]

        if not (self.minimum_deposit(user_id)
                and self.maximum_books(user_id)
                and self.isvalid(user_id, book_id)
                and self.quantity_available(book_id)):
            print("Book cannot be checked out.")
            return

        checkouts = self.load_checkout()
        checkout_date = datetime.today()
        book_details = {
            "book_id": book_id,
            "due_date": (checkout_date + timedelta(days=15)).strftime("%Y-%m-%d"),
            "return_date": "",
            "book_checkout_date": checkout_date.strftime("%Y-%m-%d"),
            "extensions": 0
        }

        user_found = False
        for user in checkouts:
            if user["user_id"] == user_id:
                user["checkout_details"].append(book_details)
                user_found = True
                break

        if not user_found:
            checkouts.append({"user_id": user_id, "checkout_details": [book_details]})

        self.save_checkout(checkouts)
        self.reduce_quantity(book_id)

        book_info = self.get_book(book_id)
        print(f"Book '{book_info.get('name', book_id)}' checked out successfully. Due: {book_details['due_date']}")

    # ─── View My Borrowed Books ───────────────────────────────────────────────

    def view_my_books(self, user_id):
        record = self.get_checkout_record(user_id)
        if not record or not record["checkout_details"]:
            print("You have no books currently borrowed.")
            return

        print(f"\n{'Book ID':<10} {'Title':<40} {'Checkout Date':<15} {'Due Date':<15} {'Extensions':<12}")
        print("-" * 95)
        for b in record["checkout_details"]:
            book_info = self.get_book(b["book_id"])
            title = book_info.get("name", "Unknown") if book_info else "Unknown"
            print(f"{b['book_id']:<10} {title:<40} {b['book_checkout_date']:<15} {b['due_date']:<15} {b.get('extensions', 0):<12}")

    # ─── Fine Calculation ─────────────────────────────────────────────────────

    def calculate_fine(self, due_date_str, return_date_str, book_cost=0):
        due = datetime.strptime(due_date_str, "%Y-%m-%d")
        ret = datetime.strptime(return_date_str, "%d/%m/%Y")
        days_late = (ret - due).days

        if days_late <= 0:
            return 0

        # Base: 2 Rs/day after 15 days
        fine = days_late * FINE_PER_DAY_BASE

        # Exponential escalation every 10 days
        escalation_periods = days_late // FINE_ESCALATION_DAYS
        for i in range(escalation_periods):
            fine += (i + 1) * FINE_PER_DAY_BASE * FINE_ESCALATION_DAYS

        # Cap at 80% of book cost if book_cost provided
        if book_cost > 0:
            cap = book_cost * 0.80
            fine = min(fine, cap)

        return round(fine, 2)

    # ─── Return / Manage Book ─────────────────────────────────────────────────

    def manage_book(self, user_id):
        self.view_my_books(user_id)
        record = self.get_checkout_record(user_id)
        if not record or not record["checkout_details"]:
            return

        try:
            book_id = int(input("Enter Book ID to manage: "))
        except ValueError:
            print("Invalid Book ID")
            return

        book_entry = None
        for b in record["checkout_details"]:
            if b["book_id"] == book_id:
                book_entry = b
                break

        if not book_entry:
            print("Book not found in your borrowed list.")
            return

        book_info = self.get_book(book_id)
        book_cost = book_info.get("cost", 500) if book_info else 500

        print("\nWhat would you like to do?")
        print("1. Return Book")
        print("2. Extend Tenure")
        print("3. Mark Book as Lost")
        print("4. Exchange Book")
        action = input("Enter choice: ").strip()

        if action == "1":
            self._return_book(user_id, book_id, book_entry, book_cost)
        elif action == "2":
            self._extend_tenure(user_id, book_id, book_entry)
        elif action == "3":
            self._mark_book_lost(user_id, book_id, book_entry, book_cost)
        elif action == "4":
            self._exchange_book(user_id, book_id, book_entry, book_cost)
        else:
            print("Invalid choice")

    def _get_return_date(self):
        while True:
            date_str = input("Enter return date (DD/MM/YYYY): ").strip()
            try:
                datetime.strptime(date_str, "%d/%m/%Y")
                return date_str
            except ValueError:
                print("Invalid date format. Use DD/MM/YYYY")

    def _apply_fine(self, user_id, fine_amount, reason):
        if fine_amount <= 0:
            return
        print(f"\nFine Amount: Rs.{fine_amount} | Reason: {reason}")
        print("Pay fine via:")
        print("1. Cash")
        print("2. Deduct from Security Deposit")
        pay_choice = input("Enter choice: ").strip()

        members = self.load_members()
        for user in members:
            if user["user_id"] == user_id:
                fine_record = {
                    "date": datetime.today().strftime("%Y-%m-%d"),
                    "amount": fine_amount,
                    "reason": reason,
                    "paid_via": "cash" if pay_choice == "1" else "deposit"
                }
                if "fine_history" not in user:
                    user["fine_history"] = []
                user["fine_history"].append(fine_record)

                if pay_choice == "2":
                    user["deposit"] -= fine_amount
                    print(f"Rs.{fine_amount} deducted from deposit. Remaining deposit: Rs.{user['deposit']}")
                else:
                    print(f"Please pay Rs.{fine_amount} at the counter.")
                break
        self.save_members(members)

    def _remove_from_checkout(self, user_id, book_id):
        checkouts = self.load_checkout()
        for user in checkouts:
            if user["user_id"] == user_id:
                user["checkout_details"] = [b for b in user["checkout_details"] if b["book_id"] != book_id]
        self.save_checkout(checkouts)

    def _add_borrow_history(self, user_id, book_id, checkout_date, return_date, fine, reason="returned"):
        members = self.load_members()
        book_info = self.get_book(book_id)
        for user in members:
            if user["user_id"] == user_id:
                if "borrow_history" not in user:
                    user["borrow_history"] = []
                user["borrow_history"].append({
                    "book_id": book_id,
                    "book_name": book_info.get("name", "Unknown") if book_info else "Unknown",
                    "checkout_date": checkout_date,
                    "return_date": return_date,
                    "fine": fine,
                    "status": reason
                })
                break
        self.save_members(members)

    def _return_book(self, user_id, book_id, book_entry, book_cost):
        return_date = self._get_return_date()
        fine = self.calculate_fine(book_entry["due_date"], return_date, book_cost)

        if fine > 0:
            self._apply_fine(user_id, fine, f"Late return of book ID {book_id}")
        else:
            print("No fine. Book returned on time.")

        self._add_borrow_history(user_id, book_id, book_entry["book_checkout_date"], return_date, fine, "returned")
        self._remove_from_checkout(user_id, book_id)
        self.increase_quantity(book_id)
        print("Book returned successfully.")

    def _extend_tenure(self, user_id, book_id, book_entry):
        extensions = book_entry.get("extensions", 0)
        if extensions >= 2:
            print("Cannot extend tenure. Maximum 2 extensions allowed.")
            return

        checkouts = self.load_checkout()
        for user in checkouts:
            if user["user_id"] == user_id:
                for b in user["checkout_details"]:
                    if b["book_id"] == book_id:
                        current_due = datetime.strptime(b["due_date"], "%Y-%m-%d")
                        new_due = current_due + timedelta(days=15)
                        b["due_date"] = new_due.strftime("%Y-%m-%d")
                        b["extensions"] = extensions + 1
                        print(f"Tenure extended. New due date: {b['due_date']} (Extension {b['extensions']}/2)")
                        break
        self.save_checkout(checkouts)

    def _mark_book_lost(self, user_id, book_id, book_entry, book_cost):
        fine = round(book_cost * LOST_BOOK_FINE_PERCENT, 2)
        self._apply_fine(user_id, fine, f"Lost book ID {book_id}")
        self._add_borrow_history(user_id, book_id, book_entry["book_checkout_date"],
                                  datetime.today().strftime("%d/%m/%Y"), fine, "lost")
        self._remove_from_checkout(user_id, book_id)
        print("Book marked as lost. Fine applied.")

    def _exchange_book(self, user_id, book_id, book_entry, book_cost):
        # First return the current book
        return_date = self._get_return_date()
        fine = self.calculate_fine(book_entry["due_date"], return_date, book_cost)
        if fine > 0:
            self._apply_fine(user_id, fine, f"Late return (exchange) of book ID {book_id}")

        self._add_borrow_history(user_id, book_id, book_entry["book_checkout_date"], return_date, fine, "exchanged")
        self._remove_from_checkout(user_id, book_id)
        self.increase_quantity(book_id)
        print("Book returned for exchange.")

        # Now checkout a new book
        self.view_books()
        try:
            new_book_id = int(input("Enter new Book ID to borrow: "))
            self.add_book(user_id, {"book_id": new_book_id})
        except ValueError:
            print("Invalid Book ID")

    # ─── Card Lost ───────────────────────────────────────────────────────────

    def report_card_lost(self, user_id):
        print(f"Card lost fine: Rs.{CARD_LOST_FINE}")
        self._apply_fine(user_id, CARD_LOST_FINE, "Membership card lost")
        print("Card loss reported. New card will be issued.")

    # ─── History ─────────────────────────────────────────────────────────────

    def view_history(self, user_id):
        user = self.get_user(user_id)
        if not user:
            print("User not found")
            return

        print("\n--- Borrow History ---")
        history = user.get("borrow_history", [])
        if not history:
            print("No borrow history found.")
        else:
            print(f"{'Book':<40} {'Checkout':<12} {'Return':<12} {'Fine':<8} {'Status':<10}")
            print("-" * 85)
            for h in history:
                print(f"{h.get('book_name','N/A'):<40} {h.get('checkout_date','N/A'):<12} {h.get('return_date','N/A'):<12} {h.get('fine',0):<8} {h.get('status','N/A'):<10}")

        print("\n--- Fine History ---")
        fines = user.get("fine_history", [])
        if not fines:
            print("No fine history found.")
        else:
            print(f"{'Date':<12} {'Amount':<10} {'Reason':<40} {'Paid Via':<10}")
            print("-" * 75)
            for f in fines:
                print(f"{f.get('date','N/A'):<12} Rs.{f.get('amount',0):<8} {f.get('reason','N/A'):<40} {f.get('paid_via','N/A'):<10}")

        print(f"\nCurrent Deposit Balance: Rs.{user.get('deposit', 0)}")
