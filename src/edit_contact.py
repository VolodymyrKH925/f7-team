from datetime import datetime
from addressbook.utils import save_data
from addressbook.book import AddressBook

def edit_contact(book: AddressBook):
    print("\n=== Contact Editing Mode ===")
    print("Type 'back' anytime to return to main menu.\n")

    while True:
        name = input("👤 Enter contact name to edit: ").strip()
        if name.lower() == "back":
            print("👋 Exiting editing mode.\n")
            break

        record = book.find(name)
        if not record:
            print(f"❌ Contact '{name}' not found.\n")
            continue

        print(f"\n✏️ Editing contact: {name}")
        show_fields_help()

        while True:
            field = input("📌 What do you want to edit? (or type 'show'): ").strip().lower()

            if field == "back":
                break

            if field == "show":
                show_fields_help()
                continue

            if field == "phone":
                phones_str = [str(phone) for phone in record.phones]
                if not phones_str:
                    print("📭 No phones to edit.")
                    new = input("📲 Enter new phone to add: ").strip()
                    record.add_phone(new)
                    save_data(book)
                    print("✅ Phone added.")
                    continue

                print(f"📞 Current phone(s):")
                for idx, phone in enumerate(phones_str, 1):
                    print(f"  {idx}. {phone}")

                if len(phones_str) == 1:
                    confirm = input(f"↪ Replace {phones_str[0]}? (y/n): ").strip().lower()
                    if confirm == "y":
                        new = input("📲 Enter new phone: ").strip()
                        record.edit_phone(phones_str[0], new)
                        save_data(book)
                        print("✅ Phone updated.")
                else:
                    choice = input("🔢 Enter number of phone to replace: ").strip()
                    if not choice.isdigit() or not (1 <= int(choice) <= len(phones_str)):
                        print("❌ Invalid choice.")
                        continue
                    old = phones_str[int(choice) - 1]
                    new = input("📲 Enter new phone: ").strip()
                    record.edit_phone(old, new)
                    save_data(book)
                    print("✅ Phone updated.")

            elif field == "email":
                current = str(record.email) if getattr(record, "email", None) else "None"
                print(f"📧 Current email: {current}")
                new = input("📩 Enter new email: ").strip()
                record.add_email(new)
                save_data(book)
                print("✅ Email updated.")

            elif field == "birthday":
                current = record.birthday.strftime("%d.%m.%Y") if record.birthday else "None"
                print(f"🎂 Current birthday: {current}")
                new = input("📆 Enter new birthday (DD.MM.YYYY): ").strip()
                try:
                    new_bday = datetime.strptime(new, "%d.%m.%Y").date()
                    record.add_birthday(new_bday)
                    save_data(book)
                    print("✅ Birthday updated.")
                except ValueError:
                    print("❌ Invalid date format. Please use DD.MM.YYYY.")

            elif field == "address":
                current = record.address if record.address else "None"
                print(f"🏠 Current address: {current}")
                address = input("📬 Enter new address: ").strip()
                record.address = address
                save_data(book)
                print("✅ Address updated.")

            else:
                print("❓ Unknown field. Try again or type 'show' to see available options.")

def show_fields_help():
    print("Available fields to edit:")
    print("  phone | email | birthday | address")
    print("  back - return to contact selection")
    print("  show - repeat this help\n")
