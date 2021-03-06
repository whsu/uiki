from util.const import *
from util.board import *
from uiki.player import *

from .atari_mcts import *

class AtariPlayer(Player):
    __name__ = 'omnomnom'
    __version__ = '0.2'

    def __init__(self, playouts=1000):
        super(AtariPlayer, self).__init__(playouts)

    def new_game(self, rows, cols, num_caps=1, komi=6.5,
                 suicide_allowed=False, pass_allowed=True):
        self.num_caps = num_caps
        super(AtariPlayer, self).new_game(rows, cols, komi, suicide_allowed, pass_allowed)

    def init_mcts(self, color):
        self.mcts = AtariMCTS(self.playouts, lambda x: int(x>0), 1.0, self.num_caps)

    def gen_move(self, color):
        oppcolor = opponent(color)
        if self.board.captures[oppcolor] >= self.num_caps:
            return RESIGN

        return super(AtariPlayer, self).gen_move(color)
