# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

from PIL import Image, ImageFont, ImageDraw, ImageColor


class TicketDraft:

    def __init__(self, fio, from_, to, date, font_path):
        self.fio = fio
        self.from_ = from_
        self.to = to
        self.date = date
        self.font = ImageFont.truetype(font_path, 15)
        self.ticket_template = "images/ticket_template.png"

    def make_ticket(self):
        im = Image.open(self.ticket_template)

        draw = ImageDraw.Draw(im)
        draw.text((45, 125), text=self.fio, font=self.font, fill='black')
        draw.text((45, 195), text=self.from_, font=self.font, fill='black')
        draw.text((45, 260), text=self.to, font=self.font, fill='black')
        draw.text((285, 260), text=self.date, font=self.font, fill='black')

        im.save(self.fio + '_ticket.png')
        print('Билет сохранен.')


if __name__ == '__main__':
    TicketDraft('ИВАНОВ И.И.', 'ЗЕМЛЯ', 'ЛУНА', '09.12', "fonts/ofont.ru_Plumb.ttf").make_ticket()

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля agrparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
