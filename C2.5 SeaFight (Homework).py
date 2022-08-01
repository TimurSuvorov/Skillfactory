# Определение класса исключений
class BoardOutException(Exception):
    def __str__(self):
        return "Удар вне поля боя!"


class BoardUsedException(Exception):
    def __str__(self):
        return "Удар в те же координаты"


# Определение класса точек на поле
class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other_dot):
        return self.x == other_dot.x and self.y == other_dot.y

    def __repr__(self):
        return f"Dot ({self.x}, {self.y})"
