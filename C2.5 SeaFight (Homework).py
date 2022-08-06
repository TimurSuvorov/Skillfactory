import random


# Класс исключений
class AllBoardExceptions(Exception):
    pass


class BoardOutException(AllBoardExceptions):
    def __str__(self):
        return "Удар вне поля боя!"


class BoardUsedException(AllBoardExceptions):
    def __str__(self):
        return "Удар в те же координаты"


class BoardWrongPlaceException(AllBoardExceptions):
    def __str__(self):
        return "Ошибка расположения"
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

    @staticmethod
    def randomdot(size):
        return Dot(random.randint(1, size), random.randint(1, size))


# Класс корабля (длина, расположение, жизни)
class Ship:
    def __init__(self, length, bowpos, direction):
        self.length = length
        self.bowpos = bowpos  # Передается объект из Dot
        self.direction = direction
        self.health = length

    @property
    def dots(self):
        ships_dots = []
        for i in range(self.length):
            shipdot_x, shipdot_y = self.bowpos.x, self.bowpos.y
            if self.direction == "v":
                shipdot_x += i
            if self.direction == "h":
                shipdot_y += i

            ships_dots.append(Dot(shipdot_x, shipdot_y))
        return ships_dots


# Класс поля
class Board:

    def __init__(self, size, hid=False):
        self.size = size
        self.hid = hid
        self.board = [["◌"]*size for _ in range(size)]
        self.hidenboard = [["?"]*size for _ in range(size)]
        self.allshipsdots = []
        self.allships = []
        self.conturdots = []
        self.shotlist = []

    def __str__(self):
        row0 = "         x\y  " + " | ".join([str(i) for i in range(1, self.size + 1)]) + " | "
        print(row0)
        if self.hid:
            self.board = self.hidenboard
        for i, row in enumerate(self.board):
            print(f"        | {i+1} |\033[1;34m {' | '.join(row)} | \033[0;0m")
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
            # Проверка всех точек корабля на возможность установки
            if ships_dots.x > self.size or ships_dots.y > self.size or \
                    ships_dots.x < 1 or ships_dots.y < 1 or \
                    Dot(ships_dots.x, ships_dots.y) in self.conturdots or \
                    Dot(ships_dots.x, ships_dots.y) in self.allshipsdots:
                raise BoardWrongPlaceException

        # Если всё ОК, ставим на поле метку и добавляем в список кораблей
        for ships_dots in ship:
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
        if not(0 < shot_x <= self.size) or not(0 < shot_y <= self.size):  # Проверка: если вне поля
            raise BoardOutException
        elif Dot(shot_x, shot_y) in self.shotlist:  # Проверка: если в то же место
            raise BoardUsedException
        elif Dot(shot_x, shot_y) in self.allshipsdots:  # Проверка: если попал в корабль
            self.board[shot_x - 1][shot_y - 1] = "\033[1;31m╳\033[1;34m"
            self.shotlist.append(Dot(shot_x, shot_y))  # Добавление в список выстрелов
            self.allshipsdots.remove(Dot(shot_x, shot_y))  # Удаление из общего списка точек кораблей
            self.allships = Board.rm_elem(Dot(shot_x, shot_y), self.allships)  # Удаление из списка (массива) кораблей
            self.allships.remove([]) if [] in self.allships else self.allships  # Удаление пустых кораблей
            return "hit"
        else:                                       # Остальное: если промах
            self.board[shot_x - 1][shot_y - 1] = "\033[1;33m●\033[1;34m"  # В остальных случаях промах
            self.shotlist.append(Dot(shot_x, shot_y))  # Добавление в список выстрелов


class Player:
    def __init__(self, board, size):
        self.board = board
        self.size = size

    def ask(self):
        pass

    def move(self):
        try:
            if self.board.shot(self.ask) == "hit":
                print(self.board)
                print("Попадание! Ещё выстрел.")
                self.move()
        except Exception as err:
            print(err)
            self.move()


class User(Player):

    @property
    def ask(self):
        while True:
            inp = input("Введите координаты выстрела: ").split(" ")
            if len(inp) != 2:
                print("Введите два значения через пробел")
                continue
            if not (inp[0].isdigit() or inp[1].isdigit()):
                print("Значения должны быть целыми числами")
                continue

            inp_x, inp_y = map(int, inp)
            return Dot(inp_x, inp_y)


class AI(Player):

    @property
    def ask(self):
        return Dot.randomdot(self.size)


class Game:
    def __init__(self):
        self.greet()
        self.size = self.asksize  # При инициализации игры вопрос про размер поля
        self.mode = self.askmode  # При инициализации игры вопрос про режим игры
        self.user_board = Board(self.size, hid=self.mode)
        self.ai_board = Board(self.size, hid=False)
        self.user_pl = User(self.user_board, self.size)
        self.ai_pl = AI(self.ai_board, self.size)


    def greet(self):
        print("     \033[2;35m|  Добро пожаловать в игру 'Морской бой'      |")
        print("     |     На поле будут размещены корабли:        |")
        print("     |           3 x Шлюпки  - ■                   |")
        print("     |           2 x Эсминцы - ■ ■                 |")
        print("     |           1 x Линкор  - ■ ■ ■ ■             |")
        print("     |           Формат ввода: x\y                 |")
        print("     |           x - номер строки                  |")
        print("     |           y - номер столбца                 |\033[0;0m")
        print()

    @property
    def asksize(self):
        while True:
            size = input("Вы можете задать размер поля (по умолчанию 6). Введите 'n', чтобы пропустить: ")
            if not size.isdigit() and size != 'n':
                print("Значение должно быть целым числом или 'n'")
                continue
            if size == 'n':
                size = 6
                break
            if int(size) < 7:
                print("Введите значение больше 6")
                continue
            break
        return int(size)

    @property
    def askmode(self):
        while True:
            mode = input("Включить режим видимости вражеского поля ? (y/n): ")
            if mode == "y":
                mode = False
                break
            elif mode == "n":
                mode = True
                break
            else:
                print("Некорректный ввод")
        return mode

    def random_board(self, board):
        attempt = 0
        types = [4, 2, 2, 1, 1, 1]
        for i, shiptype in enumerate(types):
            while attempt < 1000:
                try:
                    board.add_ship(Ship(shiptype, Dot.randomdot(self.size), random.choice(["v", "h"])).dots)
                    break
                except AllBoardExceptions:
                    attempt += 1
                    #print(f"Loading... attempt = {attempt}")
                    continue
            if attempt == 1000:
                #print(f"Перезапуск доски attempt = {attempt}")
                board.__init__(self.size)
                self.random_board(board)

        return board

    def loop(self):
        while len(self.user_board.allships) > 0 and len(self.ai_board.allships) > 0:
            self.user_pl.move()
            self.ai_pl.move()
            print()
            print("                \033[2;32mПоле компьютера\033[0;0m")
            print(self.user_board)
            print(f"         Осталось кораблей у компьютера {len(self.user_board.allships)}")
            print()
            print("                  \033[2;32mПоле игрока\033[0;0m")
            print(self.ai_board)
            print(f"         Осталось кораблей у игрока {len(self.ai_board.allships)}")
            print()

        if len(self.user_board.allshipsdots) == 0:
            winner = "!!!Вы победили!!!"
        else:
            winner = "!!!Победил компьютер!!!"

        return print("Конец игры ", winner, end="\n")

    def start(self):
        self.random_board(self.user_board)
        self.random_board(self.ai_board)
        print()
        print("                \033[2;32mПоле компьютера\033[0;0m")
        print(self.user_board)
        print("                  \033[2;32mПоле игрока\033[0;0m")
        print(self.ai_board)
        self.loop()


Game().start()
