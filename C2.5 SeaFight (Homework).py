# Класс исключений
class BoardOutException(Exception):
    def __str__(self):
        return "Удар вне поля боя!"
class BoardUsedException(Exception):
    def __str__(self):
        return "Удар в те же координаты"
class BoardWrongPlaceException(Exception):
    pass

# Класс точек на поле
class Dot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other_dot):
        return self.x == other_dot.x and self.y == other_dot.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

#Класс корабля (длина, расположение, жизни)
class Ship:

    def __init__(self, length, bowpos, direction):
        self.length = length
        self.bowpos = bowpos # Передается объект из Dot
        self.direction = direction
        self.health = length

    @property
    def dots(self):
        ships_dots = []

        for i in range(self.length):
            shipdot_x = self.bowpos.x
            shipdot_y = self.bowpos.y
            if self.direction == "v":
                shipdot_x += i
            if self.direction == "h":
                shipdot_y += i

            ships_dots.append(Dot(shipdot_x, shipdot_y))
        return ships_dots


# Класс поля
class Board:

    def __init__(self, size, hid = False):
        self.size = size
        self.hid = hid
        self.board = [["◌"]*size for i in range(size)]
        self.hidenboard = [["?"]*size for i in range(size)]
        self.allshipsdots = []
        self.allships = []
        self.conturdots = []
        self.liveships = None
        self.shotlist = []

    def __str__(self):
        row0 = " x\y  " + " | ".join([str(i) for i in range(1, self.size + 1)]) + " | "
        print(row0)
        for i, row in enumerate(self.board):
            print(f"| {i+1} |\033[1;34m {' | '.join(row)} | \033[0;0m")
        return ""

    @staticmethod  # Функция удаления элемента из массивов разного порядка
    def rm_elem(elem, lst_):
        lst_new = []
        for row in lst_:
            if elem in row:
                row.remove(elem)
            lst_new.append(row)
        return lst_new

    def add_ship(self, ship):
        for ships_dots in ship:
            # Проверка расстановки кораблей
            if ships_dots.x > self.size or ships_dots.y > self.size or \
                    ships_dots.x <= 0 or ships_dots.y <= 0 or \
                    Dot(ships_dots.x, ships_dots.y) in self.conturdots or \
                    Dot(ships_dots.x, ships_dots.y) in self.allshipsdots:
                raise BoardWrongPlaceException
            else:
                # Если всё ОК, ставим на поле метку и добавляем в список кораблей
                self.board[ship[0].x - 1][ship[0].y - 1] = "◆"  # Нос корабля
                self.board[ships_dots.x - 1][ships_dots.y - 1] = "■"  # Тело корабля
                self.allshipsdots.append(Dot(ships_dots.x, ships_dots.y))
        self.allships.append(ship)
        self.contur(ship)

    def contur(self, ship):
        for ships_dots in ship:
            # Перебор клеток вокруг каждой точки "ships_dots" корабля
            for i in range(-1, 2):
                for j in range(-1, 2):
                    ships_dots.xc, ships_dots.yc = ships_dots.x + i, ships_dots.y + j
                    # Проверка: клетка внутри поля&не сам корабль&еще не добавлен в contur
                    if (0 < ships_dots.xc <= self.size and 0 < ships_dots.yc <= self.size) and \
                            (Dot(ships_dots.xc, ships_dots.yc) not in ship) and \
                            (Dot(ships_dots.xc, ships_dots.yc) not in self.conturdots):
                        self.conturdots.append(Dot(ships_dots.xc, ships_dots.yc))
        return self.conturdots

    def hid(self):
        if self.hid:
            return self.hidenboard

    def shot(self, shots):
        shot_x = shots.x
        shot_y = shots.y
        if not(0 < shot_x <= self.size) or not(0 < shot_y <= self.size): # Проверка: если вне поля
            raise BoardOutException
        elif Dot(shot_x, shot_y) in self.shotlist: # Проверка: если в то же место
            raise BoardUsedException
        elif Dot(shot_x, shot_y) in self.allshipsdots: # Проверка: если попал в корабль
            self.board[shot_x - 1][shot_y - 1] = "╳"
            self.shotlist.append(Dot(shot_x , shot_y))
            self.allshipsdots.remove(Dot(shot_x, shot_y)) # Удаление из общего списка точек короблей
            self.allships = Board.rm_elem(Dot(shot_x, shot_y), self.allships) # Удаление из списка короблей
        else:                                       # Остальное: если промах
            self.board[shot_x - 1][shot_y - 1] = "T"


class Player:
    def __init__(self):
        self.userboard = Board
        self.aiboard = Bo