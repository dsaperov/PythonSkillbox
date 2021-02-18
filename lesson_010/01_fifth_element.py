# -*- coding: utf-8 -*-

# Умножить константу BRUCE_WILLIS на пятый элемент строки, введенный пользователем
# Ообернуть код и обработать исключительные ситуации для произвольных входных параметров
# - ValueError - невозможно преобразовать к числу
# - IndexError - выход за границы списка
# - остальные исключения
# для каждого типа исключений написать на консоль соотв. сообщение


def multiplicate(string, operand):
    leeloo = int(input_data[4])
    res = BRUCE_WILLIS * leeloo
    return res


BRUCE_WILLIS = 42
input_data = input('Если хочешь что-нибудь сделать, сделай это сам: ')

try:
    result = multiplicate(input_data, BRUCE_WILLIS)
    print(f"- Leeloo Dallas! Multi-pass № {result}!")
except ValueError as exc:
    print(f'Невозможно преобразовать к числу символ {exc.args[0][-2]}.')
except IndexError as exc:
    print('Выход за границы списка.')
except:
    print('Произошла ошибка')
