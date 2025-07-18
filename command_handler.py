from main import AddressBook, Record, Email


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Enter the current arguments for the command"
        except IndexError:
            return "Enter user name."
    return inner


@input_error
def add_contact(book: AddressBook):
    name = input('Enter contact name: ').strip()
    if not name:
        return "Name cannot be empty."
    record = book.find(name)

    if record is None:
        record = Record(name)
    
    while True:
        phone = input('Enter phone number (or press Enter to skip/stop): ').strip()
        if not phone:
            break
        try:
            record.add_phone(phone)
            print('Phone added')
        except ValueError as e:
                print(f"Invalid phone: {e}")
    
    email = prompt_validated_input(
        "Enter email (or press Enter to skip): ",
        lambda val: Email(val),
        "Invalid email format"
        )

    if email:
        record.email = email
    
    bday = input("Enter birthday (DD.MM.YYYY) (or press Enter to skip): ").strip()

    if bday:
        try:
            record.add_birthday(bday)
        except ValueError as e:
            print(f"Invalid birthday: {e}")
    
    address = input("Enter address (or press Enter to skip): ").strip()
    if address:
        record.add_address(address)
        print('Address added.')
    
    book.add_record(record)

    return f"Contact '{name}' added successfully!"


@input_error
def change_contact(args, book: AddressBook) -> str:
    *name_parts, old_number, new_number = args
    name = " ".join(name_parts)

    record = book.find(name)
    if record:
        record.edit_phone(old_number, new_number)
    
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook) ->str:
    name = " ".join(args)
    record = book.find(name)
    if record:
        return f"{record.name.value}, phones: {', '.join(p.value for p in record.phones)}"
    else:
        raise KeyError


@input_error
def add_birthday(args, book: AddressBook) :
    *name_parts, birthday = args
    name = " ".join(name_parts)

    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"{name}'s birthday added"
    else:
        raise KeyError

@input_error
def show_birthday(args, book: AddressBook):
    name = " ".join(args)

    record = book.find(name)

    if record:
        if record.birthday:
            return f"{name}'s birthday is on {record.birthday}"
        else:
            return f"{name}'s birthday has not been added"
    else:
        raise KeyError

@input_error
def birthdays(book: AddressBook):
    if not len(book):
        return "No contacts entered!"
    birthday_peoples = book.get_upcoming_birthdays()
    if len(birthday_peoples):
        return "\n".join(f"{bp['name']} - {bp['congratulation_date']}" for bp in birthday_peoples)
    else:
        return "There are no birthdays this week"

@input_error
def add_email(args, book: AddressBook):
    name = " ".join(args)

    record = book.find(name)
    if not record:
        raise KeyError
    
    email = prompt_validated_input("Enter email (or press Enter to cancel): ",
        lambda val: Email(val),
        "Invalid email format")
    
    if email:
        record.email = email
        return f"Email for {name} added: {email}"
    return "Email not added."


def prompt_validated_input(prompt_text, validator, error_message="Invalid input. Try again.", skip_allowed=True):
    while True:
        value = input(prompt_text).strip()
        if not value and skip_allowed:
            return None
        try:
            return validator(value)
        except ValueError as e:
            print(f"{error_message} ({e})")
            print("Try again or press Enter to skip.")

@input_error
def add_address(args, book: AddressBook):
    name = " ".join(args)
    if not name:
        raise KeyError
    
    record = book.find(name)

    if record:
        address = input("Enter address (or press Enter to skip): ").strip()
        if address:
            record.add_address(address)
            return 'Address added.'
        else:
            return 'Address skipped'
    else:
        raise KeyError