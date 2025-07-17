from collections import UserDict
from datetime import datetime, timedelta
import command_handler as handler
import pickle
from notes import *
from search_contacts import (
    search_contacts_by_name,
    search_contacts_by_phone,
    search_contacts_by_email,
    search_contacts_by_birthday,
    search_contacts_by_address,
)
class Field:
    def __init__(self, value):
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
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        # додано
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

     # додано
    def add_email(self, email: str):
        self.email = email
    def add_address(self, address: str):
        self.address = address            

    def __str__(self):
        # return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        return(
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join(p.value for p in self.phones)}"
            f"{', email: ' + self.email if self.email else ''}"
            f"{', birthday: ' + str(self.birthday) if self.birthday else ''}"
            f"{', address: ' + self.address if self.address else ''}"
        )

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name: str):
        if name in self.data:
            self.data.pop(name)
            return
        raise KeyError(f"Contact '{name}' not found")
    
    def get_upcoming_birthdays(self):
        this_week_birthdays = []
        today = datetime.today().date()

        for user in self.data.values():
            if not user.birthday:
                continue

            birthday_this_year = user.birthday.value.replace(year=today.year).date()
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            
            delta = birthday_this_year - today

            if timedelta(days=0) <= delta <= timedelta(days=7):
                if birthday_this_year.weekday() > 4:
                    weekend_delta = 7 - birthday_this_year.weekday()
                    birthday_this_year = birthday_this_year + timedelta(days = weekend_delta)
                
                this_week_birthdays.append({
                    "name": user.name.value,
                    "congratulation_date": birthday_this_year.strftime("%d.%m.%Y")
                })
        return this_week_birthdays

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

 # Пошук у книзі контактів
def print_record(record):
    print(f"\n👤 {record.name}")
    print(f"📞 Phones: {', '.join(p.value for p in record.phones)}")
    print(f"📧 Email: {record.email if record.email else '-'}")
    print(f"🎂 Birthday: {record.birthday if record.birthday else '-'}")
    print(f"🏡 Address: {record.address if record.address else '-'}")
    print("-" * 30)

def search_menu(book):
    while True:
        print("\n🔍 Search by:")
        print("  name | phone | email | birthday | address")
        print("  back - to return")

        command = input("🔎 Enter search type: ").strip().lower()

        if command == "name":
            query = input("🔤 Enter name: ")
            results = search_contacts_by_name(query, book.data)
        elif command == "phone":
            query = input("📞 Enter phone: ")
            results = search_contacts_by_phone(query, book.data)
        elif command == "email":
            query = input("📧 Enter email: ")
            results = search_contacts_by_email(query, book.data)
        elif command == "birthday":
            query = input("🎂 Enter birthday (dd.mm): ")
            results = search_contacts_by_birthday(query, book.data)
        elif command == "address":
            query = input("🏘 Enter address part: ")
            results = search_contacts_by_address(query, book.data)
        elif command == "back":
            break
        else:
            print("⚠️ Unknown search type.")
            continue

        if results:
            print(f"\n✅ Found {len(results)} contact(s):")
            for r in results:
                print_record(r)
        else:
            print("❌ No matches found.")


def main():
    book = load_data()
    # load notes
    notes = load_data_notes()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break

        elif command == "hello":
            print("How can I help you?")

        # elif command == "add":
        #     print(handler.add_contact(args, book))
        elif command == "add":
            if len(args) < 2:
                print("❌ Please provide at least name and phone. Example: add John 1234567890 [email] [address]")
                continue

            name = args[0]
            phone = args[1]
            email = args[2] if len(args) > 2 else None
            address = args[3] if len(args) > 3 else None

            try:
                record = Record(name)
                record.add_phone(phone)
                if email:
                    record.add_email(email)
                if address:
                   record.add_address(address)
                book.add_record(record)
                print(f"✅ Contact '{name}' added.")
            except ValueError as e:
                print(f"⚠️ Error: {e}")


        elif command == "change":
            print(handler.change_contact(args, book))

        elif command == "phone":
            print(handler.show_phone(args, book))

        elif command == "all":
            if not len(book):
                print("No contacts entered!")
            else:
                for record in book.values():
                    print(record)

        elif command == "add-birthday":
            print(handler.add_birthday(args, book))

        elif command == "show-birthday":
            print(handler.show_birthday(args, book))

        elif command == "birthdays":
            print(handler.birthdays(book))

        # search command
        elif command == "search":
            search_menu(book)  

        # notes commands
        
        elif command == "add-note":
            print(add_note(args, notes))

        elif command == "delete-note":
            print(delete_note(args, notes))

        elif command == "search-note-tag":
            print(search_note_tag(args, notes))

        elif command == "show-notes":
            print(show_notes(notes))

        elif command == "edit-note":
            print(edit_note(args, notes))

        elif command == "search-note-tag":
            print(search_note_tag(args, notes))

        elif command == "sort-by-tag":
            print(sort_by_tag(notes))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()