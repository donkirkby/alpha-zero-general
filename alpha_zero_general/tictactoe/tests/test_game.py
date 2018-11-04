import numpy as np

from alpha_zero_general.tictactoe.TicTacToeGame import TicTacToeGame


def test():
    expected_moves = np.array([1] * 9 + [0])

    game = TicTacToeGame()
    moves = game.getValidMoves(game.getInitBoard(), player=1)

    assert all(expected_moves == moves)


def test_start_moves():
    expected_moves = np.array([1] * 9 + [0])

    game = TicTacToeGame()
    moves = game.getValidMoves(game.getInitBoard(), player=1)

    assert all(expected_moves == moves)


def test_display():
    expected_display = """\
   0 1 2
  --------
0 |- - - |
1 |- - - |
2 |- - - |
  --------
"""

    game = TicTacToeGame()
    board = game.getInitBoard()
    display_text = game.display(board)

    assert expected_display == display_text


def test_next_state():
    expected_display = """\
   0 1 2
  --------
0 |O - - |
1 |X - - |
2 |- - - |
  --------
"""

    game = TicTacToeGame()
    board1 = game.getInitBoard()
    board2, player2 = game.getNextState(board1, player=1, action=0)
    board3, _ = game.getNextState(board2, player=player2, action=3)
    display_text = game.display(board3)

    assert expected_display == display_text


def test_parse():
    state_text = """\
O - -
X X -
- - O
"""
    expected_display = """\
   0 1 2
  --------
0 |O - - |
1 |X X - |
2 |- - O |
  --------
"""
    game = TicTacToeGame()
    board = game.parse_board(state_text)

    display_text = game.display(board)

    assert expected_display == display_text
