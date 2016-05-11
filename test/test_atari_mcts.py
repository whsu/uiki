import unittest

from util.board import *
from omnomnom.atari_mcts import *

class TestMCTS(unittest.TestCase):
    def test_search_1(self):
            board = Board(3,3)
            visited = set()
            color = BLACK
            num_sims = 10000
            score_func = lambda x: int(x>0)
            exp_const = 1.0
            m = AtariMCTS(board, visited, color, num_sims, score_func, exp_const, 1)

            self.assertEqual(m.search()[0], (1,1))

if __name__ == '__main__':
    unittest.main()
