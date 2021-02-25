# -*- coding: utf-8 -*-

# На основе своего кода из lesson_009/02_log_parser.py напишите итератор (или генератор)
# котрый читает исходный файл events.txt и выдает число событий NOK за каждую минуту
# <время> <число повторений>
#
# пример использования:
#
# grouped_events = <создание итератора/генератора>
# for group_time, event_count in grouped_events:
#     print(f'[{group_time}] {event_count}')
#
# на консоли должно появится что-то вроде
#
# [2018-05-17 01:57] 1234

# Итератор
class LogParser:
    def __init__(self, file_to_parse):
        self.file_to_parse = file_to_parse
        self.opened_file = None
        self.prev_line = None
        self.prev_line_count = None
        self.cur_line = True

    def __iter__(self):
        self.opened_file = open(self.file_to_parse, mode='r', encoding='cp1251')
        return self

    def __next__(self):
        while self.cur_line:
            cur_line = self.opened_file.readline()
            if ' OK' not in cur_line:
                self.cur_line = cur_line[1:17]
                res = self._count_line()
                if res not in [(None, None), None]:
                    return res
        self.opened_file.close()
        raise StopIteration()

    def _count_line(self):
        if self.cur_line != self.prev_line:
            data = self.prev_line
            count = self.prev_line_count
            self.prev_line = self.cur_line
            self.prev_line_count = 1
            return data, count
        else:
            self.prev_line_count += 1

file_to_parse = r'D:\PycharmProjects\PythonSkillbox\lesson_009\events.txt'

grouped_events = LogParser(file_to_parse)
for group_time, event_count in grouped_events:
    print(f'[{group_time}] {event_count}')

# Генератор
def generator(file):
    prev_line = None
    prev_line_count = None

    cur_line = True
    while cur_line:
        cur_line = file.readline()
        if ' OK' not in cur_line:
            cur_line = cur_line[1:17]
            if cur_line != prev_line:
                if prev_line:
                    yield prev_line, prev_line_count
                prev_line, prev_line_count = cur_line, 1
            else:
                prev_line_count += 1

file_to_parse = r'D:\PycharmProjects\PythonSkillbox\lesson_009\events.txt'

with open(file_to_parse, mode='r', encoding='cp1251') as opened_file:
    for group_time, event_count in generator(opened_file):
        print(f'[{group_time}] {event_count}')