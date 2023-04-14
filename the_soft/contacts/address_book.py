from collections import UserDict
from datetime import date
from pickle import dump, load
import re
import os
from math import ceil
from the_soft.abstract.serializable_collection import SerializableCollection
from the_soft.base_bot.base_bot import Item


class Field:
    _required = False
    _multi_field = False
    _value = None

    def __init__(self, value=None, required=False, multi_field=False) -> None:
        self._required = required
        self._multi_field = multi_field
        self._value = value

    @property
    def value(self) -> str:
        return self._value


class Name(Field):
    def __init__(self, value: str) -> None:
        super().__init__(required=True)
        self.value = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        if value and type(value) == str:
            self._value = value
        else:
            self._value = "John Doe"


class Phone(Field):
    def __init__(self, value: str) -> None:
        super().__init__(multi_field=True)
        self.value = value

    @staticmethod
    def __sanitize_phone_number(phone):
        ptrn = re.compile(r"[+)(.\- ]")
        new_phone = re.sub(pattern=ptrn, repl="", string=phone)

        if new_phone != phone:
            print(f'Phone number has been sanitized to "{new_phone}"')

        return new_phone

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        format_warning = '\n'.join([
            'Bad phone number format!',
            'The number:',
            '- should not have less than 3 digits',
            '- should not have more than 15 digits',
            '- may start from + and should contain only digits, parentheses, dots, giphens, spaces'
        ])

        if type(value) != str:
            try:
                value = str(value)
            except ValueError:
                print(format_warning)

        value = self.__sanitize_phone_number(value)

        uni_pattern = re.compile(r"^\d{3,15}$")

        if not re.match(pattern=uni_pattern, string=value):
            print(format_warning)

            self._value = None
        else:
            self._value = value


class Birthday(Field):
    def __init__(self, value: str) -> None:
        super().__init__(multi_field=True)
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        try:
            self._value = date.fromisoformat(value)
        except ValueError:
            print('Bad date format, should be "%Y-%m-%d" like "2000-01-01"')
            self._value = None


class Email(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value=value, multi_field=True)

    @property
    def value(self):
        return self._value


class AddressHome(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value=value, multi_field=True)

    @property
    def value(self):
        return self._value


class Record(Item):
    def __init__(self, name, phone=None,
                 birthday=None, email=None, address_home=None) -> None:
        self.name = name
        super().__init__(name.value)
        self.phones = []
        self.birthday = birthday
        self.email = email
        self.address_home = address_home

        if phone and phone.value:
            self.add_phone(phone)

    def __str__(self) -> str:
        result = f"{self.name.value} =>\n"

        if self.birthday and self.birthday.value is not None:
            result += f"\tbirthday: {self.birthday.value}"
            result += f" ({self.days_to_birthday()} days left)\n"

        if self.phones:
            result += "\tphones: "
            result += f"{', '.join([p.value for p in self.phones])}\n"

        if self.email:
            result += "\temail: "
            result += f" {self.email.value}\n"

        if self.address_home:
            result += "\taddress: "
            result += f" {self.address_home.value}\n"

        return result
    
    def __find_phone(self, phone: Phone):
        for i, item in enumerate(self.phones):
            if item.value == phone.value:
                return i

    def days_to_birthday(self):
        if self.birthday and self.birthday.value is not None:
            current_date = date.today()

            current_year_bd = date(
                current_date.year,
                self.birthday.value.month,
                self.birthday.value.day
            )

            if current_year_bd >= current_date:
                next_bd_year = current_date.year 
            else:
                next_bd_year = current_date.year + 1

            next_birthday = date(
                next_bd_year,
                self.birthday.value.month,
                self.birthday.value.day
            )

            return (next_birthday - current_date).days

    def add_phone(self, phone: Phone) -> bool:
        if phone and phone.value:
            self.phones.append(phone)
            return True
        return False

    def del_phone(self, phone: Phone) -> bool:
        if (index := self.__find_phone(phone)) is not None:
            self.phones.remove(self.phones[index])
            return True
        return False

    def edit_phone(self, current_value: Phone, new_value: Phone) -> bool:
        if (index := self.__find_phone(current_value)) is not None:
            self.phones[index].value = new_value.value
            return True
        return False


class AddressBook(UserDict, SerializableCollection):
    __with_init_dict = False

    def __init__(self, init_dict=None, db_file_path=None):
        self.__address_db_file = db_file_path or "address_book.dat"

        if init_dict is not None:
            self.__with_init_dict = True

        super().__init__(init_dict)

    def __record_exists(self, record_key):
        return bool(self.data.get(record_key, None))

    def __str__(self) -> str:
        return '\n'.join([f"{self.data[name]}" for name in self.data])

    def search_bd(self, days: str):
        if not days.isdecimal():
            return None
        found1 = AddressBook()
        for key in self.data:
            bday = self.data[key].days_to_birthday()
            if bday is not None and bday <= int(days):
                found1[key] = self.data[key]

        return found1 if len(found1.data) else None

    def search(self, pattern: str):
        found = AddressBook()
        for name, record in self.data.items():
            aggregated = ''.join([(f.value if isinstance(f, Field) else '')
                                  for f in (record.name, record.address_home, record.email)])
            aggregated += ''.join([(p.value if isinstance(p, Field) else '') for p in record.phones])
            if re.match(f".*{pattern}.*", aggregated, re.I):
                if isinstance(record, Record):
                    found[record.p_key] = record

        return found if len(found.data) else None

    def iterator(self, records_number=1):
        if records_number <= 0:
            records_number = 1
            print("Bad records number, set to default - 1")

        if records_number > len(self.data):
            records_number = len(self.data)

        ci = 0
        for _ in range(ceil(len(self.data) / records_number)):
            yield AddressBook(list(self.data.items())[ci:ci + records_number])
            ci += records_number

    def serialize(self, to_file: str = None) -> bool:
        dst_file = to_file or self.__address_db_file

        with open(dst_file, 'wb') as db_file_fh:
            if db_file_fh.writable():
                dump(self.data, db_file_fh)
            else:
                print(f"Cannot write to {dst_file} file!",
                      "Serialization is impossible!")
                return False
        return True
    
    def deserialize(self, from_file: str = None) -> bool:
        source_file = from_file or self.__address_db_file

        if not os.path.isfile(source_file):
            print(f"{self.__class__.__name__}: Database file {source_file} was not found!")
            return False
        
        with open(source_file, 'rb') as db_file_fh:
            if db_file_fh.readable():
                self.data = load(db_file_fh)
            else:
                print(f"{self.__class__.__name__}: Cannot read from {source_file} file!")
                return False
        return True
