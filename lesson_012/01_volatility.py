# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от средней цены за торговую сессию:
#   средняя цена = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / средняя цена) * 100%
# Например для бумаги №1:
#   average_price = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / average_price) * 100 = 8.7%
# Для бумаги №2:
#   average_price = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / average_price) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base_source/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
import os
import time


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'------------------------Функция работала {elapsed} секунд(ы)------------------------')
        return result

    return surrogate


class Ticker:

    def __init__(self, log):
        self.log = log
        self.id = None
        self.max_price = None
        self.min_price = None
        self.volatility = None

    def calculate_volatility(self):
        next(self.log)
        first_data_line = self.log.readline()
        self.id = self._get_column_data(first_data_line, column=0)
        first_price = self._get_column_data(first_data_line, column=2)
        self.max_price = self.min_price = first_price

        for line in self.log:
            price = self._get_column_data(line, column=2)
            if price > self.max_price:
                self.max_price = price
            if price < self.min_price:
                self.min_price = price

        average_price = (self.max_price + self.min_price) / 2
        volatility = (self.max_price - self.min_price) / average_price * 100
        self.volatility = round(volatility, 2)

    def _get_column_data(self, line, column):
        data_list = line.split(',')
        data = data_list[column]
        if column == 2:
            data = float(data)
        return data


@time_track
def main():
    zero_volatility_tickers = []
    non_zero_volatility_tickers = []

    trades_path = r'.\trades'
    file_names = os.listdir(trades_path)

    for file_name in file_names:
        file_path = os.path.join(trades_path, file_name)
        with open(file=file_path, mode='r') as file:
            ticker = Ticker(file)
            ticker.calculate_volatility()
            if ticker.volatility == 0:
                zero_volatility_tickers.append(ticker.id)
            else:
                non_zero_volatility_tickers.append((ticker.id, ticker.volatility))

    non_zero_volatility_tickers.sort(key=lambda x: x[1])
    min_volatility_tickers = non_zero_volatility_tickers[:3]
    max_volatility_tickers = non_zero_volatility_tickers[-3:]

    print('Максимальная волатильность:')
    for ticker in max_volatility_tickers:
        result = '\t' + f'{ticker[0]} - {ticker[1]}%'
        print(result)

    print('Минимальная волатильность:')
    for ticker in min_volatility_tickers:
        result = '\t' + f'{ticker[0]} - {ticker[1]}%'
        print(result)

    print('Нулевая волатильность:')
    zero_volatility_tickers = ', '.join(zero_volatility_tickers)
    print('\t' + zero_volatility_tickers)


main()
