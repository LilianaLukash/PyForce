from collections import defaultdict
from datetime import datetime, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, number):
        if not self.is_valid(number):
            raise ValueError("Invalid phone number")
        super().__init__(number)

    @staticmethod
    def is_valid(number):
        return len(number) == 10 and number.isdigit()


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Birthday(Field):
    def __init__(self, date):
        if not self.is_valid(date):
            raise ValueError("Invalid birthday date")
        super().__init__(date)

    @staticmethod
    def is_valid(date):
        try:
            datetime.strptime(date, "%d.%m.%Y")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        if Phone.is_valid(phone):
            self.phones.append(Phone(phone))
        else:
            raise ValueError("Invalid phone number")

    def add_birthday(self, birthday):
        if not birthday:
            return
        if Birthday.is_valid(birthday):
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Invalid birthday date")

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


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, name, phone, birthday=None):
        if name in self.data:
            self.data[name].add_phone(phone)
            self.data[name].add_birthday(birthday)
        else:
            self.data[name] = Record(name, phone, birthday)

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