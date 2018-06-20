from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from alpha_zero_general import pit
from alpha_zero_general import train


def parse_args():
    parser = ArgumentParser(description='AlphaZero for any game',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.set_defaults(handler=lambda args: parser.print_usage())
    subparsers = parser.add_subparsers(description='AlphaZero actions')

    train.config_parser(subparsers.add_parser(
        'train',
        help='Train a model',
        description='Train a model by alternating self play and learning.'))

    pit.config_parser(subparsers.add_parser(
        'pit',
        help='Pit two players against each other',
        description='Pit two players against each other in two games.'))

    return parser.parse_args()


def main():
    args = parse_args()

    args.handler(args)


main()
