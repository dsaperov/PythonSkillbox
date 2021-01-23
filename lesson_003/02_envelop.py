# -*- coding: utf-8 -*-

# (if/elif/else)

# Заданы размеры envelop_x, envelop_y - размеры конверта и paper_x, paper_y листа бумаги
#
# Определить, поместится ли бумага в конверте (стороны листа параллельны сторонам конверта)
#
# Результат проверки вывести на консоль (ДА/НЕТ)
# Использовать только операторы if/elif/else, можно вложенные

envelop_x, envelop_y = 10, 7
paper_x, paper_y = 8, 9
# проверить для
# paper_x, paper_y = 9, 8
# paper_x, paper_y = 6, 8
# paper_x, paper_y = 8, 6
# paper_x, paper_y = 3, 4
# paper_x, paper_y = 11, 9
# paper_x, paper_y = 9, 11
# (просто раскоментировать нужную строку и проверить свой код)

if paper_x <= envelop_x:
    if paper_y <= envelop_y:
        print('ДА')
    else:
        if paper_y <= envelop_x:
            if paper_x <= envelop_y:
                print('ДА')
            else:
                print('НЕТ')
        else:
            print('НЕТ')
else:
    if paper_x <= envelop_y:
        if paper_y <= envelop_x:
            print('ДА')
        else:
            print('НЕТ')
    else:
        print('НЕТ')
