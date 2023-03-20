import re
from notebook_classes import *

GOOD_BYE_MSG = "Good bye!"
COMMAND_ARGS_MAX_COUNT = 5
INDEX_NOT_FOUND = -1

notebook = NoteBook()



# command handlers

def hello_handler(data=None) :
    return "How can I help you?"



def help_handler(data=None) :
    field_len = len(sorted(COMMANDS.keys(), key=lambda x : len(x), reverse=True)[0])
    print(field_len)
    commands = [f"{c:<{field_len}} - {COMMANDS[c]['description']}" for c in COMMANDS]
    return f"   Available commands:\n\t" + '\n\t'.join(sorted(commands))



def add_note(data) -> str:
    title = input(f"Title: ")
    content = input(f"Content: ")
    notebook.add_note(Note(title, content))
    return "Note successfully added."



def show_all_handler(data=None) :
    if len(notebook) == 0 :
        return "I do not have any contacts yet."

    if data :
        pages_count = int(data[0])
        for n, page in enumerate(notebook.iterator(pages_count)) :
            print(f"Page-{n}:")
            print(page)

            try :
                answer = input("Continue? [Y/n]: ")
            except (EOFError, KeyboardInterrupt) :
                answer = "n"

            if answer == "n" :
                break
        else :
            return "Done!"
    else :
        return str(notebook)



def exit_handler(data=None) :
    if notebook.save_to_file() :
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
    "add note": {
        "handler": add_note,
        "args_count": 0,
        "description": "adds a contact to the address book"
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


def call_handler(command_data) :
    if command_data[1] and len(command_data[1]) > COMMAND_ARGS_MAX_COUNT :
        raise ValueError
    return COMMANDS[command_data[0]]["handler"](command_data[1])


def main() :
    notebook.load_from_file()

    while True :
        try :
            command_with_args = input("Enter command: ").strip()
        except (EOFError, KeyboardInterrupt) :
            print()
            exit_handler()
            exit()

        if command_with_args :
            command_parts = command_with_args.split(' ')

            command = None
            data = None
            for i, _ in enumerate(command_parts) :
                if (command := ' '.join(command_parts[:i + 1])) in list(COMMANDS.keys()) :
                    data = command_parts[i + 1 :]
                    break

            handler_result = call_handler((command, data))

            print(handler_result)

            if handler_result == GOOD_BYE_MSG :
                break


if __name__ == "__main__" :
    main()




