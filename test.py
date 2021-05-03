import argparse

parser = argparse.ArgumentParser(
    description='glean the data from the command line')
parser.add_argument('fio', type=str)
parser.add_argument(
    '--log', default=sys.stdout, type=argparse.FileType('w'),
    help='the file where the sum should be written')
args = parser.parse_args()
args.log.write('%s' % sum(args.integers))
args.log.close()