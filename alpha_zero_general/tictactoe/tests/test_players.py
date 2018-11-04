from alpha_zero_general.tictactoe.TicTacToeGame import TicTacToeGame
from alpha_zero_general.tictactoe.TicTacToePlayers import FirstChoicePlayer


def test_first_choice():
    state_text = """\
O - -
X X -
- - O
"""
    game = TicTacToeGame()
    start_board = game.parse_board(state_text)
    player = FirstChoicePlayer(game)
    expected_display = """\
   0 1 2
  --------
0 |O O - |
1 |X X - |
2 |- - O |
  --------
"""

    action = player.play(start_board)
    next_board, _ = game.getNextState(start_board, player=1, action=action)
    display_text = game.display(next_board)

    assert expected_display == display_text
