from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from typing import Union, Iterable


class CommandInterpreter:
    __prompt_string = "Choose option: "

    def __init__(self, completion_list: Iterable, prompt_string=None, case_sensitive=False):
        self.__completion_list = [str(w) for w in completion_list] if completion_list else completion_list
        self.__case_sensitive = case_sensitive
        if prompt_string is not None:
            self.__prompt_string = prompt_string

        # Створення об'єкта WordCompleter для автозаповнення команд
        self.__completer = self.get_completer()

    def ask(self) -> Union[str, bool]:
        try:
            # Налаштування промпта з автозаповненням
            value = prompt(self.__prompt_string, completer=self.__completer).strip()
            # value = input(self.__prompt_string).strip()
            return value if self.__case_sensitive else value.lower()

        except (KeyboardInterrupt, EOFError):
            return False

    def get_completer(self) -> WordCompleter:
        return WordCompleter(self.__completion_list)

    def set_prompt_string(self, prompt_string):
        self.__prompt_string = prompt_string
