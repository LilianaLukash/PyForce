from models import *
from datetime import datetime

LOGO = r"""
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

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name."
        except ValueError as e:
            return (str(e) + "enter <?> to find out about all commands")
        except IndexError:
            return "Enter <name> <phone> please!"

    return wrapper


@input_error
def handle_hello():
    return "Greetings! How can I help you young Jedi?"


@input_error
def handle_add(command, address_book):
    _, name, phone, *birthday = command.split()
    birthday = birthday[0] if birthday else None
    address_book.add_record(name, phone, birthday)
    return f"Contact {name} added."

@input_error
def handle_change(command, address_book):
    _, name, phone = command.split()
    record = address_book.find(name)
    record.edit_phone(record.phones[0].value, phone)
    return "Contact {name} changed."


@input_error
def handle_phone(command, address_book):
    _, name = command.split()
    record = address_book.find(name)
    return f"Phone number for {name}: {record.phones[0].value}"


@input_error
def handle_delete(command, address_book):
    _, name = command.split()
    address_book.delete(name)
    return f"Deleted {name}"


@input_error
def handle_all(address_book):
    result = "All records:\n"
    for name, record in address_book.data.items():
        birthday_info = f" ({record.birthday.value})" if record.birthday else ""
        result += f"{name}: {record.phones[0].value}{birthday_info}\n"
    return result


@input_error
def handle_add_birthday(command, address_book):
    _, name, birthday = command.split()
    address_book.find(name).add_birthday(birthday)
    return f"Birthday added for {name}."


@input_error
def handle_show_birthday(command, address_book):
    _, name = command.split()
    record = address_book.find(name)
    if record.birthday:
        return f"Birthday for {name}: {record.birthday.value}"
    else:
        return f"No birthday found for {name}."


def print_supported_commands():
    print(f"{LOGO}\n"
      "'add-phone <name> <phone>'to add/create new contact or to add phone\n"
      "'add-email <name> <phone> <email>' to add an e-mail\n"
      "'add-birthday <name> <DD.MM.YYYY>'\n"
      "'add-phone <name> <phone> <note>' to add note you must\n"
      "'change <name> <new phone>' to change contact\n"
      "'phone-name' to see a phone and a name input\n"
      "'delete' <name> <phone> to delete contact\n"
      "'birthdays' to see upcoming birthdays for the next 7 days\n"
      "'birthdays <number of days>'-> if you want to specify for how many days forward you want a list of birthdays\n"
      "'all' to see all the addressbook\n"
      "'close' to end the assistant")


def main():
    try:
        with open("contacts", "rb"):
            pass
        file_exists = True
    except FileNotFoundError:
        file_exists = False

    address_book = AddressBook()

    if file_exists:
        address_book.load_from_file("contacts")
        print("Data loaded from file.")
    else:
        print("No data found in file. Creating a new one.")

    while True:
        command = input("Enter a command: ").strip()
        if command in ["close", "exit", "end"]:
            address_book.save_to_file("contacts")
            print("Good bye! May the Force be with you!")
            break
        elif command in ["hello", "hi"]:
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
        elif command.startswith("add"):
            print(handle_add(command, address_book))
        elif command.startswith("birthdays"):
            parts = command.split()
            if len(parts) == 1:
                num_of_days = 7  # Default value
            elif len(parts) == 2 and parts[1].isdigit():
                num_of_days = int(parts[1])
            else:
                print("Invalid command format. Please use 'birthdays' or 'birthdays <number>'.")
                continue
            if address_book.count_records() > 0:
                handle_all_birthdays(address_book, num_of_days)
            else:
                print("No contacts young Jedi. Please add contacts")
        elif command in ['?', 'help', 'how']:
            print_supported_commands()
        else:
            print("Invalid command young Jedi. Try again!")
            print_supported_commands()


if __name__ == "__main__":
    main()
