from random import shuffle

_holder = None


def guess_the_number():
    digits = list(range(10))
    while digits[0] == 0:
        shuffle(digits)
    global _holder
    _holder = digits[0:4]


def check_the_number(number):
    coincidences = 0
    bulls = 0
    for i in range(4):
        if int(number[i]) in _holder:
            coincidences += 1
        if int(number[i]) == _holder[i]:
            bulls += 1

    cows = coincidences - bulls
    return {'bulls': bulls, 'cows': cows}