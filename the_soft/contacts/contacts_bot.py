from the_soft.abstract.application import AppComponent
from the_soft.contacts.address_book import *
from the_soft.base_bot.base_bot import BaseBot
from typing import Any
from the_soft.interpreter.command_interpreter import CommandInterpreter
from the_soft.base_bot.base_bot import bot_exceptions


class ContactsBot(AppComponent, BaseBot):
    def __init__(self):
        self._items_collection = AddressBook()
        self._bot_name = "Contacts"
        self._commands = {
            ("help",): {
                "handler": self.get_help,
                "description": "shows this help"
            },
            ("add", "add contact"): {
                "handler": self.add_item,
                "description": "adds a contact to the address book"
            },
            ("delete", "remove", "delete contact", "remove contact"): {
                "handler": self.remove_item,
                "description": "deletes a contact by the name"
            },
            ("change contact", "edit contact"): {
                "handler": self.edit_item,
                "description": "allows to edit an existing contact"
            },
            ("find", "search", "search for contact", "find contact"): {
                "handler": self.search,
                "description": "looks through contacts names and phones by a key"
            },
            ("congrats", "birthday search", "anniversary"): {
                "handler": self.congratulate,
                "description": "Search in the address book who has a birthday in the coming days"
            },
            ("show all",): {
                "handler": self.show_all,
                "description": "prints all contacts with pagination"
            },
            ("goodbye", "quit", "close", "exit"): {
                "handler": None,
                "description": "quits the program"
            }
        }
        super().__init__()

    def launch(self):
        self.prompt_loop()

    @staticmethod
    def __sanitize_phone_number(phone):
        """Cleans phone numbers"""

        ptrn = re.compile(r"[^+\d]")

        if new_phone := re.sub(pattern=ptrn, repl="", string=phone):
            new_phone = (
                    new_phone[0] +
                    new_phone[1:].replace("+", "")
            )
            return new_phone
        else:
            print("Invalid phone number!")

    @staticmethod
    def __is_valid_email(email):
        """Check Email"""

        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if re.fullmatch(regex, email):
            return email
        else:
            print("Invalid email")

    @staticmethod
    def __is_valid_address(address_home):
        if len(address_home) > 50:
            print("Too long Address")
        else:
            return address_home

    def add_item(self, item=None):
        print("A new contact is being added...")

        interpreter = CommandInterpreter([], prompt_string="name: ", case_sensitive=True)
        if not (name := interpreter.ask()):
            print("Name must be specified!")
            return False

        name = Name(name)

        interpreter.set_prompt_string("phone: ")
        if phone := interpreter.ask():
            phone = Phone(self.__sanitize_phone_number(phone))

        interpreter.set_prompt_string("birthday: ")
        if birthday := interpreter.ask():
            birthday = Birthday(birthday)

        interpreter.set_prompt_string("email: ")
        if email := interpreter.ask():
            email = Email(self.__is_valid_email(email))

        interpreter.set_prompt_string("address: ")
        if address_home := interpreter.ask():
            address_home = AddressHome(self.__is_valid_address(address_home))

        try:
            result = super().add_item(Record(name, phone, birthday, email, address_home))
        except bot_exceptions.ItemExists as ex:
            print(ex)
            return False

        if result:
            print("Contact has been successfully added.")
        else:
            print('An error occured!')

        return result

    def remove_item(self, item=None):
        print("Deleting the contact...")
        interpreter = CommandInterpreter(self._items_collection.keys(), "Enter the name of the contact: ", True)
        if not (name := interpreter.ask()):
            print("Name must be specified!")
            return False

        try:
            result = super().remove_item(name)
        except bot_exceptions.ItemNotExists as ex:
            print(ex)
            return False

        if result:
            print("Contact has been successfully removed.")
        else:
            print('An error occured!')

        return result

    def edit_item(self, item_p_key: Any = None) -> bool:
        interpreter = CommandInterpreter(self._items_collection.keys(), "Enter the name: ", True)
        item_p_key = interpreter.ask()
        try:
            item = self._items_collection[item_p_key]
        except KeyError:
            print("The item doesn't exist, let's create a new one!")
            return self.add_item()

        print("The contact is found and being edited...")
        print(f"Current name is {item.name.value}")
        interpreter = CommandInterpreter([], prompt_string="new name (blank to skip): ", case_sensitive=True)
        if name := interpreter.ask():
            item.name = Name(name)

        interpreter.set_prompt_string("new phone (blank to skip): ")
        if phone := interpreter.ask():
            item.phones.append(Phone(self.__sanitize_phone_number(phone)))

        interpreter.set_prompt_string("birthday (blank to skip): ")
        if birthday := interpreter.ask():
            item.birthday = Birthday(birthday)

        interpreter.set_prompt_string("email (blank to skip): ")
        if email := interpreter.ask():
            item.email = Email(self.__is_valid_email(email))

        interpreter.set_prompt_string("address (blank to skip): ")
        if address_home := interpreter.ask():
            item.address_home = AddressHome(self.__is_valid_address(address_home))

        super().remove_item(item.p_key)
        item.p_key = item.name.value
        result = super().add_item(item)

        return result

    def search(self, pattern: str = None) -> None:
        if search_query := CommandInterpreter([], "Enter search query: ").ask():
            if found := self._items_collection.search(search_query):
                print(found)
            else:
                print("Nothing's found!")

    def congratulate(self):
        if days_count := CommandInterpreter([], "Enter days number: ").ask():
            print(self._items_collection.search_bd(days_count) or "Nothing's found!")


if __name__ == "__main__":
    ContactsBot().launch()
