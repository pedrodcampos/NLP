import argparse
parser = argparse.ArgumentParser()
parser.add_argument('args', nargs='?')
args = parser.parse_args()
if args.args == 'setup':
    print('po')
