import os
from argparse import Namespace
from pathlib import Path

from alpha_zero_general.play import RemotePlayerClient
from . import Arena
from .MCTS import MCTS

import numpy as np
from alpha_zero_general.utils import imported_argument

"""
Use this script to play any two agents against each other, or play manually with
any agent.
"""


def config_parser(parser):
    parser.set_defaults(handler=pit)
    parser.add_argument(
        'game',
        nargs='?',
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
        '--remote_path',
        type=Path,
        help='Path to another copy of the project to run player 2.')
    group = parser.add_argument_group(
        'players',
        'These options can accept one or two values. Use one value if it should '
        'be used by both players.')
    group.add_argument(
        '--players',
        nargs='*',
        default=['alpha_zero_general.pit.MCTSPlayer'],
        help='classes to choose moves for player 1 and 2')
    group.add_argument(
        '--networks',
        nargs='*',
        default=['alpha_zero_general.othello.pytorch.NNet.NNetWrapper'],
        help='neural network classes to use for player 1 and 2 if they are MCTS')
    group.add_argument(
        '--num_mcts_sims',
        nargs='*',
        type=int,
        default=[25],
        help='number of Monte Carlo Tree Search simulations before each move '
             'for player 1 and 2 if they are MCTS')
    group.add_argument(
        '--cpucts',
        nargs='*',
        type=float,
        default=[1.0],
        help='a hyperparameter that controls the degree of exploration '
             'for player 1 and 2')
    group.add_argument(
        '--load_models',
        nargs='*',
        default=['./temp/best.pth.tar'],
        help='checkpoint file to load neural network model from for player 1')


def split_args(args):
    args1, args2 = Namespace(), Namespace()
    for name, value in args.__dict__.items():
        if name.startswith('_'):
            continue
        if not name.endswith('s'):
            target_name = name
            value1 = value2 = value
        else:
            target_name = name[:-1] if name != 'num_mcts_sims' else name
            if len(value) == 1:
                value1 = value2 = value[0]
            else:
                value1, value2 = value
        setattr(args1, target_name, value1)
        setattr(args2, target_name, value2)
    return args1, args2


class MCTSPlayer:
    def __init__(self, game, args):
        self.game = game
        network = imported_argument(args.network)(game)
        folder, filename = os.path.split(args.load_model)
        network.load_checkpoint(folder, filename)
        self.mcts = MCTS(game, network, args)

    def play(self, board):
        return np.argmax(self.mcts.getActionProb(board, temp=0))


def pit(args):
    args1, args2 = split_args(args)
    g = imported_argument(args.game)()

    player1 = imported_argument(args1.player)(g, args1).play
    if args.remote_path is None:
        player2 = imported_argument(args2.player)(g, args2).play
    else:
        player2 = RemotePlayerClient(args2).play

    arena = Arena.Arena(player1, player2, g, display=args.display)
    print(arena.playGames(args.game_count, verbose=not args.quiet))
