# AddressBook Bot

## 🧾 Description

This command-line bot helps you manage your contacts, notes, and birthdays. It features:

- Contact storage with names, phone numbers, emails
- Notes with tags and text search
- Birthday reminders
- Beautiful colored terminal output using `prompt_toolkit`

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your_username/your_repository.git
cd your_repository
```

### 2. Create and Activate a Virtual Environment
```bash
<details> <summary>macOS / Linux</summary>

python3 -m venv venv
source venv/bin/activate
</details> <details> <summary>Windows</summary>

python -m venv venv
venv\Scripts\activate
</details>
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

▶️ Running the Application

```bash
python src/main.py
```

## 💡 Usage
After launching, use the following commands:

🔹 Contact Management
add-contact [name] [phone] [email] — Add a new contact

delete-contact [name] — Delete a contact

edit-contact [name] [field] [new_value] — Edit a contact's field

🔹 Notes
add-note [text] #[tag] — Add a note with an optional tag

search-note-text [text] — Search notes by content

search-note-tag #[tag] — Search notes by tag

🔹 Birthdays
birthdays [days_ahead] — Show upcoming birthdays within the next X days

🔹 Other Commands
help — Show help message

exit — Exit the program

## 📌 Example Session
bash

> add-contact Alice +380501234567 alice@email.com
Contact Alice added.

> birthdays 7
Upcoming birthdays:
Alice - 2025-07-22

> search-note-text project
Note #2
Finish project plan
Tags: work, project

> exit
Goodbye!


## ⚙️ Technical Details
Language: Python 3

CLI Interface: prompt_toolkit for styled terminal output

Architecture: Modular structure using classes like AddressBook, Note, etc.
