from main import AddressBook, Record


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
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook) -> str:
    name, old_number, new_number = args
    print(name, old_number, new_number)
    record = book.find(name)
    if record:
        record.edit_phone(old_number, new_number)
    
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook) ->str:
    name = args[0]
    record = book.find(name)
    if record:
        return f"{record.name.value}, phones: {', '.join(p.value for p in record.phones)}"
    else:
        raise KeyError


@input_error
def add_birthday(args, book: AddressBook) :
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"{name}'s birthday added"
    else:
        raise KeyError

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
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
