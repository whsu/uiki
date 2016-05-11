import unittest

from omnomnom.atari_player import *

B = BLACK
W = WHITE
E = EMPTY

class TestAtariPlayer(unittest.TestCase):
    def test_place_move(self):
        player = AtariPlayer(1, 2, 3, suicide_allowed=False)
        result = player.place_move(BLACK, 1, 2)

        self.assertTrue(result)
        self.assertEqual(player.board.config, [[E,E,E],
                                               [E,E,B]])
        self.assertEqual(player.states_visited, set(['.....X']))

        result = player.place_move(WHITE, 1, 2)
        self.assertFalse(result)
        self.assertEqual(player.board.config, [[E,E,E],
                                               [E,E,B]])
        self.assertEqual(player.states_visited, set(['.....X']))

        player.place_move(WHITE, 1, 1)
        player.place_move(WHITE, 0, 2)
        self.assertEqual(player.board.config, [[E,E,W],
                                               [E,W,E]])
        self.assertEqual(player.states_visited, set(['.....X','....OX','..O.O.']))

if __name__ == '__main__':
    unittest.main()
