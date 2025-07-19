import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def autosave_contacts(method):
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        save_data(self)
        return result
    return wrapper