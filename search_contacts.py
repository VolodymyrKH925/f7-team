from datetime import datetime
def _get_value(attr):
    # Утиліта: якщо атрибут має .value, повернути його, інакше сам атрибут
    return attr.value if hasattr(attr, 'value') else attr

def search_contacts_by_name(query, contacts):
    query = query.lower()
    results = []
    for record in contacts.values():
        name = _get_value(record.name)
        if query in name.lower():
            results.append(record)
    return results

def search_contacts_by_phone(query, contacts):
    query = query.lower()
    results = []
    for record in contacts.values():
        for phone in record.phones:
            phone_val = _get_value(phone)
            if query in phone_val.lower():
                results.append(record)
                break
    return results

def search_contacts_by_email(query, contacts):
    query = query.lower()
    results = []
    for record in contacts.values():
        if hasattr(record, 'email') and record.email:
            email = _get_value(record.email)
            if query in email.lower():
                results.append(record)
    return results

def search_contacts_by_birthday(query, contacts):
    # Очікуємо query у форматі "dd.mm.yyyy"
    try:
        query_date = datetime.strptime(query, "%d.%m.%Y").date()
    except ValueError:
        print("⚠️ Invalid birthday format. Please use DD.MM.YYYY")
        return []

    results = []
    for record in contacts.values():
        if hasattr(record, 'birthday') and record.birthday:
            bd = _get_value(record.birthday)
            # Якщо bd - datetime.date або datetime.datetime
            bd_date = bd if isinstance(bd, datetime) else bd
            if isinstance(bd_date, datetime):
                bd_date = bd_date.date()
            if bd_date == query_date:
                results.append(record)
    return results

def search_contacts_by_address(query, contacts):
    query = query.lower()
    results = []
    for record in contacts.values():
        if hasattr(record, 'address') and record.address:
            address = record.address
            # Припускаємо, що address - словник (наприклад, {"city":..., "street":...})
            for value in address.values() if isinstance(address, dict) else [address]:
                val_str = _get_value(value)
                if val_str and query in str(val_str).lower():
                    results.append(record)
                    break
    return results
