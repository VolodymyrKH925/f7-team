import re
from datetime import datetime

class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value: str):
        if type(value) != str:
            raise ValueError("Name value isn't correct")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value: str):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone value must contain 10 digits")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value: str):
        try:
            date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
    
class Email(Field):
    def __init__(self, value: str):
        if not self.is_valid_email(value):
            raise ValueError("Invalid email format")
        super().__init__(value)

    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

class Address(Field):
    def __init__(self, value: str):
        super().__init__(value)
