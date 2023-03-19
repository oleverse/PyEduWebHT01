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
        self.notes.append(note.id)


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
        self.tags = {}
    
    def __get_max_note_id(self):
        if len(self.data) > 0:
            return max([note.id for note in self.data.values()])

        return 0

    def add_note(self, note: Note):  # додає нотатку в словник ключем якого є id
        self.__max_note_id += 1
        note.id = self.__max_note_id
        self.data[note.id] = note

    def del_note(self, note_id):  # видаляє нотатки по id
        self.data.pop(note_id)
        return self.data

    def overwrite_note(self, note_id: int, new_note):
        pass
   
    def add_tag(self, tag: Tag):
        if tag.value not in self.tags.keys():
            self.tags[tag.value] = tag
        else:
            self.tags[tag.value].notes.extend(tag.notes)
            self.tags[tag.value].notes = list(set(self.tags[tag.value].notes))

    def del_tag(self, tag: Tag):
        self.tags.pop(tag.value, None)

    def untag_note(self, tag, note_id):
        try:
            for note in self.tags[tag.value].notes:
                if note == note_id:
                    self.tags[tag.value].notes.remove(note)
                    break
        except KeyError:
            return False
    
    def clear_note_tags(self, note_id):
        for tag in self.tags.values():
            self.untag_note(tag, note_id)

    def search(self, text: str): # пошук по заголовку
        pass

    def get_by_tag(self, tag: Tag, sort=False): # пошук по гегу
        pass

    def get_all(self): # поврптає усі нотатки
        pass

    def save_to_file(self, file_name="notebook.dat"): # зберігає у файлі
        pass

    def load_from_file(self, file_name="notebook.dat"): # завантажує з файлу
        pass
