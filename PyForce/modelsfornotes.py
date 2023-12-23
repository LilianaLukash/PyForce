from collections import defaultdict
from datetime import datetime, timedelta
import pickle
from collections import UserDict, UserList


class Field:
    def __init__(self, value):
        self.value = value


class Notes(UserDict):
    def __init__(self, title, note, tags=None):
        super().__init__()
        self.data["title"] = title.strip()
        self.data["note"] = note.strip()
        self.data["tags"] = tags or []

    def addtag(self, tag):
        self.data["tags"].append(tag)


class NotesBook(UserList):
    def __init__(self, *args):
        super().__init__(*args)

    def addnote(self, *args):
        newnote = Notes(*args)
        self.append(newnote)

    def searchbytitle(self, title):
        # Return the note with matching title, title have to be unique
        for note in self:
            if note.data["title"] == title:
                return note
        return None

    def removenote(self, title):
        note_to_remove = self.searchbytitle(title)
        if note_to_remove:
            self.remove(note_to_remove)
            print("Note deleted")

    def searchbytag(self, tag):
        # Return list of notes with matching tags
        found = []
        for note in self:
            if tag in note.data["tags"]:
                found.append(note)
        return found

    def editbytitle(self, title, newnote):
        note_to_edit = self.searchbytitle(title)
        if note_to_edit is not None:
            note_to_edit.data["note"] = newnote
            print("Text was changed")

    def all(self):
        for note in self:
            print(
                f"title: {note['title']} | Note: {note['note']} | Tags: {', '.join(note['tags'])}"
            )
        if self == []:
            print("No notes")

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        with open(filename, "rb") as file:
            self.data = pickle.load(file)
