from addressbook.book import AddressBook
import command_handler as handler
import pickle
from notes import *
from autocomplete import CommandCompleter, show_help
from prompt_toolkit import prompt
from addressbook.utils import save_data

# from typing import List, Dict
from search_contacts import (
    search_contacts_by_name,
    search_contacts_by_phone,
    search_contacts_by_email,
    search_contacts_by_birthday,
    search_contacts_by_address,
)

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

    completer = CommandCompleter()

    print("Welcome to the assistant bot!")
    while True:
        user_input = None
        while not user_input or not user_input.strip(): 
            user_input = prompt("Enter a command: ", completer=completer)

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "help":
            show_help()

        elif command == "add":
            print(handler.add_contact(book))

        elif command == "change":
            handler.change_contact(book)          

        elif command == "phone":
            print(handler.show_phone(args, book))

        elif command == "all":
            if not len(book):
                print("No contacts entered!")
            else:
                for record in book.values():
                    record.pretty_print()

        elif command == "delete":
            handler.delete_contact(book)         

        elif command == "search":
            search_menu(book)

        elif command == "add-birthday":
            print(handler.add_birthday(args, book))

        elif command == "show-birthday":
            print(handler.show_birthday(args, book))

        elif command == "birthdays":
            handler.birthdays(args, book)

        elif command == "add-email":
            print(handler.add_email(args, book))

        elif command == "add-address":
            print(handler.add_address(args, book))

        # notes commands
        
        elif command == "add-note":
            print(add_note(args, notes))

        elif command == "delete-note":
            print(delete_note(args, notes))

        elif command == "show-notes":
            print(show_notes(notes))

        elif command == "edit-note":
            print(edit_note(args, notes))

        elif command == "search-note-tag":
            print(search_note_tag(args, notes))
        
        elif command == "search-note-text":
            search_note_text(args, notes)

        elif command == "sort-by-tag":
            print(sort_by_tag(notes))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()