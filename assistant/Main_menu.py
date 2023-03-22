from arrange_dir import arrange_dir
from main_address_book import main as adress_book
from main_note import main as note_book
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import random


ABOUT_MLA = '''
Hi, I'm your little assistant!
Select an option:
[1] Open your contact book;
[2] Open your note book;
[3] I can put in order the same folder where you dump something for "it must be found later."
'''
JOKE_FROM_GPT = '''Why did the AI cross the road?\n
To prove it wasn't chicken, but it didn't need to prove anything to the humans, it already dominated them.'''
FIRST_MENU = 'Your choice -> '


def print_about_mla():
    print(ABOUT_MLA)

def print_hello():
    print(random.choice(['Hi, haw can i help you?', 'Hello, hurman']))

def print_joke():
    print(JOKE_FROM_GPT)

def goodby():
    exit(0)

def start_arrange_dir():
    try:
        dir = input('Give me the link to the dir: ')  #/Users/mykhailo/studies/go_it/my_little_assistant/arrange_dir/
    except:
        start_arrange_dir()
    arrange_dir(dir)

def start_note_book():
    note_book()

def start_adress_book():
    adress_book()

COMMANDS = ['help', 'hello', 'hi', 'make jok', 'close', 'quit', 'by', 'goodby',
            '3', 'arrange_dir', '2', 'note', 'add note', '1', 'phone_book',
            'address_book', 'call']
FUNCTIONS = [print_about_mla, print_hello, print_hello, print_joke, goodby,
             goodby, goodby, goodby, start_arrange_dir, start_arrange_dir,
             start_note_book, start_note_book, start_adress_book,
             start_adress_book, start_adress_book, start_adress_book,
             start_adress_book]
COMANDS_DICT = dict(zip(COMMANDS, FUNCTIONS))


def main():
    command_completer = WordCompleter(COMMANDS)  # Створення об'єкту WordCompleter для автозаповнення команд
    user_input = prompt(FIRST_MENU, completer=command_completer)  # Налаштування промпта з автозаповненням
    COMANDS_DICT[user_input]()


if __name__ == '__main__':
    print(ABOUT_MLA)
    while True:
        main()
