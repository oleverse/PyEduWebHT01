from abc import abstractmethod, ABC


class View(ABC):
    @abstractmethod
    def render(self):
        pass
