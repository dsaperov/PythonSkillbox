# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#
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
import os
import time
from threading import Thread, Lock


def time_track(func):
    def wrapper(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'------------------------Функция работала {elapsed} секунд(ы)------------------------')
        return result

    return wrapper


class VolatilityCalculator(Thread):

    def __init__(self, file_path, tickers, lock):
        super().__init__()
        self.file_path = file_path
        self.ticker_id = None
        self.max_price = None
        self.min_price = None
        self.tickers = tickers
        self.lock = lock

    def run(self):
        with open(file=self.file_path, mode='r') as file:
            next(file)
            first_data_line = file.readline()
            self._save_base_data(first_data_line)
            self._find_price_extremes(file)

        volatility = self._get_volatility()
        self._save_volatility(volatility)

    def _save_base_data(self, first_data_line):
        self.ticker_id = self._get_column_data(first_data_line, column=0)
        base_price = self._get_column_data(first_data_line, column=2)
        self.max_price = self.min_price = base_price

    def _get_column_data(self, line, column):
        data_list = line.split(',')
        data = data_list[column]
        if column == 2:
            data = float(data)
        return data

    def _find_price_extremes(self, file):
        for line in file:
            price = self._get_column_data(line, column=2)
            if price > self.max_price:
                self.max_price = price
            if price < self.min_price:
                self.min_price = price

    def _get_volatility(self):
        average_price = (self.max_price + self.min_price) / 2
        volatility = (self.max_price - self.min_price) / average_price * 100
        return round(volatility, 2)

    def _save_volatility(self, volatility):
        if volatility == 0:
            key, data_to_save = 'zero_volatility', self.ticker_id
        else:
            key, data_to_save = 'non-zero_volatility', (self.ticker_id, volatility)
        with self.lock:
            self.tickers[key].append(data_to_save)


@time_track
def main():
    trades_path = r'.\trades'
    file_names = os.listdir(trades_path)
    threads = []
    lock = Lock()
    tickers = {'zero_volatility': [], 'non-zero_volatility': []}

    for file_name in file_names:
        file_path = os.path.join(trades_path, file_name)
        threads.append(VolatilityCalculator(file_path, tickers, lock))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    tickers['zero_volatility'].sort()
    tickers['non-zero_volatility'].sort(key=lambda x: x[1])
    min_volatility_tickers = tickers['non-zero_volatility'][:3]
    max_volatility_tickers = tickers['non-zero_volatility'][-3:]

    print('Максимальная волатильность:')
    for ticker in max_volatility_tickers:
        result = '\t' + f'{ticker[0]} - {ticker[1]}%'
        print(result)

    print('Минимальная волатильность:')
    for ticker in min_volatility_tickers:
        result = '\t' + f'{ticker[0]} - {ticker[1]}%'
        print(result)

    print('Нулевая волатильность:')
    zero_volatility_tickers = ', '.join(tickers['zero_volatility'])
    print('\t' + zero_volatility_tickers)


main()
