import argparse
from pprint import pprint

parser = argparse.ArgumentParser(description='glean the data from the command line')

args_names = ['fio', 'from_', 'to', 'date', 'save_to']
args_help = ['ФИО пассажира', 'Место вылета', 'Место назначения', 'Дата вылета']
for arg_name, args_help in zip(args_names[0:4], args_help):
    parser.add_argument(f'--{arg_name}', help=args_help)
parser.add_argument('--save_to', required=False, help='Сохранить как')

args = parser.parse_args()

fio, from_, to, date, save_to = [getattr(args, arg) for arg in args_names]

for arg in (fio, from_, to, date, save_to):
    print(arg)
















