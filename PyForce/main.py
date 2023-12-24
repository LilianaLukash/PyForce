from models import *
from datetime import datetime
from modelsfornotes import *
import threading 


LOGO_VADER = r"""

                       .-.
                      |_:_|
                     /(_Y_)\
.                   ( \/M\/ )
 '.               _.'-/'-'\-'._
   ':           _/.--'[[[[]'--.\_
     ':        /_'  : |::"| :  '.\
       ':     //   ./ |oUU| \.'  :\
         ':  _:'..' \_|___|_/ :   :|
           ':.  .'  |_[___]_|  :.':\
            [::\ |  :  | |  :   ; : \
             '-'   \/'.| |.' \  .;.' |
             |\_    \  '-'   :       |
             |  \    \ .:    :   |   |
             |   \    | '.   :    \  |
             /       \   :. .;       |
            /     |   |  :__/     :  \\
           |  |   |    \:   | \   |   ||
          /    \  : :  |:   /  |__|   /|
          |     : : :_/_|  /'._\  '--|_\
          /___.-/_|-'   \  \
                         '-'
"""

LOGO_C3PO = r"""
          ___
         /---\
        | @ @:|
        |  " :|
         \_-_/
       _.d._.b.__
   +"i\  |\_/|  /i"+
   [_| \ |   | / |_]
  .' |  ):===:(  | `.
  |:.'+-" | | "-+`.:|
  |_| |-. |_|   | |_|
  \:\ |-' /+\   ! |:|
   \ \|n._\+/_.n| / /
    \XT::::-::::T/ /
     "l-. `"' .-lXX
      |: \   / :|
      |:  i-i  :|
      |:  | |  :| 
      |:  | |  :|
     \|;_ | |__;|/
      (__() ()__) 
      |:  | |  :|      
"""


LOGO_R2D2 = r"""
             ___
          ,-'___'-.
        ,'  [(_)]  '.
       |_]||[][O]o[][|
     _ |_____________| _
    | []   _______   [] |
    | []   _______   [] |
   [| ||      _      || |]
    |_|| =   [=]     ||_|
    | || =   [|]     || |
    | ||      _      || |
    | ||||   (+)    (|| |
    | ||_____________|| |
    |_| \___________/ |_|
    / \      | |      / \
   /___\    /___\    /___\
"""


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "There is no such сontact young Padawan. <add-contact> first!"
        except ValueError as e:
            return f"{str(e)}. Make sure you provide data in the correct format. Enter <?> for the instructions"
        except IndexError:
            return "Provide a name and a phone number please young Jedi."
        except TypeError:
            return "Please use correct number of arguments young Padawan"
        except Exception as ex:
            print(f"Unexpected exception young Jedi {ex}: in def {func.__name__}()")

    return wrapper


@input_error
def handle_hello():
    return "Greetings! How can I help you young Jedi?"


@input_error
def handle_add(command, address_book):
    _ = command.split()
    while True:
        name = input("Enter Name: ")
        if name == "close":
            return "Exited to main menu"
        if not Name.is_valid(name):
            print("Please use valid name youn Jedi, or type 'close' to exit in main menu")
        else:
            break

    while True:
        phone = input("Enter Phone: ")
        if phone == "close":
            return "Exited to main menu"
        if not Phone.is_valid(phone):
            print("Please use valid phone number young Jedi, or 'close' to exit in main menu")
        else:
            break

    address = input("Enter Address: ")
    birthday = input("Enter Birthday in DD.MM.YYYY format: ")
    email = input("Enter Email: ")

    address = address or None
    birthday = birthday or None
    email = email or None
    address_book.add_record(name, phone, address, birthday, email)
    return "Contact added. May the Force be with you!"


@input_error
def handle_change(command, address_book):    # change of phone number
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
def handle_find_by_criteria(command, address_book):
    _, criteria = command.split()
    if len(criteria) < 3:
        return "Please enter min. 3 symbols for search criteria"
    records = address_book.find_by_criteria(criteria)
    result = f"Found {len(records)} record(s) for criteria - {criteria} :\n"
    return "\n".join(records)


@input_error
def handle_show_birthday(command, address_book):
    _, name = command.split()
    record = address_book.find(name)
    if record.birthday:
        return f"Birthday for {name}: {record.birthday.value}"
    else:
        return f"No birthday found for {name}."


def print_supported_commands():
    print(f"{LOGO_C3PO}\n"
      "'add-contact then <enter>. Successively type in <name><phone><birthday><address><email>'\n"
      "'add-phone <name> <phone>'to add a phone to the existing contact\n"
      "'add-email <name> <email>' to add an e-mail to the existing contact\n"
      "'add-email <name> <phone> <email>' to add an e-mail to the existing contact\n" #change e-mail
      "'add-address <name> <actual-adвress-in-one-string>' to add an address the existing contact\n"
      "'add-note <name> <phone> <note>' to add note you must\n"
      "'change-phone <name> <old phone> <new phone>' to change phone\n"
      "'findall <criteria> search of contacts by criteria from 3 symbols\n"
      "'phone <name>' to see a phone and a name input\n"
      "'show-birthday <name>' to see birthday date for the contact\n"
      "'change-birthday <name> <DD.MM.YYYY>'\n" #  re-write
      "'birthdays' to see upcoming birthdays for the next 7 days\n"
      "'birthdays <number of days>'-> if you want to specify for how many days forward you want a list of birthdays\n"
      "'all' to see all the addressbook\n"
      "'delete' <name>  to delete the contact\n"
      "'notes-help' if you want to see intstructions on how to add notes\n"
      "'close' to end the assistant"
      )


def print_notes_help_commands():
    print(f"{LOGO_R2D2}\n"
        " If you want to add notes follow the instructions below: \n"
          "'<noteadd : title : note >' - to add a note\n"
          "'type in <tag, tag, tag>' if you want tags\n"
          "'<notesall>' - to print all notes\n"
          "'<notesfind : title>' - search a note by title\n"
          "'<notesedit : title>' - search by title and re-write\n"
          "'<findbytag : title>' - find a note by tag\n"
          "'<addtag:title :<tag>>' add tag to a note by title\n"
          "'<notesremove: title>' - remove a note by title\n"
    )


@input_error
def handle_notes_add(command, note_book):
    _, title, text = command.split(":")
    title = title.strip()
    text = text.strip()
    note_book.addnote(title, text)
    tags_to_add = input(
        'Note was added.\nDo you want to add tags?\nIf yes, write separate by ",", if not, put "n": '
    )
    if tags_to_add != "n":
        tags = tags_to_add.split(",")
        for newtag in tags:
            if note_to_edit := note_book.searchbytitle(title):
                note_to_edit.addtag(newtag.strip())
                print("Added")
            else:
                print(f"Note with title'{title}' was not found")


@input_error
def handle_notes_edit(command, note_book):
    _, title, new_text = command.split(":")
    note_book.editbytitle(title, new_text)


@input_error
def handle_notes_remove(command, note_book):
    _, title = command.split(":")
    note_book.removenote(title)


@input_error
def handle_notes_find(command, note_book):
    _, title = command.split(":")
    title = title.strip()
    if note := note_book.searchbytitle(title):
        print(
            f"title: {note['title']} | Note: {note['note']} | Tags: {', '.join(note['tags'])}"
        )
    else:
        print("No such note")


@input_error
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


@input_error
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
        if command in ["close", "exit", "end", "bye"]:
            address_book.save_to_file("contacts")
            print(f"{LOGO_VADER}\nGood bye! May the Force be with you!")
            note_book.save_to_file("notes")
           
            break
        elif command in ["hello", "hi"]:
            print(handle_hello())
            
        elif command.startswith("change-phone"):
            print(handle_change(command, address_book))
        elif command.startswith("phone"):
            print(handle_phone(command, address_book))
        elif command == "all":
            print(handle_all(address_book))
        elif command.startswith("delete"):
            print(handle_delete(command, address_book))
        elif command.startswith("change-birthday"):
            print(handle_add_birthday(command, address_book))
        elif command.startswith("show-birthday"):
            print(handle_show_birthday(command, address_book))
        elif command.startswith("add-contact"):
            print(handle_add(command, address_book))
        elif command.startswith("birthdays"):
            parts = command.split()
            if len(parts) == 1:
                num_of_days = 7  # Default value
            elif len(parts) == 2 and parts[1].isdigit():
                num_of_days = int(parts[1])
            else:
                print(
                    "Invalid command format. Please use 'birthdays' or 'birthdays <number>'."
                )
                continue
            if address_book.count_records() > 0:
                handle_all_birthdays(address_book, num_of_days)
            else:
                print("No contacts young Jedi. Please add contacts")
        elif command in ["?", "help", "how"]:
            print_supported_commands()
        elif command in ["note-help", "notes-help", "notehelp", "noteshelp"]:
            print_notes_help_commands()
        elif command.startswith("add-address"):
            print(handle_add_address(command, address_book))
        elif command.startswith("add-email"):
            print(handle_add_email(command, address_book))
        elif command.startswith("add-phone"):
            print(handle_add_phone(command, address_book))
        elif command.startswith("findall"):
            print(handle_find_by_criteria(command, address_book))
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
            print("Invalid command young Jedi. Try again!")
            print_supported_commands()


if __name__ == "__main__":
    main()
