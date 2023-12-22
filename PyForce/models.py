from collections import defaultdict
from datetime import datetime, timedelta
import pickle
import re


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, name: str):
        if not self.is_valid(name):
            raise ValueError("Invalid Name")
        super().__init__(name)

    @staticmethod
    def is_valid(name: str):
        """
        Check if a name is valid.

        Args:
            name (str): The name to be checked.

        Returns:
            bool: True if the name is valid, False otherwise."""

        return name.strip() != ""


class Phone(Field):
    def __init__(self, number):
        if not self.is_valid(number):
            raise ValueError("Invalid phone number. Phone number must be 10 digits young Padawan")
        super().__init__(number)

    @staticmethod
    def is_valid(number):
        """
        Check if a phone number is valid.

        Args:
            number (str): The phone number to be checked.

        Returns:
            bool: True if the phone number is valid, False otherwise."""

        return len(number) == 10 and number.isdigit()


class Address(Field):
    def __init__(self, address):
        if not self.is_valid(address):
            raise ValueError("Invalid Address young Padawan")
        super().__init__(address)

    @staticmethod
    def is_valid(address):
        """
        Check if an address is valid.

        Args:
            address (str): The address to be checked.

        Returns:
            bool: True if the address is valid, False otherwise."""

        try:
            address = str(address)
            return True
        except ValueError:
            return False


class Birthday(Field):
    date_format = "%d.%m.%Y"

    def __init__(self, date):
        if not self.is_valid(date):
            raise ValueError(
                "Invalid birthday date. Birthday date must be <DD.MM.YYYY> format"
            )
        super().__init__(date)

    @staticmethod
    def is_valid(date):
        """
        Check if a date is valid.

        Args:
            date (str): The date to be checked.

        Returns:
            bool: True if the date is valid, False otherwise."""

        try:
            datetime.strptime(date, Birthday.date_format)
            return True
        except ValueError:
            return False


class Email(Field):
    def __init__(self, email):
        if not self.is_valid(email):
            raise ValueError("Invalid Email. Do or do not. There is no try")
        super().__init__(email)

    @staticmethod
    def is_valid(email):
        """
        The function `is_valid` checks if an email address is valid based on a specific pattern.

        :param email: The parameter `email` is a string that represents an email address
        """

        email_pattern = (
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )
        return re.fullmatch(email_pattern, email) is not None


class Record:
    def __init__(self, name, phone, address=None, birthday=None, email=None):
        self.name = Name(name)
        self.phones = {Phone(phone)}
        self.address = Address(address) if address else None
        self.birthday = Birthday(birthday) if birthday else None
        self.email = Email(email) if email else None

    def add_phone(self, phone):
        """
        Add a phone number to the object.
        Args:
            phone (str): The phone number to be added.
        Raises:
            ValueError: If the phone number is invalid.
        Returns:
            None
        """

        if Phone.is_valid(phone):
            self.phones.add(Phone(phone))
        else:
            raise ValueError(
                "Invalid phone number. Phone number must be 10 digits young Jedi"
            )

    def add_address(self, address):
        """
        Add an address to the object.

        Args:
            address (str): The address to be added.

        Raises:
            ValueError: If the address is invalid.

        Returns:
            None"""

        if Address.is_valid(address):
            self.address = Address(address)
        else:
            raise ValueError("Invalid Address young Padawan")

    def add_birthday(self, birthday):
        """
        Add a birthday to the object.

        Args:
            birthday (str): The birthday date to be added.

        Raises:
            ValueError: If the birthday date is invalid.

        Returns:
            None"""

        if not birthday:
            return
        if Birthday.is_valid(birthday):
            self.birthday = Birthday(birthday)
        else:
            raise ValueError(
                "Invalid birthday date. Birthday date must be <DD.MM.YYYY> format"
            )

    def add_email(self, email):
        """
        Add an email address to the object.

        Args:
            email (str): The email address to be added.

        Raises:
            ValueError: If the email address is invalid.

        Returns:
            None"""

        if Email.is_valid(email):
            self.email = Email(email)
        else:
            raise ValueError("Invalid Email. Do or do not. There is no try")

    def remove_phone(self, phone):
        """
        Remove a phone number from the object.

        Args:
            phone (str): The phone number to be removed.

        Raises:
            KeyError: If the phone number is not found.

        Returns:
            None"""

        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
        else:
            raise KeyError("Phone number not found youn Jedi")

    def edit_phone(self, old_phone, new_phone):
        """
        Edit a phone number by replacing the old phone number with a new phone number.

        Args:
            old_phone (str): The old phone number to be replaced.
            new_phone (str): The new phone number to replace the old phone number.

        Raises:
            ValueError: If the new phone number is invalid.
            KeyError: If the old phone number is not found.

        Returns:
            None"""

        if not Phone.is_valid(new_phone):
            raise ValueError("Invalid new phone number. Phone must be 10 digits young Jedi")

        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break
        else:
            raise KeyError("Phone number not found young Jedi. I've got a bad feeling about this")

    def find_phone(self, phone):
        """
        Find a phone number in the object.

        Args:
            phone (str): The phone number to be found.

        Raises:
            KeyError: If the phone number is not found.

        Returns:
            Phone: The Phone object representing the found phone number."""

        for p in self.phones:
            if p.value == phone:
                return p
        raise KeyError("Phone number not found. I've got a bad feeling about this")

    def edit_address(self, address: str):
        """
        Edit the address by adding a new address.

        Args:
            address (str): The new address to be added.

        Returns:
            None"""

        self.add_address(address)

    def edit_email(self, email: str):
        """
        Edit the email address by adding a new email.

        Args:
            email (str): The new email address to be added.

        Returns:
            None"""

        self.add_email(email)

    def get_phones(self):
        """
        Get the list of phone numbers associated with the object.

        Returns:
            list: A list of phone numbers."""

        return self.phones
      

    def get_birthday(self):      
        """
        Get the birthday associated with the object.

        Returns:
            Birthday or None: The birthday of the object, or None if not set."""
        
        return self.birthday.value if self.birthday else None

    def get_address(self):
        """
        Get the address associated with the object.

        Returns:
            str or None: The address of the object, or None if not set."""
        
        return self.address.value if self.address else None

    def get_email(self):
        """
        Get the email address associated with the object.

        Returns:
            str or None: The email address of the object, or None if not set."""
        
        return self.email.value if self.email else None



    def __str__(self):
        """
        Return a string representation of the Contact object.

        Returns:
            str: The string representation of the Contact object."""

        birthday = f", birthday: {str(self.birthday.value)}" if self.birthday else ""
        address = f", address: {str(self.address.value)}" if self.address else ""
        email = f", email: {str(self.email.value)}" if self.email else ""
        phones = ",".join([f"{v.value}" for v in self.phones])
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}{address}{email}"


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, name, phone, address=None, birthday=None, email=None):
        """
        Add a record to the address book.

        Args:
            name (str): The name of the contact.
            phone (str): The phone number of the contact.
            address (str, optional): The address of the contact. Defaults to None.
            birthday (str, optional): The birthday of the contact. Defaults to None.
            email (str, optional): The email address of the contact. Defaults to None.

        Returns:
            None"""

        if name in self.data:
            self.data[name].add_phone(phone)
            if address:
                self.data[name].add_address(address)
            if birthday:
                self.data[name].add_birthday(birthday)
            if email:
                self.data[name].add_email(email)
        else:
            self.data[name] = Record(name, phone, address, birthday, email)

    def count_records(self):
        """
        Count the number of records in the object.

        Returns:
            int: The number of records."""

        return len(self.data)

    def find(self, name):
        """
        Find a record by name in the object.

        Args:
            name (str): The name of the record to find.

        Raises:
            KeyError: If the record with the given name is not found.

        Returns:
            Record: The found record."""

        if name in self.data:
            return self.data[name]
        else:
            raise KeyError("Name not found young Jedi. Enter <?> to find out all commands")
    
    def find_by_criteria(self, criteria):
        records = []
        for name, record in self.data.items():
            sourcestring = name + ''.join(str(s.value) for s in record.get_phones()) + record.get_address() + record.get_birthday() + record.get_email() 
            if criteria in sourcestring:
                birthday = f", birthday: {str(record.get_birthday())}"
                address = f", address: {str(record.get_address())}" 
                email = f", email: {str(record.get_email())}"
                phones = ",".join([f"{v.value}" for v in record.get_phones()])
                targetstring = f"Contact name: {name}, phones: {phones}{birthday}{address}{email}"
                records.append(targetstring)
        return records

    def delete(self, name):
        """
        Delete a record by name from the object.

        Args:
            name (str): The name of the record to delete.

        Raises:
            KeyError: If the record with the given name is not found.

        Returns:
            None"""

        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Name not found young Jedi. Enter <?> to find out all commands")

    def save_to_file(self, filename):
        """
        Save the object to a file.

        Args:
            filename (str): The name of the file to save the object to.

        Returns:
            None"""

        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        """
        Load data from a file and update the object.

        Args:
            filename (str): The name of the file to load data from.

        Returns:
            None"""

        with open(filename, "rb") as file:
            self.data = pickle.load(file)

    def get_birthdays_per_week(self):
        """
        Get upcoming birthdays per week from the address book.

        Returns:
            dict: A dictionary mapping days of the week (0-6)
            to a list of tuples containing the names and birthday dates
            of contacts with upcoming birthdays.
        """

        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = {day: [] for day in range(7)}

        for name, record in self.data.items():
            if record.birthday:
                birthday_date = datetime.strptime(
                    record.birthday.value, "%d.%m.%Y"
                ).date()
                if today <= birthday_date < next_week:
                    day = (birthday_date - today).days
                    if day < 0:
                        day += 365
                    upcoming_birthdays[day].append((name, birthday_date))

        return upcoming_birthdays


def handle_all_birthdays(address_book, num_of_days=7):
    birthdays_by_date = defaultdict(list)

    today = datetime.now().date()

    for name, record in address_book.data.items():
        if record.birthday:
            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()

            for i in range(num_of_days):
                future_date = today + timedelta(days=i)
                if (
                    birthday_date.day == future_date.day
                    and birthday_date.month == future_date.month
                ):
                    birthdays_by_date[future_date].append(name)

    while birthdays_by_date:
        upcoming_dates = [
            today + timedelta(days=day_offset) for day_offset in range(num_of_days)
        ]

        for day in upcoming_dates:
            day_of_week = day.strftime("%A")
            if names := birthdays_by_date.get(day, []):
                names = [name.capitalize() for name in names]
                if day_of_week == "Saturday":
                    day_of_week = "Monday"
                print(f"{day_of_week} ({day.strftime('%d-%m')}): {', '.join(names)}")

            if day in birthdays_by_date:
                del birthdays_by_date[day]

    if not birthdays_by_date:
        print(f"No birthdays in the next {num_of_days} days young Jedi.")
