class Validators:
    def __init__(self):
        pass

    @staticmethod
    def email_validator(email):
        if "@" not in email or "admin" in email:
            print("Invalid Input or borrower cannot have mail id named Admin")
            return False
        return True

    @staticmethod
    def choice_validator(choice):
        if choice < 0 and choice > 4:
            print("Invalid Input or borrower cannot have choice")
            return False
        return True

