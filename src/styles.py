from prompt_toolkit import print_formatted_text, HTML

def print_contact(contact):
    def safe(val):
        if isinstance(val, list):
            return ", ".join(val) if val else "-"
        if val is None or val == "":
            return "-"
        return str(val)

    rows = [
        ("Name", safe(contact.get("name")), "ansibrightblue"),
        ("Phones", safe(contact.get("phones")), "ansiyellow"),
        ("Email", safe(contact.get("email")), "ansibrightcyan"),
        ("Birthday", safe(contact.get("birthday")), "ansired"),
        ("Address", safe(contact.get("address")), "ansigreen"),
    ]

    max_key_len = max(len(label) for label, _, _ in rows)

    print_formatted_text(HTML("<ansiblue>" + "="*42 + "</ansiblue>"))
    for label, value, color in rows:
        print_formatted_text(HTML(
            f"<ansimagenta>{label:<{max_key_len}}</ansimagenta> : <{color}>{value}</{color}>"
        ))
    print_formatted_text(HTML("<ansiblue>" + "="*42 + "</ansiblue>"))


def print_note_colored(note_id: int, note):
    tags_str = ", ".join(note.tags) if note.tags else "No tags"

    print_formatted_text(HTML("<ansiblue>" + "="*50 + "</ansiblue>"))
    print_formatted_text(HTML(
        f"<ansimagenta><b>Note #{note_id}</b></ansimagenta>"
    ))
    print_formatted_text(HTML(
        f"<ansicyan>{note.text}</ansicyan>"
    ))
    print_formatted_text(HTML(
        f"<ansiyellow>{tags_str}</ansiyellow>"
    ))
    print_formatted_text(HTML("<ansiblue>" + "="*50 + "</ansiblue>\n"))