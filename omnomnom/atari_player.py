from util.const import *
from util.board import *
from uiki.player import *

from .atari_mcts import *

class AtariPlayer(Player):
    __name__ = 'omnomnom'
    __version__ = '0.1'

    def __init__(self, num_caps=1, rows=19, cols=19, komi=6.5,
                       suicide_allowed=False, playouts=1000):
        super(AtariPlayer, self).__init__(rows, cols, komi, suicide_allowed,
                                          playouts, pass_allowed=False)
        self.num_caps = num_caps

    def gen_move(self, color):
        oppcolor = opponent(color)
        if self.board.captures[oppcolor] >= self.num_caps:
            return RESIGN

        return super(AtariPlayer, self).gen_move(color)

    def create_mcts_searcher(self, color):
        k = self.komi if color==BLACK else -self.komi
        m = AtariMCTS(self.board, self.states_visited, color, self.playouts,
                 lambda x: int(x>k), 1.0, self.num_caps)
        return m
