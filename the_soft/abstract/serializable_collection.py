from abc import abstractmethod, ABC


class SerializableCollection(ABC):
    @abstractmethod
    def serialize(self, to_file: str = None) -> bool:
        pass

    @abstractmethod
    def deserialize(self, from_file: str = None) -> bool:
        pass

    @abstractmethod
    def search(self, pattern: str):
        pass
