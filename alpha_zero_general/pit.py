import os
from argparse import Namespace

from . import Arena
from .MCTS import MCTS

import numpy as np
from alpha_zero_general.utils import imported_argument

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""


def config_parser(parser):
    parser.set_defaults(handler=pit)
    parser.add_argument(
        'game',
        nargs='?',
        type=imported_argument,
        default='alpha_zero_general.othello.OthelloGame.OthelloGame',
        help='game class with rules')
    parser.add_argument(
        '--display',
        type=imported_argument,
        default='alpha_zero_general.othello.OthelloGame.display',
        help='function to display the game')
    parser.add_argument(
        '--game_count',
        type=int,
        default=2,
        help='number of games to play')
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='turns off game display')
    parser.add_argument(
        '--player1',
        type=imported_argument,
        help='class to choose moves for player 1, if not MCTS')
    parser.add_argument(
        '--player2',
        type=imported_argument,
        help='class to choose moves for player 2, if not MCTS')
    parser.add_argument(
        '--network1',
        type=imported_argument,
        default='alpha_zero_general.othello.pytorch.NNet.NNetWrapper',
        help='neural network class to use for player 1 if it is MCTS')
    parser.add_argument(
        '--network2',
        type=imported_argument,
        help='neural network class to use for player 2, if different')
    parser.add_argument(
        '--num_mcts_sims1',
        type=int,
        default=25,
        help='number of Monte Carlo Tree Search simulations before each move '
             'for player 1 if it is MCTS')
    parser.add_argument(
        '--num_mcts_sims2',
        type=int,
        help='number of Monte Carlo Tree Search simulations before each move '
             'for player 2, if different')
    parser.add_argument(
        '--cpuct1',
        type=float,
        default=1.0,
        help='a hyperparameter that controls the degree of exploration '
             'for player 1')
    parser.add_argument(
        '--cpuct2',
        type=float,
        help='a hyperparameter that controls the degree of exploration '
             'for player 2, if different')
    parser.add_argument(
        '--load_model1',
        default='./temp/best.pth.tar',
        help='checkpoint file to load neural network model from for player 1')
    parser.add_argument(
        '--load_model2',
        help='checkpoint file to load neural network model from for player 2, '
             'if different')


def split_args(args):
    args1, args2 = Namespace(), Namespace()
    for name, value in args.__dict__.items():
        if name.startswith('_'):
            continue
        if name is 'player1':
            args1.player = value
        elif name is 'player2':
            args2.player = value
        elif name.endswith('1'):
            base_name = name[:-1]
            value2 = getattr(args, base_name+'2', value)
            if value2 is None:
                value2 = value
            setattr(args1, base_name, value)
            setattr(args2, base_name, value2)
        elif not name.endswith('2'):
            setattr(args1, name, value)
            setattr(args2, name, value)
    return args1, args2


def create_player(args, game):
    if args.player is not None:
        return args.player(game).play

    # MCTS players
    network = args.network(game)
    folder, filename = os.path.split(args.load_model)
    network.load_checkpoint(folder, filename)
    mcts = MCTS(game, network, args)
    return lambda x: np.argmax(mcts.getActionProb(x, temp=0))


def pit(args):
    args1, args2 = split_args(args)
    g = args.game()

    # noinspection PyTypeChecker
    player1 = create_player(args1, g)
    # noinspection PyTypeChecker
    player2 = create_player(args2, g)

    arena = Arena.Arena(player1, player2, g, display=args.display)
    print(arena.playGames(args.game_count, verbose=not args.quiet))
