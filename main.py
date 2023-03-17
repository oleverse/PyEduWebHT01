import re
from address_book import *

GOOD_BYE_MSG = "Good bye!"
COMMAND_ARGS_MAX_COUNT = 3
INDEX_NOT_FOUND = -1

CONTACTS = AddressBook()

# utilities
def contact_index(name):
    """Returns the index of a contact in the CONTACTS list"""

    try:
        return [item["name"] for item in CONTACTS].index(name)
    except ValueError:
        return INDEX_NOT_FOUND


def contact_exists(name):
    """Returns whether a contact exists"""
    return contact_index(name) != INDEX_NOT_FOUND


def sanitize_phone_number(phone):
    """Cleans phone numbers"""

    ptrn = re.compile(r"[^+\d]")

    new_phone = re.sub(pattern=ptrn, repl="", string=phone)
    new_phone = (
        new_phone[0] +
        new_phone[1:].replace("+", "")
    )

    return new_phone


def input_error(handler):
    """Errors handler"""

    def decorate_handler(data=None):
        warning = ""
        if handler.__name__  == "call_handler" and data is not None:
            command = data[0]
            
            if data[1]:
                args_count = len(data[1])
                if args_count > COMMANDS[command]["args_count"]:
                    warning = "Extra arguments discarded.\n"
                    data = data[1][:COMMANDS[command]["args_count"]]
        try:
            return f"{warning}{handler(data)}"
        except KeyError:
            if handler.__name__  == "call_handler":
                return "Unknown command."
        except ValueError:
            if handler.__name__  == "call_handler":
                return "Too many arguments."
        except IndexError:
            if handler.__name__ in(
                    "add_handler",
                    "change_handler"
                ):
                if not data:
                    return "Input should be: name [phone [birthday]]"
            else:
                if not data:
                    return "Specify a name please."
    return decorate_handler


# command handlers
@input_error
def hello_handler(data=None):
    return "How can I help you?"


@input_error
def help_handler(data=None):
    field_len = len(sorted(COMMANDS.keys(), key=lambda x: len(x), reverse=True)[0])
    print(field_len)
    commands = [f"{c:<{field_len}} - {COMMANDS[c]['description']}" for c in COMMANDS]
    return f"   Available commands:\n\t" + '\n\t'.join(sorted(commands))


@input_error
def add_handler(data):
    name = Name(data[0])
    phone = None
    birthday = None

    if len(data) > 1:
        phone = Phone(sanitize_phone_number(data[1]))
        if len(data) == 3:
            birthday = Birthday(data[2])

    if CONTACTS.add_record(Record(name, phone, birthday)):
        return "Contact successfully added."
    else:
        return 'The record exists or an error occured. Try "change" command.'
    

@input_error
def delete_handler(data):
    try:
        CONTACTS.pop(data[0])
    except KeyError:
        return "Contact not found"
    else:
        return "Contact has been successfully deleted."


@input_error
def change_name_handler(data):
    try:
        record = CONTACTS[data[0]]
    except KeyError:
        return "Contact not found"
    else:
        record.name.value = data[1]
        if CONTACTS.add_record(record):
            CONTACTS.pop(data[0])
            return "Contact has been successfully renamed."
        else:
            record.name.value = data[0]
            return "Contact has not been successfully renamed."
    

@input_error
def change_phone_handler(data):
    phone = Phone(sanitize_phone_number(data[1]))
    new_phone = Phone(sanitize_phone_number(data[2]))

    try:
        the_contact = CONTACTS[data[0]]
    except KeyError:
        return "Contact not found."
    else:
        if the_contact.edit_phone(phone, new_phone):
            return "Phone number has been changed."
        else:
            return "Phone number has not been changed."


@input_error
def change_birthday_handler(data):
    try:
        the_contact = CONTACTS[data[0]]
    except KeyError:
        return "Contact not found."
    else:
        the_contact.birthday = Birthday(data[1])
        return "Birthday has been changed."


@input_error
def remove_phone_handler(data):
    phone = Phone(sanitize_phone_number(data[1]))

    try:
        the_contact = CONTACTS[data[0]]
    except KeyError:
        return "Contact not found."
    else:
        if the_contact.del_phone(phone):
            return "Phone number has been removed."
        else:
            return "Phone number has not been removed."
        
        
@input_error
def new_phone_handler(data):
    new_phone = Phone(sanitize_phone_number(data[1]))

    try:
        the_contact = CONTACTS[data[0]]
    except KeyError:
        return "Contact not found."
    else:
        if the_contact.add_phone(new_phone):
            return "Phone number has been added."
        else:
            return "Phone number has not been added."
    

@input_error
def find_handler(data):
    if (found := CONTACTS.search(data[0])):
        return found
    else:
        return "Contact not found."


@input_error
def show_all_handler(data=None):
    if len(CONTACTS) == 0:
        return "I do not have any contacts yet."
    
    if data:
        pages_count = int(data[0])
        for n, page in enumerate(CONTACTS.iterator(pages_count)):
            print(f"Page-{n}:")
            print(page)

            try:
                answer = input("Continue? [Y/n]: ")
            except (EOFError, KeyboardInterrupt):
                answer = "n"

            if answer == "n":
                break
        else:
            return "Done!"
    else:
        return str(CONTACTS)


@input_error
def exit_handler(data=None):
    if CONTACTS.serialize():
        print("Database saved.")

    return GOOD_BYE_MSG


COMMANDS = {
    "hello": {
        "handler": hello_handler,
        "args_count": 0,
        "description": "shows greetings"
    },
    "help": {
        "handler": help_handler,
        "args_count": 0,
        "description": "shows this help"
    },
    "add": {
        "handler": add_handler,
        "args_count": 3,
        "description": "adds a contact to the address book"
    },
    "delete": {
        "handler": delete_handler,
        "args_count": 1,
        "description": "deletes a contact by the name"
    },
    "change phone": {
        "handler": change_phone_handler,
        "args_count": 3,
        "description": "usage: change phone name old_number new_number"
    },
    "new phone": {
        "handler": new_phone_handler,
        "args_count": 2,
        "description": "usage: new phone name phone_number"
    },
    "remove phone": {
        "handler": remove_phone_handler,
        "args_count": 2,
        "description": "usage: remove phone name phone_number"
    },
    "change birthday": {
        "handler": change_birthday_handler,
        "args_count": 2,
        "description": "usage: change birthday name new_birthday"
    },
    "change name": {
        "handler": change_name_handler,
        "args_count": 2,
        "description": "usage: change name old_name new_name"
    },
    "find": {
        "handler": find_handler,
        "args_count": 1,
        "description": "looks through contacts names and phones by a key"
    },
    "show all": {
        "handler": show_all_handler,
        "args_count": 1,
        "description": "prints all contacts with pagination"
    },
    "exit": {
        "handler": exit_handler,
        "args_count": 0,
        "description": "quits the program"
    }
}


@input_error
def call_handler(command_data):
    if command_data[1] and len(command_data[1]) > COMMAND_ARGS_MAX_COUNT:
        raise ValueError
    return COMMANDS[command_data[0]]["handler"](command_data[1])


def main():
    CONTACTS.deserialize()

    while True:
        try:
            command_with_args = input("Enter command: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            exit_handler()
            exit()
        
        if command_with_args:
            command_parts = command_with_args.split(' ')
            
            command = None
            data = None
            for i, _ in enumerate(command_parts):
                if (command := ' '.join(command_parts[:i+1])) in list(COMMANDS.keys()):
                    data = command_parts[i+1:]
                    break

            handler_result = call_handler((command, data))

            print(handler_result)

            if handler_result == GOOD_BYE_MSG:
                break


if __name__ == "__main__":
    main()