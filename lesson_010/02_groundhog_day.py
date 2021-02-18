# -*- coding: utf-8 -*-

# День сурка
#
# Напишите функцию one_day() которая возвращает количество кармы от 1 до 7
# и может выкидывать исключения:
# - IamGodError
# - DrunkError
# - CarCrashError
# - GluttonyError
# - DepressionError
# - SuicideError
# Одно из этих исключений выбрасывается с вероятностью 1 к 13 каждый день
#
# Функцию оберните в бесконечный цикл, выход из которого возможен только при накоплении
# кармы до уровня ENLIGHTENMENT_CARMA_LEVEL. Исключения обработать и записать в лог.
# При создании собственных исключений максимально использовать функциональность
# базовых встроенных исключений.

from random import randint, choice


class IamGodError(Exception):
    pass


class DrunkError(Exception):
    pass


class CarCrashError(Exception):
    pass


class GluttonyError(Exception):
    pass


class DepressionError(Exception):
    pass


class SuicideError(Exception):
    pass


def one_day():
    karma = randint(1, 7)
    exc_dice = randint(1, 13)
    if exc_dice == 13:
        random_exc = choice([IamGodError, DrunkError, CarCrashError,
                             GluttonyError, DepressionError,
                             SuicideError])
        raise random_exc
    return karma


ENLIGHTENMENT_CARMA_LEVEL = 777
total_karma = 0
day = 0

while total_karma < ENLIGHTENMENT_CARMA_LEVEL:
    day += 1
    try:
        total_karma += one_day()
    except (IamGodError, DrunkError, CarCrashError, GluttonyError, DepressionError, SuicideError) as exc:
        with open('exceptions_log.txt', mode='a') as file:
            exc_class = exc.__class__.__name__
            file_content = f'День {day} - {str(exc_class)}\n'
            file.write(file_content)

print(day)

# https://goo.gl/JnsDqu
