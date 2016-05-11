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

    def test_resign(self):
        player = AtariPlayer(2, 3, 3, suicide_allowed=False)
        player.place_move(BLACK, 1, 2)
        player.place_move(WHITE, 2, 2)
        player.place_move(BLACK, 2, 1)
        move = player.gen_move(WHITE)
        self.assertNotEqual(move, RESIGN)

        player.reset_game()
        player.place_move(BLACK, 1, 2)
        player.place_move(WHITE, 2, 2)
        player.place_move(BLACK, 2, 1)
        player.place_move(WHITE, 2, 0)
        player.place_move(BLACK, 1, 0)
        move = player.gen_move(WHITE)
        self.assertEqual(move, RESIGN)

if __name__ == '__main__':
    unittest.main()
