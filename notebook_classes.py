from collections import UserDict
import pickle



class Field: # батьківський клас у якому прописані __init__, @property, @setter, які наслідують класи Tag, Title, Content
    def __init__(self, value) -> None:
        self.value = value



class Tag(Field): # тег 
    pass


class Title(Field): # заголовок
    pass


class Content(Field): # основний зміст нотатки
    pass


class Note: 
    def __init__(self, title: str, content: str, tag = None):
        self.tag = tag # список
        self.title = title # строка
        self.content = content # строка
        
        



class NoteBook(UserDict): # контейнер для нотаток
    
    def add_note(self, note): # додає нотатку в словник ключем якого є id
        self.data[id(note)] = {}
        self.data[id(note)]["title"] = note.title.value
        self.data[id(note)]["content"] = note.content.value
        self.data[id(note)]["tags"] = note.tad.value

    def search_by_title(self, title): # пошук по заголовку
        pass

    def search_by_tag(self, tag): # пошук по гегу
        pass

    def show_all(self): # поврптає усі нотатки
        pass

    def del_note(self, title): # видаляє нотатки по заголовку
        pass

    def owerwrite(self, title): # дописати нотатку по заголовку
        pass

    def save_to_file(self): # зберігає у файлі
        pass

    def load_from_file(self): # завантажує з файлу
        pass