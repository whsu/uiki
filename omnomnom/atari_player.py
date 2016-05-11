from uiki.player import *

from .atari_mcts import *

class AtariPlayer(Player):
    __name__ = 'omnomnom'
    __version__ = '0.1'

    def __init__(self, board, visited, color, num_sims, score_func, exp_const,
                       num_caps):
        super(AtariMCTS, self).__init__(
                  board, visited, color, num_sims, score_func, exp_const)
        self.num_caps = num_caps

    def __init__(self, num_caps=1, rows=19, cols=19, komi=6.5,
                       suicide_allowed=False, playouts=1000):
        super(AtariPlayer, self).__init__(rows, cols, komi, suicide_allowed, playouts)
        self.num_caps = num_caps

    def create_mcts_searcher(self, color):
        k = self.komi if color==BLACK else -self.komi
        m = AtariMCTS(self.board, self.states_visited, color, self.playouts,
                 lambda x: int(x>k), 1.0, self.num_caps)
        return m
