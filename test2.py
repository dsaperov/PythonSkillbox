# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

from PIL import Image, ImageFont, ImageDraw
import argparse


class TicketDraft:

    def __init__(self, fio, from_, to, date, save_to):
        self.fio = fio
        self.from_ = from_
        self.to = to
        self.date = date
        self.font = ImageFont.truetype("fonts/ofont.ru_LagunaC.ttf", 15)
        self.ticket_template = "images/ticket_template.png"
        self.save_to = save_to if save_to else self.fio + '_ticket.png'

    def make_ticket(self):
        im = Image.open(self.ticket_template)

        draw = ImageDraw.Draw(im)
        draw.text((45, 125), text=self.fio, font=self.font, fill='black')
        draw.text((45, 195), text=self.from_, font=self.font, fill='black')
        draw.text((45, 260), text=self.to, font=self.font, fill='black')
        draw.text((285, 260), text=self.date, font=self.font, fill='black')

        im.save(self.save_to)
        print('Билет сохранен.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='glean the data from the command line')

    args_names = ['fio', 'from_', 'to', 'date', 'save_to']
    args_help = ['ФИО пассажира', 'Место вылета', 'Место назначения', 'Дата вылета']
    for arg_name, args_help in zip(args_names[0:4], args_help):
        parser.add_argument(f'--{arg_name}', help=args_help)
    parser.add_argument('--save_to', required=False, help='Сохранить как')

    args = parser.parse_args()
    fio, from_, to, date, save_to = [getattr(args, arg) for arg in args_names]

    TicketDraft(fio, from_, to, date, save_to).make_ticket()

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля agrparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
