# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.

class NotNameError(Exception):
    pass


class NotEmailError(Exception):
    pass


def validate(string):
    elements = string.split()
    if len(elements) != 3:
        raise ValueError('количество полей не равно 3-ем')
    name = elements[0]
    email = elements[1]
    age = elements[2]
    if not age.isdigit() or not 10 <= int(age) <= 99:
        raise ValueError('недопустимый возраст')
    elif not name.isalpha():
        raise NotNameError('имя содержит цифры')
    elif '@' not in email or '.' not in email:
        raise NotEmailError('недопустимый email')
    else:
        return True


def append_good_line(string):
    with open('registrations_good.log', mode='a', encoding='utf-8') as file:
        file.write(string)


def append_bad_line(string, exc_object):
    exc_class = exc_object.__class__.__name__
    with open('registrations_bad.log', mode='a', encoding='utf-8') as file:
        file_content = f'{string[:-1]} / {exc_class} - {exc_object}\n'
        file.write(file_content)


with open('registrations.txt', mode='r', encoding='utf-8') as file:
    for line in file:
        try:
            line_is_good = validate(line)
            append_good_line(line)
        except (ValueError, NotNameError, NotEmailError, IndexError) as exc:
            append_bad_line(line, exc)
