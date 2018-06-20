import os

from alpha_zero_general.utils import imported_argument
from .Coach import Coach


def config_parser(parser):
    parser.set_defaults(handler=train)
    parser.add_argument(
        'game',
        nargs='?',
        type=imported_argument,
        default='alpha_zero_general.othello.OthelloGame.OthelloGame',
        help='game class with rules')
    parser.add_argument(
        'network',
        nargs='?',
        type=imported_argument,
        default='alpha_zero_general.othello.pytorch.NNet.NNetWrapper',
        help='neural network class to train')
    parser.add_argument(
        '--num_iters',
        type=int,
        default=1000,
        help='number of iterations of self play and learning')
    parser.add_argument(
        '--episodes',
        type=int,
        default=100,
        help='number of episodes of self play per iteration')
    parser.add_argument(
        '--temp_threshold',
        type=int,
        default=15,
        help='number of episodes with temp 1 before switching to 0')
    parser.add_argument(
        '--update_threshold',
        type=float,
        default=0.6,
        help='minimum win ratio to update neural network')
    parser.add_argument(
        '--maxlen_of_queue',
        type=int,
        default=200000,
        help='number of game states from each episode to save for training')
    parser.add_argument(
        '--num_mcts_sims',
        type=int,
        default=25,
        help='number of Monte Carlo Tree Search simulations before each move')
    parser.add_argument(
        '--arena_compare',
        type=int,
        default=40,
        help='number of games to play before deciding to update neural network')
    parser.add_argument(
        '--cpuct',
        type=float,
        default=1.0,
        help='a hyperparameter that controls the degree of exploration')
    parser.add_argument(
        '--checkpoint',
        default='./temp/',
        help='folder to store checkpoint data as neural network improves')
    parser.add_argument(
        '--load_model',
        help='checkpoint file to resume from, like /path/to/best.pth.tar')
    parser.add_argument(
        '--num_iters_for_train_examples_history',
        type=int,
        default=20,
        help='number of episodes to keep training data from')


def train(args):
    g = args.game()
    nnet = args.network(g)

    if args.load_model:
        nnet.load_checkpoint(os.path.dirname(args.load_model),
                             os.path.basename(args.load_model))

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
