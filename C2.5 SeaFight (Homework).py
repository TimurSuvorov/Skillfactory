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

#Определение класса корабля (длина, расположение, жизни)
class Ship:

    def __init__(self, length, stpos, direction):
        self.length = length
        self.stpos = stpos
        self.direction = direction
        self.health = length

    @property
    def dots(self):
        ships_dots = []
        # В self.stpos передается объект из Dot

        for i in range(self.length):
            shipdot_x = self.stpos.x
            shipdot_y = self.stpos.y
            if self.direction == "v":
                shipdot_x += i
            if self.direction == "h":
                shipdot_y += i

            ships_dots.append(Dot(shipdot_x, shipdot_y))
        return ships_dots

