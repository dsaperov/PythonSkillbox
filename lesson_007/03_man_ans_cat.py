# -*- coding: utf-8 -*-

from random import randint
from termcolor import cprint


# Доработать практическую часть урока lesson_007/python_snippets/08_practice.py

# Необходимо создать класс кота. У кота есть аттрибуты - сытость и дом (в котором он живет).
# Кот живет с человеком в доме.
# Для кота дом характеризируется - миской для еды и грязью.
# Изначально в доме нет еды для кота и нет грязи.

# Доработать класс человека, добавив методы
#   подобрать кота - у кота появляется дом.
#   купить коту еды - кошачья еда в доме увеличивается на 50, деньги уменьшаются на 50.
#   убраться в доме - степень грязи в доме уменьшается на 100, сытость у человека уменьшается на 20.
# Увеличить кол-во зарабатываемых человеком денег до 150 (он выучил пайтон и устроился на хорошую работу :)

# Кот может есть, спать и драть обои - необходимо реализовать соответствующие методы.
# Когда кот спит - сытость уменьшается на 10
# Когда кот ест - сытость увеличивается на 20, кошачья еда в доме уменьшается на 10.
# Когда кот дерет обои - сытость уменьшается на 10, степень грязи в доме увеличивается на 5
# Если степень сытости < 0, кот умирает.
# Так же надо реализовать метод "действуй" для кота, в котором он принимает решение
# что будет делать сегодня

# Человеку и коту надо вместе прожить 365 дней.

class Cat:
    def __init__(self, name):
        self.name = name
        self.home = None
        self.fullness = 30

    def __str__(self):
        res = 'Кот {} сытый на {}.'.format(self.name, self.fullness)
        return res

    def eat(self):
        self.fullness += 20
        self.home.cat_food -= 10
        cprint('Кот {} обожрался!'.format(self.name), color='magenta')

    def sleep(self):
        self.fullness -= 10
        cprint('Кот {} спал весь день!'.format(self.name), color='magenta')

    def rip_off_wallpapers(self):
        self.fullness -= 10
        self.home.mud += 5
        cprint('Кот {} от скуки сгрыз обои!'.format(self.name), color='magenta')

    def act(self):
        if self.fullness < 30 and self.home.cat_food >= 10:
            self.eat()
        else:
            if self.fullness < 30 and self.home.cat_food < 10:
                cprint('В доме закончилась кошачья еда - кот {} голодает!'.format(self.name), color='red')
            dice = randint(1, 2)
            if dice == 1:
                self.sleep()
            else:
                self.rip_off_wallpapers()

        if self.fullness <= 0:
            self.home.alive_citizens.remove(self)
            cprint('Кот {} умер голодной смертью...'.format(self.name), color='red')


class Human:
    def __init__(self, name, home):
        self.name = name
        self.home = home
        self.home.alive_citizens.append(self)
        self.money = 100
        self.fullness = 100

    def __str__(self):
        res = '{} сытый на {}. Остаток денег - {}'.format(self.name, self.fullness, self.money)
        return res

    def pick_up_a_cat(self, _cat, home):
        _cat.home = home
        self.home.alive_citizens.append(_cat)
        cprint('{} забрал домой кота и назвал его {}!'.format(self.name, _cat.name), color='magenta')

    def buy_cat_food(self):
        self.home.cat_food += 50
        self.money -= 50
        cprint('{} купил еду котам!'.format(self.name), color='magenta')

    def buy_human_food(self):
        self.home.human_food += 50
        self.money -= 50
        cprint('{} купил еду себе!'.format(self.name), color='magenta')

    def clean_home(self):
        self.home.mud -= 100
        self.fullness -= 20
        cprint('{} поклеил обои и очистил дом от шерсти!'.format(self.name), color='magenta')

    def eat(self):
        self.fullness += 40
        cprint('{} поел!'.format(self.name), color='magenta')

    def work(self):
        self.money += 150
        self.fullness -= 20
        cprint('{} поработал!'.format(self.name), color='magenta')

    def have_a_rest(self):
        self.money -= 20
        cprint('{} отдохнул!'.format(self.name), color='magenta')

    def act(self):
        if self.fullness <= 20:
            self.eat()
        elif self.home.human_food < 50:
            self.buy_human_food()
        elif self.money < 50:
            self.work()
        elif self.home.cat_food < 60:
            self.buy_cat_food()
        elif self.home.mud > 100:
            self.clean_home()
        else:
            self.have_a_rest()

        if self.fullness <= 0:
            self.home.alive_citizens.remove(self)
            cprint('{} умер голодной смертью...'.format(self.name), color='red')


class Home:
    def __init__(self):
        self.human_food = 100
        self.cat_food = 0
        self.mud = 0
        self.alive_citizens = []

    def __str__(self):
        res = 'Осталось {} единиц человеческой еды, {} единиц кошачей еды. Загрязненность - {}.'.format(self.human_food,
                                                                                                        self.cat_food,
                                                                                                        self.mud)
        return res

    def act(self):
        if self.mud >= 250:
            self.alive_citizens.clear()
            cprint('Жители дома задохнулись от пыли и шерсти...', color='red')


sweet_home = Home()
human1 = Human('Василий', sweet_home)

cats = (Cat('Песик'), Cat('Динозавр'), Cat('Вован'), Cat('Дональд'), Cat('Хайзенберг'), Cat('Цыпленок'),
        Cat('Потрошитель'), Cat('Пушок'), Cat('Вредина'))

for cat in cats:
    human1.pick_up_a_cat(cat, sweet_home)

for day in range(1, 366):
    cprint('============== День {} =============='.format(day), color='green')
    for citizen in sweet_home.alive_citizens:
        citizen.act()
    sweet_home.act()
    if not sweet_home.alive_citizens:
        break
    cprint('-------------- На конец дня --------------'.format(day), color='blue')
    for citizen in sweet_home.alive_citizens:
        print(citizen)
    print(sweet_home)

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
