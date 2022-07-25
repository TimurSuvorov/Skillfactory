#Игра крестики-нолики
field = [['-' for j in range(3)] for i in range(3)] # Создание пустой матрицы
PLAYER =('x', 'o')
step_count = 0

#Функция вывода текущего поля в нужном формате
def print_field():
    print( "    0  1  2")
    for i, row in enumerate(field):
        print(f" {i} \033[1;34m {'  '.join(row)} \033[0;0m")
    print()

#Функция проверки выигрыша или ничьи
def win_check():
    # Формирование комбинации рядов для проверки на выигрыш
    win_set_h = list(map("".join, [field[i] for i in range(3)]))  # Горизонтальные ряды
    win_set_v = list(map("".join, [[field[i][j] for i in range(3)] for j in range(3)]))  # Вертикальные ряды
    win_set_d1 = list(map("".join, [[field[i][i] for i in range(3)]]))  # Диагональный ряд 1
    win_set_d2 = list(map("".join, [[field[i][-i - 1] for i in range(3)]]))  # Диагональный ряд 2
    win_sets = win_set_h + win_set_v + win_set_d1 + win_set_d2

    # Проверка на выигрыш или ничью
    if "xxx" in win_sets:
        print("\033[1;35m Победил игрок X. Поздравляем!\033[0;0m")
        return "stop"
    elif "ooo" in win_sets:
        print("\033[1;35mПобедил игрок O. Поздравляем!\033[0;0m")
        return "stop"
    elif step_count == 9:
        print("Конец игры! Ничья!")
        return "stop"


print_field()
while win_check() != "stop":
    try:
        i, j = map(int, input(f"Игрок '{PLAYER[step_count%2]}' введите координаты: ").split(' '))
        if field[i][j] == 'x' or field[i][j] == 'o':
            print(f"\033[2;33mЗдесь место занято '{field[i][j]}'. Поставьте в другое место на поле\033[0;0m ")
            print()
        else:
            field[i][j] = PLAYER[step_count%2]
            step_count += 1
            print_field()
    except Exception:
        print("\033[2;31mЧто-то пошло не так. Попробуйте ввести по-другому\033[0;0m")
        print()
