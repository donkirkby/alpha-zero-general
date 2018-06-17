from argparse import ArgumentParser

from alpha_zero_general.pit import pit
from alpha_zero_general.train import train


def parse_args():
    parser = ArgumentParser(description='AlphaZero for any game')
    parser.set_defaults(handler=parser.print_usage)
    subparsers = parser.add_subparsers(description='AlphaZero actions')

    train_parser = subparsers.add_parser(
        'train',
        help='Train a model',
        description='Train a model by alternating self play and learning.')
    train_parser.set_defaults(handler=train)

    pit_parser = subparsers.add_parser(
        'pit',
        help='Pit two players against each other',
        description='Pit two players against each other in two games.')
    pit_parser.set_defaults(handler=pit)

    return parser.parse_args()


def main():
    args = parse_args()

    args.handler()


main()
