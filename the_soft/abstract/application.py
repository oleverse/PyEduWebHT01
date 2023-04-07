from abc import abstractmethod, ABC


class Application(ABC):
    @abstractmethod
    def run(self):
        pass


class AppComponent(ABC):
    @abstractmethod
    def launch(self):
        pass
