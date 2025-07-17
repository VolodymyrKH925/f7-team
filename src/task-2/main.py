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

        print(f"{user['name']} → {birthday_this_year} → через {days_until_birthday} днів")

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
        {"name": "Анна", "birthday": "1995.07.20"},
        {"name": "Ігор", "birthday": "1990.09.22"},
        {"name": "Олена", "birthday": "1988.07.19"},
        {"name": "Марко", "birthday": "1992.11.17"},
    ]

    try:
        days_input = int(input("Введіть кількість днів наперед для перевірки: "))
    except ValueError:
        print("Будь ласка, введіть ціле число.")
        exit(1)

    result = get_upcoming_birthdays(users, days_input)

    print("\nРезультат:")
    if result:
        for user in result:
            print(user)
    else:
        print("Немає користувачів з днем народження через задану кількість днів.")