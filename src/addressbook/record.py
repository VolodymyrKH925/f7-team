from .fields import Name, Phone, Email, Birthday, Address
from styles import print_contact

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone_number: str):
        self.phones.append(Phone(phone_number))
    
    def remove_phone(self, phone_number: str):
        for phone in self.phones:
             if phone.value == phone_number:
                self.phones.remove(phone)
                return
        raise ValueError(f"Phone number {phone_number} not found")
    
    def edit_phone(self, old_phone: str, new_phone: str):
        new_phone_obj = Phone(new_phone)  # Валідуємо тут
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = new_phone_obj
                return
        raise ValueError(f"number {old_phone} not found")

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone.value
        raise ValueError("Value not found")
    
    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def get_next_birthday_date(self):
        if self.birthday:
            return self.birthday.value
        return None

    def remove_phone(self, phone_str: str):
        self.phones = [p for p in self.phones if str(p) != phone_str]

    def add_email(self, value):
        self.email = Email(value)

    def add_address(self, address):
        self.address = Address(address)

    def pretty_print(self):
        print()
        print_contact({
            "name": self.name.value,
            "phones": [phone.value for phone in self.phones],
            "email": getattr(self, "email", "No email"),
            "birthday": getattr(self, "birthday", "No birthday"),
            "address": getattr(self, "address", "No address"),
        })

    def __str__(self):
        parts = [f"Contact name: {self.name.value}"]

        if self.phones:
            parts.append("phones: " + "; ".join(p.value for p in self.phones))
        if self.email:
            parts.append(f"Email: {self.email}")
        if self.birthday:
            parts.append(f"Birthday: {self.birthday}")
        if self.address:
            parts.append(f"Address: {self.address}")

        return ', '.join(parts)
