from addressbook.book import AddressBook
from addressbook.record import Record
from addressbook.fields import Email
from edit_contact import edit_contact
from delete import handle_delete
from prompt_toolkit import HTML, print_formatted_text


def input_error(error_message="Something went wrong"):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except (ValueError, IndexError, KeyError):
                return error_message
            
        return inner
    return decorator


@input_error()
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

    record.pretty_print()

    return f"Contact '{name}' added successfully!"

@input_error()
def change_contact(book: AddressBook):
    edit_contact(book)

@input_error("Usage: phone [name]")
def show_phone(args, book: AddressBook) ->str:
    name = " ".join(args)
    record = book.find(name)
    if record:
        return f"{record.name.value}, phones: {', '.join(p.value for p in record.phones)}"
    else:
        raise KeyError


@input_error("Usage: add-birthday [name] [DD.MM.YYYY]")
def add_birthday(args, book: AddressBook) :
    *name_parts, birthday = args
    name = " ".join(name_parts)

    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"{name}'s birthday added"
    else:
        raise KeyError

@input_error("Usage: show-birthday [name]")
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

@input_error("Usage: birthdays [days_ahead]")
def birthdays(args: int, book: AddressBook):
    days_ahead = int(args[0])
    if not len(book):
        print_formatted_text(HTML('<ansired>No contacts entered!</ansired>'))
        return

    birthday_peoples = book.get_upcoming_birthdays(days_ahead)
    if birthday_peoples:
        print_formatted_text(HTML('<ansiblue>Upcoming birthdays:</ansiblue>'))
        for bp in birthday_peoples:
            print_formatted_text(HTML(
                f"<ansigreen>{bp['name']}</ansigreen> - <ansiyellow>{bp['congratulation_date']}</ansiyellow>"
            ))
    else:
        print_formatted_text(HTML('<ansired>There are no birthdays this period</ansired>'))


@input_error("Usage: delete")
def delete_contact(book: AddressBook):
    handle_delete(book)
    
@input_error("Usage: add-email [name] [email]")
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

@input_error("Usage: add-address [name]")
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
