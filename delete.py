from main import AddressBook, save_data

def handle_delete(book: AddressBook):
    print("\n=== Delete Contact Mode ===")
    print("Type 'back' anytime to return to the main menu.\n")

    while True:
        name = input("🔎 Enter contact name to delete: ").strip()
        if name.lower() == "back":
            print("👋 Exiting delete mode.\n")
            break

        record = book.find(name)
        if not record:
            print(f"❌ Contact '{name}' not found.\n")
            continue

        print(f"\n🗑️ Contact: {name}")
        print_delete_options()

        while True:
            choice = input("🔘 Choose an option (or type 'show'): ").strip().lower()

            if choice == "show":
                print_delete_options()
                continue
            elif choice == "back":
                break
            elif choice == "all":
                confirm = input(f"⚠️ Delete ALL data for '{name}'? (y/n): ").strip().lower()
                if confirm == "y":
                    book.delete(name)
                    save_data(book)
                    print("✅ Contact deleted.\n")
                    break
            elif choice == "phone":
                if not record.phones:
                    print("📭 No phone numbers found.")
                    continue
                print("📞 Phone numbers:")
                for idx, phone in enumerate(record.phones, 1):
                    print(f"  {idx}. {phone}")
                to_delete = input("🔢 Enter number to delete: ").strip()
                if to_delete.isdigit() and 1 <= int(to_delete) <= len(record.phones):
                    deleted = record.phones.pop(int(to_delete) - 1)
                    save_data(book)
                    print(f"✅ Phone '{deleted}' deleted.")
                else:
                    print("❌ Invalid choice.")
            elif choice == "email":
                if not record.email:
                    print("📭 No emails found.")
                    continue
                if isinstance(record.email, list):
                    for idx, email in enumerate(record.email, 1):
                        print(f"  {idx}. {email}")
                    to_delete = input("🔢 Enter number to delete: ").strip()
                    if to_delete.isdigit() and 1 <= int(to_delete) <= len(record.email):
                        deleted = record.email.pop(int(to_delete) - 1)
                        save_data(book)
                        print(f"✅ Email '{deleted}' deleted.")
                    else:
                        print("❌ Invalid choice.")
                else:
                    confirm = input(f"⚠️ Delete email '{record.email}'? (y/n): ").strip().lower()
                    if confirm == "y":
                        record.email = None
                        save_data(book)
                        print("✅ Email deleted.")
            elif choice == "birthday":
                if not record.birthday:
                    print("📭 No birthday found.")
                    continue
                confirm = input(f"⚠️ Delete birthday '{record.birthday}'? (y/n): ").strip().lower()
                if confirm == "y":
                    record.birthday = None
                    save_data(book)
                    print("✅ Birthday deleted.")
            elif choice == "address":
                if not record.address:
                    print("📭 No address found.")
                    continue
                confirm = input(f"⚠️ Delete address '{record.address}'? (y/n): ").strip().lower()
                if confirm == "y":
                    record.address = {}
                    save_data(book)
                    print("✅ Address deleted.")
            else:
                print("❓ Unknown option. Type a number 1-6 or 'show'.")

def print_delete_options():
    print("Available options to delete:")
    print("  all | phone | email | birthday | address")
    print("  back - return to contact selection")
    print("  show - repeat this help\n")


   
