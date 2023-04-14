from the_soft.notebook.notebook import *
from the_soft.base_bot.base_bot import BaseBot
from the_soft.abstract.application import AppComponent
from the_soft.interpreter.command_interpreter import CommandInterpreter
from the_soft.base_bot.base_bot import bot_exceptions


class NotebookBot(AppComponent, BaseBot):
    def __init__(self):
        self._items_collection = NoteBook()
        self._bot_name = "Notebook"
        self._commands = {
            ("help",): {
                "handler": self.get_help,
                "description": "shows this help"
            },
            ("add note",): {
                "handler": self.add_item,
                "description": "adds note to the Notebook"
            },
            ("delete note", "remove note"): {
                "handler": self.remove_item,
                "description": "deletes a note by ID"
            },
            ("change note", "edit note"): {
                "handler": self.edit_item,
                "description": "allows to edit an existing note"
            },
            ("search for contact", "find contact"): {
                "handler": self.search,
                "description": "looks for notes by a query string"
            },
            ("show all",): {
                "handler": self.show_all,
                "description": "prints all contacts with pagination"
            },
            ("goodbye", "quit", "close", "exit"): {
                "handler": None,
                "description": "quits the program"
            },
            ("show tags", "print tags"): {
                "handler": self.show_tags,
                "description": "shows all tags"
            },
            ("add tag", "new tag"): {
                "handler": self.add_tag,
                "description": "adds a tag to a note"
            },
            ("delete tag", "remove tag"): {
                "handler": self.del_tag,
                "description": "deletes a tag from all notes"
            },
            ("search tag", "find tag", "look for tag", "search by tag"): {
                "handler": self.search_tag,
                "description": "looks for notes by a tag"
            },
            ("clear tags",): {
                "handler": self.clear_tags,
                "description": "removing all tags from a note"
            },
            ("untag note",): {
                "handler": self.untag_note,
                "description": "removes a tag from a note"
            },
            ("sort by tags",): {
                "handler": self.sort_by_tags,
                "description": "outputs all notes sorted by tags"
            }
        }
        super().__init__()

    @staticmethod
    def split_by_len_line(text: str, length: int, split_list: list = None) -> list:
        """recursively splits the text by the specified length.
        returns a list of text chunks of approximately the same length.
        fucking recursion! I worked with her all night"""

        if split_list is None:
            split_list = []

        if len(text) <= length:
            split_list.append(text)
            return split_list
        else:
            index = length
            while index > 0 and text[index] != ' ':
                index -= 1
            split_list.append(text[:index])
            return NotebookBot.split_by_len_line(text[index + 1:], length, split_list)

    @staticmethod
    def make_line_longer(line: str, num_of_space: int) -> str:
        """increases the string length by adding spaces between words"""

        words = line.split(" ")
        result = "  ".join(words[:num_of_space + 1])
        others = " ".join(words[num_of_space + 1:])
        result += f" {others}"
        return result

    @staticmethod
    def content_format(text: str, length=80) -> str:
        """formats text by line length"""

        formatted_text = ""
        separated_text = NotebookBot.split_by_len_line(text, length)
        for line in separated_text:
            if line == separated_text[-1]:
                formatted_text += f'{line}'
            else:
                if len(line) == length - 1:
                    formatted_text = f"{line}\n"
                else:
                    num_of_space = length - len(line)
                    longer_line = NotebookBot.make_line_longer(line, num_of_space)
                    formatted_text += f"{longer_line}\n"
        return formatted_text

    def launch(self):
        self.prompt_loop()

    def add_item(self, item=None):
        print("A new note is being added...")

        interpreter = CommandInterpreter([], prompt_string="title: ", case_sensitive=True)
        title = Title(interpreter.ask())
        if len(title.value) > 80:
            print("The title must contain no more than 80 symbols")
            return False

        interpreter.set_prompt_string("content: ")
        content = Content(NotebookBot.content_format(interpreter.ask()))

        try:
            result = self._items_collection.add_note(Note(title, content))
        except bot_exceptions.ItemExists as ex:
            print(ex)
            return False

        if result:
            print("Note has been successfully added.")
        else:
            print('An error occured!')

        return result

    def remove_item(self, item: Item = None) -> bool:
        print("Deleting the note...")
        interpreter = CommandInterpreter(self._items_collection.keys(), "Enter the ID of the note: ", True)
        if not (note_id := interpreter.ask()):
            print("ID must be specified!")
            return False

        try:
            result = super().remove_item(int(note_id))
        except bot_exceptions.ItemNotExists as ex:
            print(ex)
            return False
        except ValueError:
            print("Bad ID!")
            return False

        if result:
            print("Note has been successfully removed.")
        else:
            print('An error occured!')

        return result

    def edit_item(self, item_p_key=None) -> bool:
        interpreter = CommandInterpreter(self._items_collection.keys(), "Enter note ID: ")
        item_p_key = interpreter.ask()
        try:
            item = self._items_collection[int(item_p_key)]
        except KeyError:
            print("The item doesn't exist, let's create a new one!")
            return self.add_item()
        except ValueError:
            print("Bad note ID!")
            return False

        print("The note is found and being edited...")
        interpreter = CommandInterpreter([], prompt_string="new title (blank to skip): ", case_sensitive=True)
        if title := interpreter.ask():
            if len(title) > 80:
                print("The title must contain no more than 80 symbols")
            else:
                item.title = Title(title)

        interpreter.set_prompt_string("new content (blank to skip): ")
        if content := interpreter.ask():
            item.content = Content(NotebookBot.content_format(content))

        result = self._items_collection.overwrite_note(item.id, Note(item.title, item.content))
        print("Note updated.")

        return result

    def search(self, pattern: str = None) -> None:
        if search_query := CommandInterpreter([], "Enter search query: ").ask():
            if found := self._items_collection.search(search_query, False):
                print(found)
            else:
                print("Nothing's found!")

    def show_tags(self):
        tags_list = NotebookBot.content_format(", ".join([tag for tag in self._items_collection.tags]))
        print(tags_list)

    def add_tag(self):
        interpreter = CommandInterpreter(self._items_collection.keys(), "Enter note ID: ")
        item_p_key = interpreter.ask()
        try:
            note_id = int(item_p_key)
            item = self._items_collection[note_id]
        except KeyError:
            print("The item doesn't exist!")
            return False
        except ValueError:
            print("Bad note ID!")
            return False

        if tag := CommandInterpreter([], "Enter tag to add: ", True).ask():
            tag = Tag(tag)
            self._items_collection.add_tag(tag, item.id)
            print("Tag added!")
            return True
        else:
            print("Tag cannot be empty!")
            return False

    def del_tag(self):
        if tag := CommandInterpreter([], "Enter tag to delete: ", True).ask():
            tag = Tag(tag)
            self._items_collection.del_tag(tag)
            print("Tag removed!")
            return True
        else:
            print("Tag cannot be empty!")
            return False

    def search_tag(self):
        if tag := CommandInterpreter([], "Enter tag to search: ", True).ask():
            found = self._items_collection.get_by_tag(Tag(tag), False)
            print(found or "Nothing's found!")
            return True

    def clear_tags(self):
        print("Clearing all tags from a note...")
        interpreter = CommandInterpreter(self._items_collection.keys(), "Enter note ID: ")
        item_p_key = interpreter.ask()
        try:
            note_id = int(item_p_key)
            item = self._items_collection[note_id]
        except KeyError:
            print("The item doesn't exist!")
            return False
        except ValueError:
            print("Bad note ID!")
            return False

        self._items_collection.clear_note_tags(item.id)
        print(f"Tags for the note with ID {item.id} are removed.")

    def untag_note(self):
        print("Removing a tag from a note...")
        interpreter = CommandInterpreter(self._items_collection.keys(), "Enter note ID: ")
        item_p_key = interpreter.ask()
        try:
            note_id = int(item_p_key)
            item = self._items_collection[note_id]
        except KeyError:
            print("The item doesn't exist!")
            return False
        except ValueError:
            print("Bad note ID!")
            return False

        if tag := CommandInterpreter([], "Enter tag to remove: ", True).ask():
            tag = Tag(tag)
            self._items_collection.untag_note(tag, item.id)
            return f"Tag {tag} deleted from note with ID {item.id}."
        else:
            print("Tag cannot be empty!")
            return False

    def sort_by_tags(self):
        sorted_by_tag = {}
        not_tagged = []
        id_with_tags = []
        for tag in sorted(self._items_collection.tags):
            sorted_by_tag[tag] = self._items_collection.get_by_tag(Tag(tag), False)
            id_with_tags.extend(self._items_collection.tags[tag].notes)

        id_with_tags = set(id_with_tags)

        for note in self._items_collection.values():
            if note.id not in id_with_tags:
                not_tagged.append(note)

        for tag, items in sorted_by_tag.items():
            print(f"TAG: {tag}:")
            print('\n'.join([str(n) for n in items.values()]), end="\n\n")

        if uncategorized := [str(n) for n in not_tagged]:
            print(f"TAG: Uncategorized:")
            print('\n'.join(uncategorized), end="\n\n")

        print("Done!")


if __name__ == "__main__":
    NotebookBot().launch()
