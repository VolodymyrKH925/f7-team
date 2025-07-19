from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text, HTML

COMMANDS = {
    "hello": "contact",
    "add": "contact",
    "change": "contact",
    "phone": "contact",
    "all": "contact",
    "delete": "contact",
    "search": "contact",
    "add-birthday": "contact",
    "show-birthday": "contact",
    "birthdays": "contact",
    "add-email": "contact",
    "add-address": "contact",
    "exit": "contact",
    "close": "contact",
    "help": "contact",

    "add-note": "note",
    "delete-note": "note",
    "search-note-tag": "note",
    "show-notes": "note",
    "edit-note": "note",
    "sort-by-tag": "note",
}

def show_help():
    contact_commands = [cmd for cmd, cat in COMMANDS.items() if cat == "contact"]
    note_commands = [cmd for cmd, cat in COMMANDS.items() if cat == "note"]

    max_len = max(len(contact_commands), len(note_commands))
    contact_commands += [""] * (max_len - len(contact_commands))
    note_commands += [""] * (max_len - len(note_commands))

    print_formatted_text(HTML("<skyblue>\n" + "="*50 + "</skyblue>"))
    print_formatted_text(HTML("<b><ansiyellow>📒 Contacts</ansiyellow></b>           "
                              "<b><ansimagenta>   📝 Notes</ansimagenta></b>"))
    print_formatted_text(HTML("<skyblue>" + "-"*50 + "</skyblue>"))

    for left, right in zip(contact_commands, note_commands):
        left_col = f"<ansiyellow>{left:<25}</ansiyellow>" if left else ""
        right_col = f"<ansimagenta>{right}</ansimagenta>" if right else ""
        print_formatted_text(HTML(f"{left_col}{right_col}"))

    print_formatted_text(HTML("<skyblue>" + "="*50 + "</skyblue>\n"))

class CommandCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lower()
        for cmd in COMMANDS:
            if cmd.startswith(text):
                yield Completion(cmd, start_position=-len(text))

style = Style.from_dict({
    'prompt': '#00aa00 bold',
})