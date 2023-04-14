class BotExceptions(BaseException):
    _message = None

    def __init__(self, message=None):
        if message:
            self._message = message


class ItemExists(BotExceptions):
    def __str__(self):
        return self._message or "Item exists!"


class ItemNotExists(BotExceptions):
    def __str__(self):
        return self._message or "Item does not exists!"

