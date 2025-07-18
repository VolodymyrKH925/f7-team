from datetime import datetime
from typing import List, Dict

def get_upcoming_birthdays(users: List[Dict[str, str]], days_ahead: int) -> List[Dict[str, str]]:
    current_date = datetime.today().date()
    upcoming_birthdays = []

    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        birthday_this_year = birthday.replace(year=current_date.year)

        if birthday_this_year < current_date:
            birthday_this_year = birthday_this_year.replace(year=current_date.year + 1)

        days_until_birthday = (birthday_this_year - current_date).days

        print(f"{user['name']} → {birthday_this_year} → in {days_until_birthday} days")

        if days_until_birthday == days_ahead:
            upcoming_birthdays.append({
                "name": user["name"],
                "birthday": user["birthday"],
                "in_days": days_ahead,
                "congratulation_date": birthday_this_year.strftime("%Y.%m.%d")
            })

    return upcoming_birthdays


if __name__ == "__main__":
    users = [
        {"name": "Hanna", "birthday": "1995.07.20"},
        {"name": "Vova", "birthday": "1990.09.22"},
        {"name": "Vlad", "birthday": "1988.07.19"},
        {"name": "Yana", "birthday": "1992.11.17"},
    ]

    try:
        days_input = int(input("Enter the number of days in advance to check: "))
    except ValueError:
        print("Please enter a whole number.")
        exit(1)

    result = get_upcoming_birthdays(users, days_input)

    print("\nResult:")
    if result:
        for user in result:
            print(user)
    else:
        print("There are no users with birthdays in the specified number of days.")