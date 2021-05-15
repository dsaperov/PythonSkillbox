# -*- coding: utf-8 -*-
import logging

log = logging.getLogger('primes')
print('создан объект логирования для primes')


def prime_numbers_generator(n):
    prime_numbers = []
    for number in range(2, n + 1):
        log.debug(f'number {number}')
        for prime in prime_numbers:
            if number % prime == 0:
                log.debug(f'делится на {prime}')
                break
        else:
            log.debug(f'найдено новое простое {number}')
            prime_numbers.append(number)
            yield number


