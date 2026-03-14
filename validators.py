class Validators:
    def __init__(self):
        pass

    @staticmethod
    def email_validator(email):
        if "@" not in email:
            print("Invalid Email format")
            return False
        return True

    @staticmethod
    def choice_validator(choice, max_val):
        if choice < 1 or choice > max_val:
            print("Invalid choice")
            return False
        return True

    @staticmethod
    def date_validator(date_str):
        from datetime import datetime
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            print("Invalid date format. Use DD/MM/YYYY")
            return False
