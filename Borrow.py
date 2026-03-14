import json
import uuid

FILE = "data.json"


class Borrower:

    def __init__(self, username, password, admin=False, deposit=1500):
        self.username = username
        self.password = password
        self.admin = admin
        self.deposit = deposit

    def todict(self):
        return {
            "user_id": str(uuid.uuid4()),
            "username": self.username,
            "password": self.password,
            "admin": self.admin,
            "deposit": self.deposit,
            "fine_limit": 500,
            "borrow_history": [],
            "fine_history": []
        }

    def create_user(self):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
        except:
            data = []

        for user in data:
            if user["username"] == self.username:
                print("User already exists")
                return

        data.append(self.todict())

        with open(FILE, "w") as f:
            json.dump(data, f, indent=4)

        print("Account created successfully.")

    @staticmethod
    def load_users():
        try:
            with open(FILE, "r") as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def save_users(data):
        with open(FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def login(username, password):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)

            for user in data:
                if user["username"] == username and user["password"] == password:
                    print("Login successful.")
                    return {"admin": user["admin"], "user_id": user["user_id"]}

            print("Invalid credentials")
            return None

        except:
            print("No user data found")
            return None
