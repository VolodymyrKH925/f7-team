from collections import UserDict
from .record import Record
from datetime import datetime
from addressbook.utils import autosave_contacts

class AddressBook(UserDict):

    @autosave_contacts
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
    
    def get_upcoming_birthdays(self, days_ahead: int):
        today = datetime.today().date()
        result = []
        for record in self.data.values():
            next_bday = record.get_next_birthday_date()
            if not next_bday:
                continue
            days_until = (next_bday - today).days
            if days_until == days_ahead:
                result.append({
                    "name": record.name.value,
                    "birthday": record.birthday.value.strftime("%d.%m.%Y"),
                    "in_days": days_ahead,
                    "congratulation_date": next_bday.strftime("%d.%m.%Y")
                })
        return result
