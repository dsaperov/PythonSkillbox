# -*- coding: utf-8 -*-

# Составить список всех живущих на районе и Вывести на консоль через запятую
# Формат вывода: На районе живут ...
# подсказка: для вывода элементов списка через запятую можно использовать функцию строки .join()
# https://docs.python.org/3/library/stdtypes.html#str.join


########################################################################################################################
# Импорт неабсолютный и неотносительный ################################################################################
########################################################################################################################

# Импорт всего модуля - вариант #1
# import district.central_street.house1.room1

# Импорт всего модуля - вариант #2 (предпочтительный)
# from district.central_street.house1 import room1

# Импорт элемента модуля
# from district.central_street.house1.room1 import folks


########################################################################################################################
# Абсолютный импорт ####################################################################################################
########################################################################################################################


# Импорт всего модуля - вариант #1
# import lesson_005.district.central_street.house1.room1

# Импорт всего модуля - вариант #2 (предпочтительный)
# from lesson_005.district.central_street.house1 import room1

# Импорт элемента модуля
# from lesson_005.district.central_street.house1.room1 import folks

# Импорт неабсолютный и неотносительный
from district.central_street.house1.room1 import folks as f1
from district.central_street.house1.room2 import folks as f2
from district.central_street.house2.room1 import folks as f3
from district.central_street.house2.room2 import folks as f4
from district.soviet_street.house1.room1 import folks as f5
from district.soviet_street.house1.room2 import folks as f6
from district.soviet_street.house2.room1 import folks as f7
from district.soviet_street.house2.room2 import folks as f8

rooms = [f1, f2, f3, f4, f5, f6, f7, f8]
folks = []
for room in rooms:
    folks.extend(room)

folks_string = ', '.join(folks)
print('На районе живут:', folks_string)