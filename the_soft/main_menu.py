from the_soft.arrange_dir.arrange_dir import arrange_dir
from the_soft.address_book.main_address_book import main as adress_book
from the_soft.notebook.main_note import main as note_book
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import random
import pyfiglet

ABOUT_MLA = r'''
  _____  _             ____     ___     _____  _____  
 |_   _|| |__    ___  / ___|   / _ \   |  ___||_   _| 
   | |  | '_ \  / _ \ \___ \  | | | |  | |_     | |   
   | |  | | | ||  __/  ___) |_| |_| |_ |  _|_   | | _ 
   |_|  |_| |_| \___| |____/(_)\___/(_)|_| (_)  |_|(_) 

  The sophisticated organizer for thoughtful
                                                                         
Select an option:
[1] Open your contact book;
[2] Open your note book;
[3] I can put in order the folder where you put something meaning '''\
'''"it should be sorted later."
'''
JOKE_FROM_GPT = '''Why did the AI cross the road?\n
To prove it wasn't chicken, but it didn't need to prove anything to the '''\
'''humans, it already dominated them.'''
FIRST_MENU = 'Your choice -> '


def print_about_mla():
    print(ABOUT_MLA)


def print_hello():
    print(random.choice(['Hi, how can I help you?', 'Hello, human!']))


def print_joke():
    print(JOKE_FROM_GPT)


def goodbye():
    exit(0)


def start_arrange_dir():
    print(pyfiglet.Figlet().renderText("Arrange Dir"))
    try:
        dir = input('Give me the link to the dir: ')
    except (KeyboardInterrupt, EOFError):
        print()
        return False
    else:
        arrange_dir(dir)


def start_note_book():
    note_book()


def start_adress_book():
    adress_book()


COMMANDS = ['help', 'hello', 'hi', 'make joke', 'close', 'quit', 'by', 'goodbye',
            '3', 'arrange_dir', '2', 'note', 'add note', '1', 'phone_book',
            'address_book', 'call', 'exit']
FUNCTIONS = [print_about_mla, print_hello, print_hello, print_joke, goodbye,
             goodbye, goodbye, goodbye, start_arrange_dir, start_arrange_dir,
             start_note_book, start_note_book, start_adress_book,
             start_adress_book, start_adress_book, start_adress_book,
             start_adress_book, goodbye]
COMANDS_DICT = dict(zip(COMMANDS, FUNCTIONS))


def main():
    print(ABOUT_MLA)
    while True:
        # Створення об'єкта WordCompleter для автозаповнення команд
        command_completer = WordCompleter(COMMANDS)
        # Налаштування промпта з автозаповненням
        user_input = prompt(FIRST_MENU, completer=command_completer)
        try:
            COMANDS_DICT[user_input]()
        except KeyError:
            print("\nUnknown command!")


if __name__ == '__main__':
    try:
        while True:
            main()
    except (KeyboardInterrupt, EOFError):
        print("\nSee you later!")
        goodbye()
