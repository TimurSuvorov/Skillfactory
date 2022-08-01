# Определение класса исключений
class BoardOutException(Exception):
    def __str__(self):
        return "Удар вне поля боя!"


class BoardUsedException(Exception):
    def __str__(self):
        return "Удар в те же координаты"
