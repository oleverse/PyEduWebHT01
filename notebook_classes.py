from collections import UserDict
import pickle



class Fields: # батьківський клас у якому прописані __init__, @property, @setter, які наслідують класи Tag, Title, Content
    def __init__(self, value) -> None:
        self.value = value



class Tags(Fields): # тег
    pass


class Title(Fields): # заголовок
    pass


class Content(Fields): # основний зміст нотатки
    pass


class Note: 
    def __init__(self, title, content, tag = None):
        self.tag = tag
        self.title = title
        self.content = content



class NoteBook(UserDict): # контейнер для нотаток
    
    def add_note(self, note): # додає нотатку в словник ключем якого є заголовок
        self.data[note.title.value] = note

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