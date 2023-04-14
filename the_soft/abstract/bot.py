from typing import List, Any
from abc import abstractmethod, ABC
from the_soft.abstract.view import View


class Item(View):
    def __init__(self, p_key_value):
        self.p_key = p_key_value

    def render(self):
        print(str(self))


class Bot(ABC):
    @abstractmethod
    def get_help(self) -> None:
        pass

    @abstractmethod
    def add_item(self, item: Item) -> bool:
        pass

    @abstractmethod
    def remove_item(self, item_p_key: Any) -> bool:
        pass

    @abstractmethod
    def edit_item(self, item_p_key: Any) -> bool:
        pass

    @abstractmethod
    def search(self, pattern: str) -> List[Item]:
        pass

    @abstractmethod
    def goodbye(self) -> None:
        pass

    @abstractmethod
    def show_all(self):
        pass
