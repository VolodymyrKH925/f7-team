from collections import UserDict
from prompt_toolkit import prompt
import pickle

def save_data_notes(notes, filename="notes.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(notes, f)

def load_data_notes(filename="notes.pkl"):
    try:
        with open(filename, "rb") as f:
            notes = pickle.load(f)
            return notes
    except FileNotFoundError:
        return NoteBook()

class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []

    def __str__(self):
        tag_str = ", ".join(self.tags)
        return f"Note: {self.text} | Tags: {tag_str}"
    
    
def autosave_notes(method):
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        save_data_notes(self)
        return result
    return wrapper

class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self.note_id = 1

    @autosave_notes
    def add_note(self, note: Note):
        self.data[self.note_id] = note
        self.note_id += 1

    @autosave_notes
    def delete_note(self, note_id: int):
        if note_id in self.data:
            del self.data[note_id]
        else:
            raise KeyError("Note ID not found")

    @autosave_notes
    def edit_note(self, note_id: int):
        if note_id not in self.data:
            raise KeyError("Note ID not found")

        note = self.data[note_id]

        new_text = prompt("Edit previous text: ", default=note.text).strip()

        if new_text:
            note.text = new_text
            
        current_tags_str = ", ".join(note.tags)
        new_tags_input = prompt("Edit tags: ", default=current_tags_str).strip()

        if new_tags_input != current_tags_str:
            new_tags = [tag.strip() for tag in new_tags_input.split(",") if tag.strip()]
            note.tags = new_tags

    def find_by_tag(self, tag: str):
        return [f"{note_id}: {note}" for note_id, note in self.data.items() if tag in note.tags]

    
    def sort_by_tags(self):

        tagged_notes = []
        for note_id, note in self.data.items():
            if note.tags:
                for tag in note.tags:
                    tagged_notes.append((tag.lower(), note_id, note))
            else:
                tagged_notes.append(("", note_id, note))

        tagged_notes.sort(key=lambda x: (x[0] == "", x[0], x[1]))

        result = []
        for tag, note_id, note in tagged_notes:
            tag_display = tag if tag else "No tag"
            result.append(f"[{tag_display}] {note_id}: {note}")

        return "\n".join(result)

    def __str__(self):
        if not self.data:
            return "No notes yet."
        return "\n".join([f"{note_id}: {note}" for note_id, note in self.data.items()])
    
    def find_by_text(self, text: str):
        result = []

        for note_id, note in self.data.items():
            note_text_lower = note.text.lower()
            search_text_lower = text.lower()

            if search_text_lower in note_text_lower:
                result.append(f"{note_id}: {note}")

        return result

def input_error(error_message="Something went wrong"):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            
            except (ValueError, IndexError, KeyError):
                return error_message
            
        return inner
    return decorator

@input_error("Usage: search-note-text [text]")
def search_note_text(args, notes):
    if not args:
        raise ValueError
    search_query = " ".join(args)
    found = notes.find_by_text(search_query)
    return "\n".join(str(note) for note in found) if found else "No notes containing that text."

@input_error("Usage: add-note [text] #[tag1] #[tag2]")
def add_note(args, notes):
    text = []
    tags = []
    for arg in args:
        if arg.startswith("#"):
            tags.append(arg[1:])
        else:
            text.append(arg)
    if not text:
        raise ValueError
    note = Note(" ".join(text), tags)
    notes.add_note(note)
    return "Note added."

@input_error("Usage: delete-note [note_id]")
def delete_note(args, notes):
    note_id = int(args[0])
    notes.delete_note(note_id)
    return f"Note {note_id} deleted."

@input_error("Usage: search-note-tag [#tag]")
def search_note_tag(args, notes):
    tag = args[0].lstrip("#")
    found = notes.find_by_tag(tag)
    return "\n".join(str(note) for note in found) if found else "No notes with this tag."

@input_error("No notes saved.")
def show_notes(notes):
    if not notes.data:
        raise ValueError
    return str(notes)

@input_error("Usage: edit-note [note_id]")
def edit_note(args, notes):
    note_id = int(args[0])
    notes.edit_note(note_id)
    return f"Note {note_id} updated."

@input_error("No notes saved")
def sort_by_tag(notes):
    if not notes.data:
        raise ValueError
    return notes.sort_by_tags()