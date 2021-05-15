import logging

from primes import prime_numbers_generator

main_log = logging.getLogger('main')
print('создан объект логирования для main')


def print_primes(n):
    for prime in prime_numbers_generator(n):
        main_log.info(f'Простое из генераторв {prime}')
