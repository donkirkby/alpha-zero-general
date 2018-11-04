from __future__ import print_function
import sys
from io import StringIO

sys.path.append('..')
from alpha_zero_general.Game import Game
from .TicTacToeLogic import Board
import numpy as np

"""
Game class implementation for the game of TicTacToe.
Based on the OthelloGame then getGameEnded() was adapted to new rules.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloGame by Surag Nair.
"""


class TicTacToeGame(Game):
    def __init__(self, n=3):
        super().__init__()
        self.n = n

    def parse_board(self, text):
        piece_players = {'O': 1, 'X': -1, '-': 0}
        board = self.getInitBoard()
        for i, line in enumerate(text.splitlines()):
            for j in range(self.n):
                c = line[j*2]
                player = piece_players[c]
                board[i][j] = player
        return board

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n*self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action/self.n), action%self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n*x+y]=1
        return np.array(valids)

    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)

        if b.is_win(player):
            return 1
        if b.is_win(-player):
            return -1
        if b.has_legal_moves():
            return 0
        # draw has a very little value 
        return 1e-4

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    def display(self, board):
        buffer = StringIO()
        display(board, buffer)
        return buffer.getvalue()


def display(board, file=None):
    n = board.shape[0]

    print("  ", end="", file=file)
    for y in range(n):
        print("", y, end="", file=file)
    print("", file=file)
    print("  ", end="", file=file)
    for _ in range(n):
        print ("-", end="-", file=file)
    print("--", file=file)
    for y in range(n):
        print(y, "|", end="", file=file)    # print the row #
        for x in range(n):
            piece = board[y][x]    # get the piece to print
            if piece == -1: print("X ", end="", file=file)
            elif piece == 1: print("O ", end="", file=file)
            else:
                if x==n:
                    print("-", end="", file=file)
                else:
                    print("- ", end="", file=file)
        print("|", file=file)

    print("  ", end="", file=file)
    for _ in range(n):
        print ("-", end="-", file=file)
    print("--", file=file)
