from typing import List, Any
from abc import abstractmethod, ABC
from the_soft.abstract.view import View


class Item(View):
    def render(self):
        print(str(self))


class Bot(ABC):
    @abstractmethod
    def get_help(self, short=True) -> None:
        pass

    @abstractmethod
    def add_item(self, item: Item) -> bool:
        pass

    @abstractmethod
    def remove_item(self, item: Item) -> bool:
        pass

    @abstractmethod
    def update_item(self, item: Item, new_item: Item) -> bool:
        pass

    @abstractmethod
    def search(self, pattern: str) -> List[Item]:
        pass

    @abstractmethod
    def goodbye(self) -> None:
        pass

    @abstractmethod
    def execute_command(self, command: str) -> Any:
        pass
