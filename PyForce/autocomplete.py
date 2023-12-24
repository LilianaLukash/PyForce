from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# You need to install the external package in the terminal first: pip install prompt_toolkit
commands = WordCompleter(
    [
        "close",
        "exit",
        "end",
        "bye",
        "hello",
        "hi",
        "change-phone",
        "phone",
        "all",
        "delete",
        "change-birthday",
        "show-birthday",
        "add-contact",
        "birthdays",
        "add-address",
        "add-email",
        "add-phone",
        "findall",
        "noteadd",
        "notesall",
        "notesedit",
        "notesremove",
        "findbytag",
        "addtag",
        "note-help",
        "notes-help",
        "notehelp",
        "noteshelp",
    ],
    ignore_case=True,
)
session = PromptSession(completer=commands)
