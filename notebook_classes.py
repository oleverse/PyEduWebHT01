from collections import UserDict
import pickle



class Field: # батьківський клас у якому прописані __init__, @property, @setter, які наслідують класи Tag, Title, Content
    def __init__(self, value) -> None:
        self.value = value



class Tag(Field): # тег 

    def __init__(self, value):
        super().__init__(value)
        self.notes = []
  
    def add_note(self, note):
        self.notes.append(note.note_id)



class Title(Field): # заголовок
    pass


class Content(Field): # основний зміст нотатки
    pass


class Note: 
    def __init__(self, title: Title, content: Content):
        self.title = title 
        self.content = content 
        self.id = 0


class NoteBook(UserDict): # контейнер для нотаток
    
    def __init__(self):
        super().__init__()
        self.__max_note_id = self.__get_max_note_id()
        self.tag_list = []
    
    def __get_max_note_id(self):
        if len(self.data) > 0:
            return max([note.id for note in self.data.values()], reverse=True)

        return 0

    def add_note(self, note: Note): # додає нотатку в словник ключем якого є id
        self.__max_note_id += 1
        note.id = self.__max_note_id
        self.data[note.id] = note

    def owerwrite(self, note_id: int, new_note):
        pass
   
    def add_tag(self, tag: Tag, note_id: int):
        pass

    def search_by_title(self, title): # пошук по заголовку
        pass

    def search_by_tag(self, tag): # пошук по гегу
        pass

    def show_all(self): # поврптає усі нотатки
        pass

    def del_note(self, note_id): # видаляє нотатки по id
        self.data.pop(note_id)
        return self.data

    def save_to_file(self): # зберігає у файлі
        pass

    def load_from_file(self): # завантажує з файлу
        pass