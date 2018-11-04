""" Run a player, receiving game states on stdin and sending moves on stdout. """
from json import dumps, loads
from sys import stdin, stdout
from traceback import format_exception_only

import numpy as np
from subprocess import Popen, PIPE

import sys

from alpha_zero_general.utils import imported_argument


class RemotePlayerServer:
    def __init__(self, in_file=stdin, out_file=stdout):
        self.in_file = in_file
        self.out_file = out_file
        self.next_player = 1
        self.game = self.player = None

    def run(self):
        for line in self.in_file:
            try:
                request = loads(line)
                command = request.pop('command')
                method = getattr(self, command)
                response = method(**request)
                print(dumps(response), file=self.out_file)
            except Exception as ex:
                message = "".join(format_exception_only(ex.__class__, ex)).strip()
                print(dumps(dict(error=message)), file=self.out_file)

    def start(self, game, player):
        game_class = imported_argument(game)
        self.game = game_class()
        player_class = imported_argument(player)
        self.player = player_class(self.game)
        return {}

    def move(self, board):
        board_array = np.array(board)
        next_action = self.player.play(board_array)
        return dict(action=int(next_action))


class RemotePlayerClient:
    def __init__(self, args):
        command = dict(args.__dict__)
        command['command'] = 'start'
        remote_path = command.pop('remote_path')
        self.process = Popen([sys.executable, '-m', 'alpha_zero_general.play'],
                             stdin=PIPE,
                             stdout=PIPE,
                             cwd=remote_path)
        self.send(command)

    def play(self, board):
        response = self.send(dict(command='move',
                                  board=board.tolist()))
        return response['action']

    def send(self, request):
        text = dumps(request) + '\n'
        self.process.stdin.write(text.encode())
        self.process.stdin.flush()
        response = self.process.stdout.readline()
        return loads(response)


def main():
    server = RemotePlayerServer()
    server.run()


if __name__ == '__main__':
    main()
