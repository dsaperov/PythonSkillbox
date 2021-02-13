# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

from abc import ABCMeta, abstractmethod


class LogParser(metaclass=ABCMeta):

    def __init__(self, file_to_parse, result_file):
        self.file_to_parse = file_to_parse
        self.result_file = result_file
        self.line_count = {}

    @abstractmethod
    def parse_file(self, sort_slice):
        with open(self.file_to_parse, mode='r', encoding='cp1251') as p_file:
            for next_line in p_file:
                if 'NOK' in next_line:
                    next_line = next_line[:sort_slice] + ']'
                    print(next_line in self.line_count)
                    if next_line not in self.line_count:
                        self.write_result()
                        self.line_count.clear()
                        self.line_count[next_line] = 1
                    else:
                        self.line_count[next_line] += 1

    def write_result(self):
        with open(result_file, mode='a', encoding='cp1251') as r_file:
            for date, count in self.line_count.items():
                file_content = f'{date} {count}' + '\n'
                r_file.write(file_content)


class SortByHour(LogParser):
    def parse_file(self, sort_slice=14):
        super().parse_file(sort_slice)


class SortByMonth(LogParser):
    def parse_file(self, sort_slice=8):
        super().parse_file(sort_slice)


class SortByYear(LogParser):
    def parse_file(self, sort_slice=5):
        super().parse_file(sort_slice)


file_to_parse = 'events.txt'
result_file = 'result.txt'

SortByHour(file_to_parse, result_file).parse_file()
SortByMonth(file_to_parse, result_file).parse_file()
SortByYear(file_to_parse, result_file).parse_file()

# После выполнения первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828
