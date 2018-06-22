from distutils.core import setup

setup(name='alpha_zero_general',
      version='0.1',
      description='A clean implementation based on AlphaZero for any game in '
                  'any framework + tutorial + Othello/Gobang/TicTacToe/Connect4',
      author='Surag Nair',
      url='https://github.com/suragnair/alpha-zero-general',
      packages=['alpha_zero_general',
                'alpha_zero_general/connect4',
                'alpha_zero_general/connect4/tensorflow',
                'alpha_zero_general/gobang',
                'alpha_zero_general/othello',
                'alpha_zero_general/tictactoe',
                'alpha_zero_general/pytorch_classification/utils'],
      install_requires=['numpy', 'progress'],
      scripts=['alpha_zero_general/alpha_zero.py'])
