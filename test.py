from notebook_classes import *


notebook = NoteBook()

note = Note(Title("Note1"), Content("Some content\
    blabla"))

notebook.add_note(note)

print(notebook[1].title.value)