from random import randint
dices = [1, 2]

print((lambda dice: dice in dices)(randint(1, 2)))
