from collections import defaultdict
from datetime import datetime, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, number):
        if not self.is_valid(number):
            raise ValueError("Invalid phone number")
        super().__init__(number)

    @staticmethod
    def is_valid(number):
        return len(number) == 10 and number.isdigit()


class Address(Field):
    def __init__(self, address):
        if not self.is_valid(address):
            raise ValueError("Invalid Address")
        super().__init__(address)

    @staticmethod
    def is_valid(address):
        try:
            address = str(address)
            return True
        except ValueError:
            return False


class Birthday(Field):
    date_format = "%d.%m.%Y"

    def __init__(self, date):
        if not self.is_valid(date):
            raise ValueError("Invalid birthday date")
        super().__init__(date)

    @staticmethod
    def is_valid(date):
        try:
            datetime.strptime(date, Birthday.date_format)
            return True
        except ValueError:
            return False


class Email(Field):
    def __init__(self, email):
        if not self.is_valid(email):
            raise ValueError("Invalid Email")
        super().__init__(email)

    @staticmethod
    def is_valid(email):
        try:
            email = str(email)
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, phone, address=None, birthday=None, email=None):
        self.name = Name(name)
        self.phones = {Phone(phone)}
        self.address = Address(address) if address else None
        self.birthday = Birthday(birthday) if birthday else None
        self.email = Email(email) if email else None

    def add_phone(self, phone):
        if Phone.is_valid(phone):
            self.phones.add(Phone(phone))
        else:
            raise ValueError("Invalid phone number")

    def add_address(self, address):
        if Address.is_valid(address):
            self.address = Address(address)
        else:
            raise ValueError("Invalid Address")

    def add_birthday(self, birthday):
        if not birthday:
            return
        if Birthday.is_valid(birthday):
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Invalid birthday date")

    def add_email(self, email):
        if Email.is_valid(email):
            self.email = Email(email)
        else:
            raise ValueError("Invalid Email")

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
        else:
            raise KeyError("Phone number not found")

    def edit_phone(self, old_phone, new_phone):
        if not Phone.is_valid(new_phone):
            raise ValueError("Invalid new phone number")

        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break
        else:
            raise KeyError("Phone number not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        raise KeyError("Phone number not found")

    def add_address(self, address: str):
        self.address = Address(address)

    def add_email(self, email: str):
        self.email = Email(email)

    def edit_address(self, address: str):
        self.add_address(address)

    def edit_email(self, email: str):
        self.add_email(email)

    def get_phones(self):
        return self.phones

    def get_birthday(self):
        return self.birthday.value

    def get_address(self):
        return self.address.value

    def get_email(self):
        return self.email.value

    def __str__(self):
        birthday = f", birthday: {str(self.birthday.value)}" if self.birthday else ""
        address = f", address: {str(self.address.value)}" if self.address else ""
        email = f", email: {str(self.email.value)}" if self.email else ""
        phones = ",".join([f"{v.value}" for v in self.phones])
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}{address}{email}"


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, name, phone, address=None, birthday=None, email=None):
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
        return len(self.data)

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise KeyError("Name not found")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Name not found")

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        with open(filename, "rb") as file:
            self.data = pickle.load(file)

    def get_birthdays_per_week(self):
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


def handle_all_birthdays(address_book):
    birthdays_by_date = defaultdict(list)

    today = datetime.now().date()

    for name, record in address_book.data.items():
        if record.birthday:
            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()

            for i in range(7):
                future_date = today + timedelta(days=i)
                if (
                    birthday_date.day == future_date.day
                    and birthday_date.month == future_date.month
                ):
                    birthdays_by_date[future_date].append(name)

    while birthdays_by_date:
        upcoming_dates = [today + timedelta(days=day_offset) for day_offset in range(7)]

        for day in upcoming_dates:
            day_of_week = day.strftime("%A")
            if names := birthdays_by_date.get(day, []):
                names = [name.capitalize() for name in names]
                if day_of_week == "Saturday":
                    day_of_week = "Monday"
                print(f"{day_of_week}: {', '.join(names)}")

            if day in birthdays_by_date:
                del birthdays_by_date[day]
