from the_soft.abstract.bot import Bot, Item
from the_soft.abstract.serializable_collection import SerializableCollection
from the_soft.exceptions import bot_exceptions
from typing import List, Any, Dict, Union, Tuple
import pyfiglet
from the_soft.interpreter.command_interpreter import CommandInterpreter


class BaseBot(Bot):
    _items_collection: Union[SerializableCollection, Dict[Any, Item]] = {}
    _commands: Dict[Tuple[Any], Any] = {}
    _bot_name = "Bot"

    def __init__(self):
        self.__interpreter = CommandInterpreter(self.get_completion_list(), "Enter command: ")

    def print_logo(self):
        print(pyfiglet.Figlet().renderText(self._bot_name))

    def add_item(self, item: Item = None) -> bool:
        if item is None:
            return False
        if self._items_collection.get(item.p_key, None):
            raise bot_exceptions.ItemExists
        else:
            self._items_collection[item.p_key] = item
            return True

    def remove_item(self, item_p_key: Any) -> bool:
        if item_p_key is None:
            return False
        if not self._items_collection.get(item_p_key, None):
            raise bot_exceptions.ItemNotExists
        else:
            self._items_collection.pop(item_p_key)
            return True

    def get_help(self) -> None:
        print("List of available commands:")
        print(*[v for v in self._commands], sep=', ', end="\n\n")

    def edit_item(self, item_p_key: Any) -> bool:
        raise NotImplementedError

    def search(self, pattern: str) -> List[Item]:
        raise NotImplementedError

    def goodbye(self) -> None:
        if self._items_collection.serialize():
            print(f"{self._bot_name}: items collection saved.")

    def show_all(self):
        for _, item in self._items_collection.items():
            item.render()

    def get_completion_list(self):
        completion_list = []
        for tupled_item in self._commands:
            if not isinstance(tupled_item, tuple):
                tupled_item = (tupled_item, )
            completion_list.extend(filter(lambda x: isinstance(x, str), tupled_item))
        return completion_list

    def get_command_handler(self, command: str):
        for tupled_key, value in self._commands.items():
            if command in tupled_key:
                return value["handler"]
        else:
            return self.unknown_command

    @staticmethod
    def unknown_command():
        print("Unknown command!")

    def prompt_loop(self):
        self.print_logo()

        print(f"{self._bot_name}: ", end='')
        if self._items_collection.deserialize():
            print("items collection loaded.")
        else:
            print("items collection NOT loaded.")

        while handler := self.get_command_handler(self.__interpreter.ask()):
            handler()

        self.goodbye()
