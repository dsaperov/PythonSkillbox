# -*- coding: utf-8 -*-


# Есть функция генерации списка простых чисел


def get_prime_numbers(n):
    prime_numbers = []
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
    return prime_numbers


# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик


class PrimeNumbers:
    def __init__(self, n):
        self.prime_numbers = []
        self.limit = n
        self.number = 1

    def __iter__(self):
        return self

    def __next__(self):
        while self.number < self.limit:
            self.number += 1
            for prime in self.prime_numbers:
                if self.number % prime == 0:
                    break
            else:
                self.prime_numbers.append(self.number)
                return self.number
        raise StopIteration()


prime_number_iterator = PrimeNumbers(n=10000)
for number in prime_number_iterator:
    print(number)


# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик


def prime_numbers_generator(n):
    prime_numbers = []
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
            yield number


for number in prime_numbers_generator(n=10000):
    print(number)


# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.

def happy_filter(number):
    number_str = str(number)
    length = len(number_str)

    if length == 1:
        print('Должно быть как минимум 2 цифры')
        return

    middle = length // 2
    if length % 2 == 0:
        sec_part_str = number_str[middle:]
    else:
        sec_part_str = number_str[middle + 1:]

    first_part_str = number_str[:middle]
    first_part_list = [int(digit) for digit in first_part_str]
    first_part_sum = sum(first_part_list)

    sec_part_list = [int(digit) for digit in sec_part_str]
    sec_part_sum = sum(sec_part_list)

    if first_part_sum == sec_part_sum:
        return True
    else:
        return False


def pallindrom_filter(number):
    number_str = str(number)
    length = len(number_str)

    if length == 1:
        print('Должно быть как минимум 2 цифры')
        return

    middle = length // 2
    if length % 2 == 0:
        sec_part_str = number_str[middle:]
    else:
        sec_part_str = number_str[middle + 1:]

    first_part_str = number_str[:middle]
    if first_part_str == sec_part_str:
        return True
    else:
        return False


def cullen_filter(number):
    def cullen_digits():
        num = 0
        cullen_digit = 1
        while cullen_digit <= number:
            yield cullen_digit
            num += 1
            cullen_digit = num * 2 ** num + 1

    res = number in cullen_digits()
    return res

# Получение из простых чисел счастливых
# Способ 1
# for number in prime_numbers_generator(10000):
#     if happy_filter(number):
#         print(number)

# Способ 2
# for number in (number for number in prime_numbers_generator(10000) if happy_filter(number)):
#     print(number)

# Способ 3
# happy_prime_numbers = filter(happy_filter, (number for number in prime_numbers_generator(10000)))
# for num in happy_prime_numbers:
#     print(num)

# Способ 4
# class PrimeHappyNumbers:
#     def __init__(self, n):
#         self.prime_numbers = []
#         self.limit = n
#         self.number = 1
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         while self.number < self.limit:
#             self.number += 1
#             for prime in self.prime_numbers:
#                 if self.number % prime == 0:
#                     break
#             else:
#                 self.prime_numbers.append(self.number)
#                 if happy_filter(self.number):
#                     return self.number
#         raise StopIteration()
#
#
# prime_happy_number_iterator = PrimeHappyNumbers(n=10000)
# for number in prime_happy_number_iterator:
#     print(number)

# Получение из простых чисел счастливых палиндромных
# Способ 1
# for number in prime_numbers_generator(10000):
#     if happy_filter(number) and pallindrom_filter(number):
#         print(number)

# Способ 2
# for number in (number for number in prime_numbers_generator(10000) if happy_filter(number) and pallindrom_filter(number)):
#     print(number)

# Способ 3
# happy_prime_numbers = filter(happy_filter, (number for number in prime_numbers_generator(10000)))
# happy_pallindrom_prime_numbers = filter(pallindrom_filter, happy_prime_numbers)
# for number in happy_pallindrom_prime_numbers:
#     print(number)

# Способ 4
# def prime_happy_numbers_generator(n):
#     prime_numbers = []
#     for number in range(2, n + 1):
#         for prime in prime_numbers:
#             if number % prime == 0:
#                 break
#         else:
#             prime_numbers.append(number)
#             if happy_filter(number) and pallindrom_filter(number):
#                 yield number
#
# for number in prime_happy_numbers_generator(n=10000):
#     print(number)