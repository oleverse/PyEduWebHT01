from notebook_classes import *


notebook = NoteBook()

note = Note(Title("Note1"), Content("Some content\
    blabla ewr rwe rw erw er 23r2 3r "))

note1 = Note(Title("Note1"), Content("Some content\
    blabla ewr rwe rw erw er 23r2 3r "))

notebook.add_note(note)
notebook.add_note(note1)



for i in range(4):
    tag = Tag(f"tag{i}")
    if i % 2:
        tag.add_note(note)
    else:
        tag.add_note(note1)

    notebook.add_tag(tag)



tag = Tag("tag0")
tag.add_note(note1)

notebook.add_tag(tag)

for v, tag in notebook.tag_list.items():
    print(tag.notes)

notebook.clear_note_tags(1)

for v, tag in notebook.tag_list.items():
    print(tag.notes)

