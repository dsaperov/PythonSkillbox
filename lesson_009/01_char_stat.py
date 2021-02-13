# -*- coding: utf-8 -*-

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

import zipfile
import os
from abc import ABCMeta, abstractmethod


class StatsGenerator(metaclass=ABCMeta):

    def __init__(self, file_name):
        self.file_name = file_name
        self.stats = {}
        self.total = 0

    def zip_check(self):
        if self.file_name.endswith('.zip'):
            return True
        else:
            return False

    def unzip(self):
        zipfile_dir = os.path.dirname(self.file_name)
        zfile = zipfile.ZipFile(self.file_name, mode='r')

        for file_name in zfile.namelist():
            zfile.extract(file_name, zipfile_dir)

        file_path = os.path.join(zipfile_dir, file_name)
        self.file_name = file_path

    def collect_stats(self):
        with open(self.file_name, mode='r', encoding='cp1251') as file:
            for line in file:
                self._collect_from_line(line)
            self.total = sum(self.stats.values())

    def _collect_from_line(self, line):
        for char in line:
            if char.isalpha():
                if char in self.stats:
                    self.stats[char] += 1
                else:
                    self.stats[char] = 1

    @abstractmethod
    def sort_stats(self):
        stats_list = list(self.stats.items())
        stats_list.sort(reverse=True, key=lambda x: x[1])
        return stats_list

    def print_table(self, sorted_stats):
        print('+---------+-----------+', '|  буква  |  частота  |', '+---------+-----------+', sep='\n')
        for char, count in sorted_stats:
            print(f'|    {char}    |   {count:6d}  |')
        print('+---------+-----------+', f'|  итого  |  {self.total}  |', '+---------+-----------+', sep='\n')

    def generate_stats(self):
        if self.zip_check():
            self.unzip()
        self.collect_stats()
        sorted_stats = self.sort_stats()
        self.print_table(sorted_stats)


class SortFreqAsc(StatsGenerator):
    def sort_stats(self):
        stats_list = list(self.stats.items())
        stats_list.sort(key=lambda x: x[1])
        return stats_list


class SortAlphAsc(StatsGenerator):
    def sort_stats(self):
        stats_list = list(self.stats.items())
        stats_list.sort()
        return stats_list


class SortAlphDesc(StatsGenerator):
    def sort_stats(self):
        stats_list = list(self.stats.items())
        stats_list.sort(reverse=True)
        return stats_list

file_name = 'D:\\PycharmProjects\\PythonSkillbox\\lesson_009\\python_snippets\\voyna-i-mir.txt.zip'

SortFreqAsc(file_name).generate_stats()
SortAlphAsc(file_name).generate_stats()
SortAlphDesc(file_name).generate_stats()


# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828


