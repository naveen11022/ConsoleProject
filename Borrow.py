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
            "id": str(uuid.uuid4()),
            "username": self.username,
            "password": self.password,
            "admin": self.admin,
            "deposit": self.deposit
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
    def login(username, password):

        try:
            with open(FILE, "r") as f:
                data = json.load(f)

            for user in data:
                if user["username"] == username and user["password"] == password:
                    print("Login successful.")
                    return {"admin": user["admin"], "user_id": user["user_id"]}

            print("User does not exist")
            return None

        except:
            print("No user data found")
            return None