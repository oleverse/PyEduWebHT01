from the_soft.arrange_dir.arrange_dir import ArrangeDir
from the_soft.contacts.contacts_bot import ContactsBot
from the_soft.notebook.notebook_bot import NotebookBot
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import pyfiglet
from the_soft.abstract.view import View
from the_soft.abstract.application import Application, AppComponent
from typing import Dict


FIRST_MENU = 'Your choice -> '


class CommandUnknown(AppComponent):
    def launch(self):
        print("Unknown command!", 'Try "help"!\n')


class AppHelp(AppComponent):
    def __init__(self, view: View):
        self.__view = view

    def launch(self):
        self.__view.render()


class ApplicationLogo(View):
    __app_name = None
    __app_slogan = None

    def __init__(self, name: str, slogan: str):
        self.__app_name = name
        self.__app_slogan = slogan

    def render(self) -> None:
        print(pyfiglet.Figlet().renderText(self.__app_name), end='')
        if self.__app_slogan:
            print(f"\n{self.__app_slogan}")
        print()


class MainMenu(View):
    __menu_entries = {}

    def __init__(self, entries: Dict[str, str] = None):
        if entries is not None:
            self.__menu_entries = {k: v for k, v in entries.items()}

    def render(self):
        for i, entry_key in enumerate(self.__menu_entries, 1):
            print(f"[{i}] {entry_key} - {self.__menu_entries[entry_key]['description']}")

    def add_entry(self, entry, description):
        self.__menu_entries[entry] = description


class TheSoftApp(Application, View):
    __app_name = "The S.O.F.T."
    __app_slogan = "The sophisticated organizer for thoughtful"
    __menu_entries = {
        "Contacts":     {"description": "open your contact book"},
        "Notebook":     {"description": "open your note book"},
        "Arrange Dir":  {"description": "arrange the folder content"},
        "Help": {"description": "get help"},
        "Exit": {"description": "quit the application"}
    }

    def __init__(self):
        self.__part_views = {
            "logo": ApplicationLogo(self.__app_name, self.__app_slogan),
            "menu": MainMenu(self.__menu_entries)
        }

        self.__commands = {
            ('1', 'phone book', 'address book', 'call'): ContactsBot(),
            ('2', 'note', 'add note'): NotebookBot(),
            ('3', 'arrange dir', 'sort dir'): ArrangeDir(),
            ('4', 'help', 'hello', 'hi'): AppHelp(self.__part_views["menu"]),
            ('5', 'close', 'quit', 'bye', 'goodbye', 'exit'): None
        }

    def render(self):
        for _, view in self.__part_views.items():
            view.render()

    def get_completer(self):
        completion_list = []
        for tupled_item in self.__commands:
            completion_list.extend(tupled_item)
        return WordCompleter(completion_list)

    def get_app_component_by_command(self, command: str) -> AppComponent:
        for tupled_key, component in self.__commands.items():
            if command in tupled_key:
                return component
        # command is not in any list
        return CommandUnknown()

    def ask_command(self):
        # Створення об'єкта WordCompleter для автозаповнення команд
        completer = self.get_completer()
        try:
            # Налаштування промпта з автозаповненням
            return prompt("Choose option: ", completer=completer).strip().lower()
        except (KeyboardInterrupt, EOFError):
            return False

    def main_loop(self):
        while component := self.get_app_component_by_command(self.ask_command()):
            component.launch()

        print("\nSee you later!")

    def run(self):
        self.render()
        self.main_loop()
        return 0
