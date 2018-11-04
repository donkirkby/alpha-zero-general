from argparse import Namespace
from io import StringIO
from pathlib import Path

import pytest

from alpha_zero_general.play import RemotePlayerServer, RemotePlayerClient, RemoteException
from alpha_zero_general.tictactoe.TicTacToeGame import TicTacToeGame


def test_second_player():
    in_file = StringIO("""\
{"command": "start", \
"game": "alpha_zero_general.tictactoe.TicTacToeGame.TicTacToeGame", \
"player": "alpha_zero_general.tictactoe.TicTacToePlayers.FirstChoicePlayer"}
{"command": "move", "board": [[1, 0, 0], [0, 0, 0], [0, 0, 0]]}
{"command": "move", "board": [[1, -1, 0], [1, 0, 0], [0, 0, 0]]}
""")
    out_file = StringIO()
    expected_out = """\
{}
{"action": 1}
{"action": 2}
"""
    server = RemotePlayerServer(in_file, out_file)
    server.run()

    assert expected_out == out_file.getvalue()


def test_first_player():
    in_file = StringIO("""\
{"command": "start", \
"game": "alpha_zero_general.tictactoe.TicTacToeGame.TicTacToeGame", \
"player": "alpha_zero_general.tictactoe.TicTacToePlayers.FirstChoicePlayer"}
{"command": "move", "board": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]}
{"command": "move", "board": [[-1, 1, 0], [0, 0, 0], [0, 0, 0]]}
""")
    out_file = StringIO()
    expected_out = """\
{}
{"action": 0}
{"action": 2}
"""
    server = RemotePlayerServer(in_file, out_file)
    server.run()

    assert expected_out == out_file.getvalue()


def test_error():
    in_file = StringIO("""\
{"command": "bogus"}
""")
    out_file = StringIO()
    expected_out = """\
{"error": "AttributeError: 'RemotePlayerServer' object has no attribute 'bogus'"}
"""
    server = RemotePlayerServer(in_file, out_file)
    server.run()

    assert expected_out == out_file.getvalue()


def test_client():
    remote_path = Path(__file__).parent.parent.parent
    args = Namespace(
        game="alpha_zero_general.tictactoe.TicTacToeGame.TicTacToeGame",
        player="alpha_zero_general.tictactoe.TicTacToePlayers.FirstChoicePlayer",
        remote_path=remote_path)
    client = RemotePlayerClient(args)
    game = TicTacToeGame()
    board = game.getInitBoard()
    expected_action = 0

    action = client.play(board)

    assert expected_action == action


def test_client_error():
    remote_path = Path(__file__).parent.parent.parent
    args = Namespace(
        game="alpha_zero_general.tictactoe.TicTacToeGame.BogusGame",
        player="alpha_zero_general.tictactoe.TicTacToePlayers.FirstChoicePlayer",
        remote_path=remote_path)
    with pytest.raises(RemoteException, match='attribute BogusGame not found'):
        RemotePlayerClient(args)
