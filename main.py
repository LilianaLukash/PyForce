from models import *
from datetime import datetime
from modelsfornotes import *


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Give me name and phone please."
        except TypeError:
            return "Please use correct number of arguments"
        except Exception as ex:
            print(f"Unexpected exception {ex}: in def {func.__name__}()")

    return wrapper


@input_error
def handle_hello():
    return "How can I help you?"


@input_error
def handle_add(command, address_book):
    _ = command.split()
    while True:
        name = input("Enter Name: ")
        if name == "close":
            return "Exited to main menu"
        if not Name.is_valid(name):
            print("Please use valid name, or type 'close' to exit in main menu")
        else:
            break

    while True:
        phone = input("Enter Phone: ")
        if phone == "close":
            return "Exited to main menu"
        if not Phone.is_valid(phone):
            print("Please use valid phone number, or 'close' to exit in main menu")
        else:
            break

    address = input("Enter Address: ")
    birthday = input("Enter Birthday in DD.MM.YYYY format: ")
    email = input("Enter Email: ")

    address = address or None
    birthday = birthday or None
    email = email or None
    address_book.add_record(name, phone, address, birthday, email)
    return "Contact added."


@input_error
def handle_change(command, address_book):
    _, name, old_phone, new_phone = command.split()
    record = address_book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact changed."


@input_error
def handle_phone(command, address_book):
    _, name = command.split()
    record = address_book.find(name)
    return f"Phone numbers for {name}: {','.join(str(s.value) for s in record.phones)}"


@input_error
def handle_delete(command, address_book):
    _, name = command.split()
    address_book.delete(name)
    return f"Deleted {name}"


@input_error
def handle_all(address_book):
    if address_book.data:
        result = f"All records ({address_book.count_records()}):\n"
        return result + "\n".join([f"{v}" for k, v in address_book.data.items()])
    else:
        return "Data is empty, nothing to show"


@input_error
def handle_add_phone(command, address_book):
    _, name, phone = command.split()
    address_book.find(name).add_phone(phone)
    return f"Phone added for {name}."


@input_error
def handle_add_address(command, address_book):
    _, name, address = command.split()
    address_book.find(name).add_address(address)
    return f"Address added for {name}."


@input_error
def handle_add_birthday(command, address_book):
    _, name, birthday = command.split()
    address_book.find(name).add_birthday(birthday)
    return f"Birthday added for {name}."


@input_error
def handle_add_email(command, address_book):
    _, name, email = command.split()
    address_book.find(name).add_email(email)
    return f"Email added for {name}."


@input_error
def handle_show_birthday(command, address_book):
    _, name = command.split()
    record = address_book.find(name)
    if record.birthday:
        return f"Birthday for {name}: {record.birthday.value}"
    else:
        return f"No birthday found for {name}."


def handle_notes_add(command, note_book):
    _, title, text = command.split(":")
    note_book.addnote(title, text)
    tags_to_add = input(
        'Note was added. Do you want to add tags? If yes, write separate by ",", if not, put "n"'
    )
    if tags_to_add != "n":
        tags = tags_to_add.split(",")
        for newtag in tags:
            if note_to_edit := note_book.searchbytitle(title):
                note_to_edit.addtag(newtag.strip())
                print("Added")
            else:
                print(f"Note with title'{title}' was not found")


def handle_notes_edit(command, note_book):
    _, title, new_text = command.split(":")
    note_book.editbytitle(title, new_text)


def handle_notes_remove(command, note_book):
    _, title = command.split(":")
    note_book.removenote(title)


def handle_notes_find(command, note_book):
    _, title = command.split(":")
    title = title.strip()
    if note := note_book.searchbytitle(title):
        print(
            f"title: {note['title']} | Note: {note['note']} | Tags: {', '.join(note['tags'])}"
        )
    else:
        print("No such note")


def handle_findbytag(command, note_book):
    _, tag = command.split(":")
    found = note_book.searchbytag(tag)
    if found == []:
        print("No notes with this tag")
    else:
        for note in found:
            print(
                f"title: {note['title']} | Note: {note['note']} | Tags: {', '.join(note['tags'])}"
            )


def handle_addtag(command, note_book):
    _, title, tag = command.split(":")
    note = note_book.searchbytitle(title)
    note.addtag(tag)
    print(
        f"title: {note['title']} | Note: {note['note']} | Tags: {', '.join(note['tags'])}"
    )


def main():
    try:
        with open("contacts", "rb"):
            pass
        file_exists = True
    except FileNotFoundError:
        file_exists = False

    try:
        with open("notes", "rb"):
            pass
        file_notes_exists = True
    except FileNotFoundError:
        file_notes_exists = False

    address_book = AddressBook()
    note_book = NotesBook([])

    if file_exists:
        address_book.load_from_file("contacts")
        print("AddressBook data loaded from file.")
    else:
        print("No data found in AddressBook file. Creating a new one.")

    if file_notes_exists:
        note_book.load_from_file("notes")
        print("NotesBook data loaded from file.")
    else:
        print("No data found in NotesBook file. Creating a new one.")

    while True:
        command = input("Enter a command: ").strip()
        if command in ["close", "exit"]:
            address_book.save_to_file("contacts")
            note_book.save_to_file("notes")
            print("Good bye!")
            break
        elif command == "hello":
            print(handle_hello())
        elif command.startswith("change"):
            print(handle_change(command, address_book))
        elif command.startswith("phone"):
            print(handle_phone(command, address_book))
        elif command == "all":
            print(handle_all(address_book))
        elif command.startswith("delete"):
            print(handle_delete(command, address_book))
        elif command.startswith("add-birthday"):
            print(handle_add_birthday(command, address_book))
        elif command.startswith("show-birthday"):
            print(handle_show_birthday(command, address_book))
        elif command.startswith("add-contact"):
            print(handle_add(command, address_book))
        elif command.startswith("add-address"):
            print(handle_add_address(command, address_book))
        elif command.startswith("add-email"):
            print(handle_add_email(command, address_book))
        elif command.startswith("add-phone"):
            print(handle_add_phone(command, address_book))
        elif command == "birthdays":
            handle_all_birthdays(address_book)
        elif command.startswith("noteadd"):
            handle_notes_add(command, note_book)
        elif command.startswith("notesall"):
            note_book.all()
        elif command.startswith("notesedit"):
            handle_notes_edit(command, note_book)
        elif command.startswith("notesremove"):
            handle_notes_remove(command, note_book)
        elif command.startswith("notesfind"):
            handle_notes_find(command, note_book)
        elif command.startswith("findbytag"):
            handle_findbytag(command, note_book)
        elif command.startswith("addtag"):
            handle_addtag(command, note_book)

        else:
            print("Invalid command. Try again.")


if __name__ == "__main__":
    main()
