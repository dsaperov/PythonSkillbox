# -*- coding: utf-8 -*-

# С помощью JSON файла rpg.json задана "карта" подземелья.
# Подземелье было выкопано монстрами и они всё ещё скрываются где-то в его глубинах,
# планируя набеги на близлежащие поселения.
# Само подземелье состоит из двух главных разветвлений и нескольких развилок,
# и лишь один из путей приведёт вас к главному Боссу
# и позволит предотвратить набеги и спасти мирных жителей.

# Напишите игру, в которой пользователь, с помощью консоли,
# сможет:
# 1) исследовать это подземелье:
#   -- передвижение должно осуществляться присваиванием переменной и только в одну сторону
#   -- перемещаясь из одной локации в другую, пользователь теряет время, указанное в конце названия каждой локации
# Так, перейдя в локацию Location_1_tm500 - вам необходимо будет списать со счёта 500 секунд.
# Тег, в названии локации, указывающий на время - 'tm'.
#
# 2) сражаться с монстрами:
#   -- сражение имитируется списанием со счета персонажа N-количества времени и получением N-количества опыта
#   -- опыт и время указаны в названиях монстров (после exp указано значение опыта и после tm указано время)
# Так, если в локации вы обнаружили монстра Mob_exp10_tm20 (или Boss_exp10_tm20)
# необходимо списать со счета 20 секунд и добавить 10 очков опыта.
# Теги указывающие на опыт и время - 'exp' и 'tm'.
# После того, как игра будет готова, сыграйте в неё и наберите 280 очков при положительном остатке времени.

# По мере продвижения вам так же необходимо вести журнал,
# в котором должна содержаться следующая информация:
# -- текущее положение
# -- текущее количество опыта
# -- текущая дата (отсчёт вести с первой локации с помощью datetime)
# После прохождения лабиринта, набора 280 очков опыта и проверки на остаток времени (remaining_time > 0),
# журнал необходимо записать в csv файл (назвать dungeon.csv, названия столбцов взять из field_names).

# Пример лога игры:
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 1234567890.0987654321 секунд
# Прошло уже 0:00:00
# Внутри вы видите:
# -- Монстра Mob_exp10_tm0
# -- Вход в локацию: Location_1_tm10400000
# -- Вход в локацию: Location_2_tm333000000
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Выход

remaining_time = '1234567890.0987654321'
# если изначально не писать число в виде строки - теряется точность!
field_names = ['current_location', 'current_experience', 'current_date']

import csv
import os
import re
from datetime import datetime
from decimal import Decimal
from json import load


class Warrior:
    ALL_ACTIONS = ['Атаковать монстров', 'Двигаться вглубь', 'Двигаться на старт', 'Выход из игры']
    DEFAULT_TIME_LEFT = '1234567890.0987654321'

    def __init__(self):
        self.time_left = Decimal(self.DEFAULT_TIME_LEFT).quantize(Decimal("1.0"), 'ROUND_HALF_UP')
        self.experience = 0

    def fight_mobs(self, mobs):
        reg_exp = r'exp(\d+)_'
        reg_time = r'tm(\d+)'

        for mob in mobs:
            time = re.search(reg_time, mob)
            exp = re.search(reg_exp, mob)
            self.time_left -= int(time[1])
            self.experience += int(exp[1])

    def move_to_next_location(self, selected_location):
        reg_time = r'tm(\d+)'
        time = re.search(reg_time, selected_location)
        self.time_left -= int(time[1])


class Location:

    def __init__(self):
        self.name = None
        self.content = None
        self.mobs = []
        self.non_location_objects_number = 0
        self.available_locations = []

    def auto_parse(self, locations_cleared_of_mobs):
        """
        В self.content всегда находится list, который может хранить объекты следующих типов:
        1. str с именем моба, охраняющего локацию
        2. dict с единственным ключом - названием локации, доступной для перехода
        3. другой list, который может хранить строки с именами мобов, охраняющих локацию

        Метод запускает цикл по объектам из self.content и передает объект на сортировку в метод _sort_object().

        :param locations_cleared_of_mobs: список локаций, очищенных от мобов.
        """
        for obj in self.content:
            self._sort_object(obj, locations_cleared_of_mobs, count_non_location_objects=True)

    def nullify_parsed_data(self):
        self.available_locations.clear()
        self.non_location_objects_number = 0
        self.mobs.clear()

    def _sort_object(self, obj, locations_cleared_of_mobs, count_non_location_objects):
        """
        Если передан объект типа str, он добавляется в self.mobs - список мобов, охраняющих локацию; если объект типа
        list, то хранящиеся в нем str также добавляются в self.mobs; если передан объект другого типа (dict с
        единственным ключом), то имя ключа добавляется в self.available_locations - списк доступных для перехода
        локаций.
        После обработки каждого объекта, кроме dict, счетчик self.non_location_objects_number увеличивается на 1. Т.о.
        в данном атрибуте фиксируется количество объектов в self.content, предшествующих объекту/объектам dict (dict
        хранит данные с названием доступной локации). Информация об этом позже понадобится для определения индекса, по
        которому можно обратиться к тому или иному dict в self.content.
        """
        if type(obj) == str:
            if self.name not in locations_cleared_of_mobs:
                self.mobs.append(obj)
            if count_non_location_objects:
                self.non_location_objects_number += 1
        elif type(obj) == list:
            for mob in obj:
                self.mobs.append(mob)
            self.non_location_objects_number += 1
        else:
            available_location = obj.keys()
            self.available_locations.extend(list(available_location))


class GameCore:
    EXP_TO_WIN = 280

    def __init__(self, hero, current_location, dungeon_map, log):
        self.hero = hero
        self.current_location = current_location
        self.dungeon_map = dungeon_map
        self.log = log

        self.start_time = None

        self.locations_cleared_of_mobs = {}

        self.game_finished = False

    def run(self):
        self.start_time = datetime.now()
        self.set_start_location()
        while not self.game_finished:
            time_data = self.get_time_data()
            if self.locations_cleared_of_mobs:
                self.print_time_info(time_data)
            self.log.write_data((self.current_location.name, self.hero.experience, time_data))
            self.current_location.auto_parse(self.locations_cleared_of_mobs)
            self.print_location_info()
            self.initiate_action()

    def get_time_data(self):
        current_time = datetime.now()
        time_passed_after_start = current_time - self.start_time
        total_seconds = time_passed_after_start.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = total_seconds % 60
        return f'{hours:02d}:{minutes:02d}:{seconds:09f}'

    @staticmethod
    def print_time_info(time_data):
        print('С начала игры прошло: ' + time_data)

    def set_start_location(self):
        start_location_name = list(self.dungeon_map.keys())[0]
        self.current_location.name = start_location_name
        self.current_location.content = self.dungeon_map[self.current_location.name]

    def print_location_info(self):
        print(f'Вы находитесь в {self.current_location.name}')
        print(f'У вас {self.hero.experience} опыта и осталось {self.hero.time_left} секунд')

        if self.current_location.mobs:
            if len(self.current_location.mobs) > 1:
                mobs = ', '.join(self.current_location.mobs)
            else:
                mobs = self.current_location.mobs[0]
        else:
            mobs = 'отсутствуют'
        available_locations = ', '.join(self.current_location.available_locations)
        print('Внутри вы видите:', f'-- Монстры: {mobs}', f'-- Входы в локации: {available_locations}', sep='\n')

    def initiate_action(self):
        available_actions_enumerated = self.get_available_actions_enumerated()
        self._print_options(available_actions_enumerated)
        selected_number = input()
        self.handle_action_choice(selected_number, available_actions_enumerated)

    def get_available_actions_enumerated(self):
        available_actions = self.hero.ALL_ACTIONS.copy()
        if not self.current_location.mobs:
            available_actions.remove('Атаковать монстров')
            if not self.current_location.available_locations:
                available_actions.remove('Двигаться вглубь')
        else:
            available_actions.remove('Двигаться вглубь')
        if self.current_location.name == list(self.dungeon_map.keys())[0]:
            available_actions.remove('Двигаться на старт')

        available_actions_enumerated = self._enumerate_options(available_actions)
        return available_actions_enumerated

    def handle_action_choice(self, selected_number, available_actions_enumerated):
        selected_action = self._get_selected_option(selected_number, available_actions_enumerated)
        if selected_action == 'Атаковать монстров':
            self.hero.fight_mobs(self.current_location.mobs)
            self.handle_fight_results()
        elif selected_action == 'Двигаться вглубь':
            self.set_next_location()
        elif selected_action == 'Двигаться на старт':
            self.set_start_location()
            self.current_location.nullify_parsed_data()
        else:
            print('Игра завершена.')
            self.game_finished = True

        if self.hero.time_left < 1:
            self.print_end_game_message('loss')

    def handle_next_location_choice(self, selected_number, available_locations_enumerated):
        selected_location, selected_number = self._get_selected_option(selected_number, available_locations_enumerated)
        location_index = self.current_location.non_location_objects_number + int(selected_number) - 1
        self.current_location.name = selected_location
        self.hero.move_to_next_location(selected_location)
        self.current_location.content = self.current_location.content[location_index][selected_location]
        self.current_location.nullify_parsed_data()

    def print_end_game_message(self, game_result):
        if game_result == 'win':
            message = f'Набрано {self.hero.experience} очков опыта. Вы выиграли игру! Желаете начать заново? (y/n)'
        else:
            message = 'Ваше время вышло... Игра завершена. Желаете начать заново? (y/n)'
        print(message)
        start_new_game_choice = input()
        self.handle_start_new_game_choice(start_new_game_choice)

    def handle_start_new_game_choice(self, choice):
        if choice == 'y':
            self.set_start_location()
            self.current_location.nullify_parsed_data()
            self.locations_cleared_of_mobs.clear()
            self.hero.time_left = Decimal(self.hero.DEFAULT_TIME_LEFT).quantize(Decimal(".0"), 'ROUND_HALF_UP')
            self.hero.experience = 0
        elif choice == 'n':
            self.game_finished = True
            time_data = self.get_time_data()
            self.log.write_data((self.current_location.name, self.hero.experience, time_data))
        else:
            print('Введите "y", если хотите начать заново, "n", если хотите завершить игру.')
            start_new_game_choice = input()
            self.handle_start_new_game_choice(start_new_game_choice)

    def handle_fight_results(self):
        if self.hero.time_left > 0:
            if self.hero.experience >= 280:
                self.print_end_game_message('win')
            else:
                self.current_location.mobs.clear()
                self.locations_cleared_of_mobs[self.current_location.name] = True

                print(f'После битвы у вас {self.hero.experience} опыта и осталось {self.hero.time_left} секунд')

                self.initiate_action()
        else:
            self.print_end_game_message('loss')

    def set_next_location(self):
        available_locations_enumerated = self._enumerate_options()
        print('Выберите номер локации:')
        self._print_options(available_locations_enumerated)
        selected_number = input()
        self.handle_next_location_choice(selected_number, available_locations_enumerated)

    def _enumerate_options(self, options=None):
        if not options:
            options = self.current_location.available_locations
        options_enumerated = {number: option for number, option in enumerate(options, 1)}
        return options_enumerated

    def _get_selected_option(self, selected_number, available_options_enumerated):
        try:
            selected_option = available_options_enumerated[int(selected_number)]
        except (ValueError, KeyError) as exc:
            if exc.__class__.__name__ == 'ValueError':
                print('--- Нужно выбрать число ---')
            else:
                print('--- Выбрано число не из списка ---')
            selected_number = input()
            selected_option = self._get_selected_option(selected_number, available_options_enumerated)
        finally:
            if 'Location' in selected_option:
                res = selected_option, selected_number
            else:
                res = selected_option
            return res

    @staticmethod
    def _print_options(options):
        print('Выберите действие:')
        for number, option in options.items():
            print(f'{number}. {option}')


class CsvLog:
    FIELDNAMES = ['current_location', 'current_experience', 'current_date']
    NAME = 'game_log.csv'

    def has_header(self):
        with open(self.NAME, 'r') as game_log:
            csv_test_bytes = game_log.read(512)
            sniffer = csv.Sniffer()
            result = sniffer.has_header(csv_test_bytes)
            return result

    def write_header(self, data_in_log, data=None):
        print(data_in_log)
        with open(self.NAME, "w", newline='') as game_log:
            writer = csv.writer(game_log)
            writer.writerow(self.FIELDNAMES)
            if data_in_log:
                writer.writerows(data)

    def write_data(self, data):
        preprocessed_data = self.preprocess_data_for_writing(data)
        with open(self.NAME, "a", newline='') as game_log:
            writer = csv.DictWriter(game_log, delimiter=',', fieldnames=self.FIELDNAMES)
            writer.writerow(preprocessed_data)

    def preprocess_data_for_writing(self, data):
        zipped_data = zip(self.FIELDNAMES, data)
        preprocessed_data = dict(zipped_data)
        return preprocessed_data

    def has_data(self):
        if os.stat(self.NAME).st_size != 0:
            return True

    def get_data(self):
        with open(self.NAME, "r", newline='') as game_log:
            csv_data = csv.reader(game_log)
            data = [row for row in csv_data]
            return data


if __name__ == '__main__':
    with open('dungeon_map.json', 'r', newline='') as dungeon_map_json:
        dungeon_map_dict = load(dungeon_map_json)

    hero = Warrior()
    current_location = Location()
    csv_log = CsvLog()

    if os.path.exists(csv_log.NAME) and csv_log.has_data():
        if not csv_log.has_header():
            csv_log_data = csv_log.get_data()
            csv_log.write_header(data_in_log=True, data=csv_log_data)
    else:
        csv_log.write_header(data_in_log=None)

    game = GameCore(hero, current_location, dungeon_map_dict, csv_log)
    game.run()


# Учитывая время и опыт, не забывайте о точности вычислений!

