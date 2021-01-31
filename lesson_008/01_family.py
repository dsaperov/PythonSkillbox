# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint


######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:

    def __init__(self):
        self.money = 100
        self.food = 50
        self.mud = 0
        self.cat_food = 30
        self.citizens = {'humans': [], 'cats': []}

    def __str__(self):
        res = 'Деньги  - {}, еда - {}, загрязненность - {}, кошачья еда - {}'.format(self.money, self.food, self.mud,
                                                                                     self.cat_food)
        return res


class LivingThing:

    def __init__(self):
        self.fullness = 30

    def _cut_bias_par_values(self):
        if self.fullness > 100:
            self.fullness = 100
        if self.fullness < 0:
            self.fullness = -1

    def _update_life_parameters(self, name, house):
        if self.fullness < 0:
            if isinstance(self, Human):
                house.citizens['humans'].remove(self)
            else:
                house.citizens['cats'].remove(self)
            cprint('{} умер(ла) голодной смертью'.format(name), color='red')



class Human(LivingThing):
    def __init__(self, name, house):
        super().__init__()
        self.name = name
        self.happiness = 100
        self.house = house
        self.house.citizens['humans'].append(self)
        self.food_consumed = 0

    def __str__(self):
        res = '{}: сытость - {}, счастье - {}'.format(self.name, self.fullness, self.happiness)
        return res

    def _cut_bias_par_values(self):
        super()._cut_bias_par_values()
        if self.happiness > 100:
            self.happiness = 100

    def _update_life_parameters(self):
        super()._update_life_parameters(self.name, self.house)

        if self.house.mud > 90:
            self.happiness -= 10
        if self.happiness < 10:
            self.house.citizens.remove(self)
            cprint('{} умер(ла) от депрессии'.format(self.name), color='red')

    def eat(self):
        if self.house.food < 30:
            self.fullness += self.house.food
            self.food_consumed += self.house.food
            self.house.food = 0
        else:
            self.fullness += 30
            self.food_consumed += 30
            self.house.food -= 30
        print('{} поел(а)'.format(self.name))

    def pet_a_cat(self):
        self.happiness += 5
        print('{} погладил(а) кота'.format(self.name))

    def buy_cat_food(self):
        self.house.cat_food += 50
        self.house.money -= 50
        print('{} купил(а) еду для кота'.format(self.name))

    def act(self, action_done=False):
        if self.fullness < 50 and self.house.food > 0:
            self.eat()
            action_done = True
        elif self.house.cat_food < 40 <= self.house.money:
            self.buy_cat_food()
            action_done = True

        self.house.mud += 2.5
        return action_done


class Husband(Human):

    def __init__(self, name, house):
        super().__init__(name, house)
        self.money_earned = 0

    def work(self):
        self.fullness -= 10
        self.house.money += 150
        self.money_earned += 150
        print('{} поработал'.format(self.name))

    def gaming(self):
        self.fullness -= 10
        self.happiness += 20
        print('{} поиграл в WoT'.format(self.name))

    def act(self):
        if not super().act():
            if self.house.money < 400:
                self.work()
            elif self.happiness < 70:
                self.gaming()
            else:
                dice = randint(1, 4)
                if dice == 1 and self.house.food > 0:
                    self.eat()
                elif dice == 2:
                    self.work()
                elif dice == 3 and self.house.citizens['cats']:
                    self.pet_a_cat()
                else:
                    self.gaming()
        self._cut_bias_par_values()
        self._update_life_parameters()


class Wife(Human):

    def __init__(self, name, house):
        super().__init__(name, house)
        self.fur_coats_counter = 0

    def shopping(self):
        self.fullness -= 10
        self.house.food += 100
        self.house.money -= 100
        print('{} сходила за продуктами'.format(self.name))

    def buy_fur_coat(self):
        self.fullness -= 10
        self.house.money -= 350
        self.happiness += 60
        self.fur_coats_counter += 1
        print('{} купила шубу'.format(self.name))

    def clean_house(self):
        self.fullness -= 10
        self.house.mud -= 100
        if self.house.mud < 0:
            self.house.mud = 0
        print('{} убралась в доме'.format(self.name))

    def act(self):
        if not super().act():
            if self.house.food < 70 and self.house.money >= 100:
                self.shopping()
            elif self.happiness < 30 and self.house.money >= 350 and self.fur_coats_counter < 4:
                self.buy_fur_coat()
            elif self.house.mud > 80:
                self.clean_house()
            else:
                dices = []
                dice = randint(1, 5)
                while dice not in dices:
                    dices.append(dice)
                    if dice == 1 and self.house.money >= 100 and self.house.food <= 300:
                        self.shopping()
                    elif dice == 2 and self.house.money >= 350 and self.fur_coats_counter < 4:
                        self.buy_fur_coat()
                    elif dice == 3 and self.house.food > 0:
                        self.eat()
                    elif dice == 4:
                        self.clean_house()
                    elif dice == 5 and self.house.citizens['cats']:
                        self.pet_a_cat()
                    else:
                        new_number = False
                        while not new_number:
                            dice = randint(1, 5)
                            if dice not in dices:
                                new_number = True
        self._cut_bias_par_values()
        self._update_life_parameters()


# TODO после реализации первой части - отдать на проверку учителю

######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


class Cat(LivingThing):

    def __init__(self, name, house):
        super().__init__()
        self.name = name
        self.house = house
        self.house.citizens['cats'].append(self)

    def __str__(self):
        res = 'Кот {}: сытость - {}'.format(self.name, self.fullness)
        return res

    def eat(self):
        if self.house.cat_food >= 10:
            self.house.cat_food -= 10
            self.fullness += self.house.cat_food * 2
        else:
            self.fullness += self.house.cat_food * 2
            self.house.cat_food = 0
        print('Кот {} обожрался'.format(self.name))

    def sleep(self):
        self.fullness -= 50
        print('Кот {} спал весь день'.format(self.name))

    def soil(self):
        self.fullness -= 10
        self.house.mud += 5
        print('Кот {} от скуки сгрыз обои'.format(self.name))

    def act(self):
        if self.fullness < 30 and self.house.cat_food > 0:
            self.eat()
        else:
            dices = []
            dice = randint(1, 3)
            while dice not in dices:
                dices.append(dice)
                if dice == 1 and self.house.food > 0:
                    self.eat()
                elif dice == 2:
                    self.sleep()
                elif dice == 3:
                    self.soil()
                else:
                    dice = randint(2, 3)

        self._cut_bias_par_values()
        self._update_life_parameters(self.name, self.house)


######################################################## Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)

class Child(Human):

    def _update_life_parameters(self):
        LivingThing._update_life_parameters(self, self.name, self.house)
        if self.happiness != 100:
            self.happiness = 100

    def eat(self):
        if self.house.food < 10:
            self.fullness += self.house.food
            self.food_consumed += self.house.food
            self.house.food = 0
        else:
            self.fullness += 10
            self.food_consumed += 10
            self.house.food -= 10
        print('{} поел(а)'.format(self.name))

    def sleep(self):
        print('{} поcпал(а)'.format(self.name))
        self.fullness -= 10

    def act(self):
        if not super().act():
            dice = randint(1, 2)
            if dice == 1 and self.house.food > 0:
                self.eat()
            else:
                self.sleep()

        self._cut_bias_par_values()
        self._update_life_parameters()

# TODO после реализации второй части - отдать на проверку учителем две ветки


######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


home = House()
serge = Husband(name='Сережа')
masha = Wife(name='Маша')
kolya = Child(name='Коля')
murzik = Cat(name='Мурзик')

for day in range(1, 366):
    cprint('================== День {} =================='.format(day), color='green')
    for citizen in [citizen for citizens in home.citizens.values() for citizen in citizens]:
        citizen.act()
        cprint(citizen, color='cyan')
    cprint(home, color='magenta')
    if not home.citizens:
        break

print('Денег заработано - {}'.format(sergey.money_earned), 'Съедено еды - {}'.format(sergey.food_consumed +
                                                                                     masha.food_consumed),
      'Купено шуб - {}'.format(masha.fur_coats_counter), sep='\n')

# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')

