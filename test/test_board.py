import unittest

from util.board import *

E = EMPTY
B = BLACK
W = WHITE

class TestBoard(unittest.TestCase):
    def test_place_1(self):
        board = Board(5, 5)
        board.config = [ [E, E, B, W, E],
                         [W, W, B, W, W],
                         [B, B, B, B, B],
                         [W, W, B, W, W],
                         [E, W, B, W, E] ]

        board.place(BLACK, 0, 0)
        self.assertEqual(board.config, [ [B, E, B, W, E],
                                         [W, W, B, W, W],
                                         [B, B, B, B, B],
                                         [W, W, B, W, W],
                                         [E, W, B, W, E]])
        self.assertEqual(board.captures, {BLACK: 0, WHITE: 0})
        self.assertIsNone(board.ko_move)
        self.assertIsNone(board.ko_color)

        board.place(WHITE, 0, 1)
        self.assertEqual(board.config, [ [E, W, E, W, E],
                                         [W, W, E, W, W],
                                         [E, E, E, E, E],
                                         [W, W, E, W, W],
                                         [E, W, E, W, E]])
        self.assertEqual(board.captures, {BLACK: 0, WHITE: 10})
        self.assertIsNone(board.ko_move)
        self.assertIsNone(board.ko_color)

    def test_place_2(self):
        board = Board(5, 5)
        board.config = [ [E, E, B, W, E],
                         [W, W, B, W, W],
                         [B, B, B, B, B],
                         [W, E, B, W, W],
                         [W, W, B, W, E] ]

        board.place(WHITE, 3, 1)
        self.assertEqual(board.config, [ [E, E, B, W, E],
                                         [W, W, B, W, W],
                                         [B, B, B, B, B],
                                         [E, E, B, W, W],
                                         [E, E, B, W, E]])
        self.assertEqual(board.captures, {BLACK: 4, WHITE: 0})
        self.assertIsNone(board.ko_move)
        self.assertIsNone(board.ko_color)

        board.place(BLACK, 4, 4)
        self.assertEqual(board.config, [ [E, E, B, W, E],
                                         [W, W, B, W, W],
                                         [B, B, B, B, B],
                                         [E, E, B, E, E],
                                         [E, E, B, E, B]])
        self.assertEqual(board.captures, {BLACK: 7, WHITE: 0})
        self.assertIsNone(board.ko_move)
        self.assertIsNone(board.ko_color)

    def test_place_3(self):
        board = Board(3, 3)
        board.config = [ [E, E, E],
                         [E, E, E],
                         [E, E, E] ]

        board.place(B, 2, 2)
        board.place(W, 2, 1)
        board.place(B, 1, 1)
        board.place(W, 1, 0)
        self.assertIsNone(board.ko_move)
        self.assertIsNone(board.ko_color)

        board.place(B, 2, 0)
        self.assertEqual(board.ko_move, (2,1))
        self.assertEqual(board.ko_color, WHITE)

        board.place(W, 0, 1)
        self.assertIsNone(board.ko_move)
        self.assertIsNone(board.ko_color)

        board.place(B, 0, 2)
        self.assertIsNone(board.ko_move)
        self.assertIsNone(board.ko_color)

        board.place(W, 1, 2)
        self.assertEqual(board.ko_move, (0,2))
        self.assertEqual(board.ko_color, BLACK)

        board.place(W, 2, 1)
        self.assertIsNone(board.ko_move)
        self.assertIsNone(board.ko_color)

    def test_get_state(self):
        board = Board(5, 5)
        board.config = [ [E, E, B, W, E],
                         [W, W, B, W, W],
                         [B, B, B, B, B],
                         [W, E, B, W, W],
                         [W, W, B, W, E] ]

        self.assertEqual(board.get_state(), '..XO.OOXOOXXXXXO.XOOOOXO.')

    def test_legal_moves(self):
        board = Board(3, 3)
        board.config = [ [E, E, E],
                         [E, E, E],
                         [E, E, E] ]

        moves = set(board.legal_moves(B, suicide_allowed=False))
        self.assertEqual(moves, set([(0,0),(0,1),(0,2),
                                     (1,0),(1,1),(1,2),
                                     (2,0),(2,1),(2,2)]))

        board.place(B, 2, 2)
        moves = set(board.legal_moves(W, suicide_allowed=False))
        self.assertEqual(moves, set([(0,0),(0,1),(0,2),
                                     (1,0),(1,1),(1,2),
                                     (2,0),(2,1)]))

        board.place(W, 2, 1)
        moves = set(board.legal_moves(B, suicide_allowed=False))
        self.assertEqual(moves, set([(0,0),(0,1),(0,2),
                                     (1,0),(1,1),(1,2),
                                     (2,0)]))

        board.place(B, 1, 1)
        board.place(W, 1, 0)
        moves = set(board.legal_moves(B, suicide_allowed=False))
        self.assertEqual(moves, set([(0,0),(0,1),(0,2),(1,2),(2,0)]))

        board.place(B, 2, 0)
        w_moves = set(board.legal_moves(W, suicide_allowed=False))
        self.assertEqual(w_moves, set([(0,0),(0,1),(0,2),(1,2)]))
        b_moves = set(board.legal_moves(B, suicide_allowed=False))
        self.assertEqual(b_moves, set([(0,0),(0,1),(0,2),(1,2),(2,1)]))

        board.place(W, 0, 0)
        w_moves = set(board.legal_moves(W, suicide_allowed=False))
        self.assertEqual(w_moves, set([(0,1),(0,2),(1,2),(2,1)]))
        b_moves = set(board.legal_moves(B, suicide_allowed=False))
        self.assertEqual(b_moves, set([(0,1),(0,2),(1,2),(2,1)]))

        board.place(B, 0, 2)
        w_moves = set(board.legal_moves(W, suicide_allowed=False))
        self.assertEqual(w_moves, set([(2,1)]))
        w_moves_suicide = set(board.legal_moves(W, suicide_allowed=True))
        self.assertEqual(w_moves_suicide, set([(0,1),(2,1)]))
        b_moves = set(board.legal_moves(B, suicide_allowed=False))
        self.assertEqual(b_moves, set([(0,1),(1,2),(2,1)]))

    def test_score(self):
        board = Board(5, 5, komi=-7.0)
        board.config = [ [E, E, B, W, E],
                         [W, W, B, W, W],
                         [B, B, B, B, B],
                         [W, W, B, W, W],
                         [E, W, B, W, E] ]

        board.place(BLACK, 0, 0)
        board.place(WHITE, 0, 1)

        self.assertEqual(board.score(WHITE), 3.0)
        self.assertEqual(board.score(BLACK), -3.0)

        board.set_komi(6.0)
        self.assertEqual(board.score(WHITE), 16.0)
        self.assertEqual(board.score(BLACK), -16.0)

    def test_blocks_1(self):
        board = Board(5, 5)
        board.place(B, 2, 2)
        self.assertEqual(set(board.blocks.keys()), set([(2,2)]))
        self.assertEqual(board.blocks[(2,2)].members, set([(2,2)]))
        self.assertEqual(board.blocks[(2,2)].free_neighbors,
                         set([(1,2),(2,1),(3,2),(2,3)]))
        self.assertFalse(board.blocks[(2,2)].is_in_atari())
        self.assertFalse(board.blocks[(2,2)].is_captured())

    def test_blocks_2(self):
        board = Board(5, 5)
        board.place(B, 2, 2)
        board.place(W, 2, 3)
        self.assertEqual(set(board.blocks.keys()), set([(2,2),(2,3)]))
        self.assertEqual(board.blocks[(2,2)].members, set([(2,2)]))
        self.assertEqual(board.blocks[(2,2)].free_neighbors,
                         set([(1,2),(2,1),(3,2)]))
        self.assertEqual(board.blocks[(2,3)].members, set([2,3]))
        self.assertEqual(board.blocks[(2,3)].free_neighbors,
                         set([(1,3),(2,4),(3,3)]))
        self.assertFalse(board.blocks[(2,2)].is_in_atari())
        self.assertFalse(board.blocks[(2,2)].is_captured())
        self.assertFalse(board.blocks[(2,3)].is_in_atari())
        self.assertFalse(board.blocks[(2,3)].is_captured())

    def test_blocks_3(self):
        board = Board(5, 5)
        board.place(B, 2, 2)
        board.place(W, 2, 3)
        board.place(B, 1, 2)
        self.assertEqual(set(board.blocks.keys()), set([(2,2),(2,3),(1,2)]))
        self.assertEqual(board.blocks[(2,2)], board.blocks[(1,2)])
        self.assertEqual(board.blocks[(2,2)].members, set([(2,2),(1,2)]))
        self.assertEqual(board.blocks[(2,2)].free_neighbors,
                         set([(0,2),(1,3),(1,1),(2,1),(3,2)]))
        self.assertEqual(board.blocks[(2,3)].members, set([2,3]))
        self.assertEqual(board.blocks[(2,3)].free_neighbors,
                         set([(1,3),(2,4),(3,3)]))
        self.assertFalse(board.blocks[(2,2)].is_in_atari())
        self.assertFalse(board.blocks[(2,2)].is_captured())
        self.assertFalse(board.blocks[(2,3)].is_in_atari())
        self.assertFalse(board.blocks[(2,3)].is_captured())

    def test_blocks_4(self):
        board = Board(5, 5)
        board.place(B, 2, 2)
        board.place(W, 2, 3)
        board.place(B, 3, 3)
        board.place(B, 1, 3)
        self.assertTrue(board.blocks[(2,3)].is_in_atari())
        self.assertFalse(board.blocks[(2,3)].is_captured())

    def test_blocks_5(self):
        board = Board(5, 5)
        board.place(B, 2, 2)
        board.place(W, 2, 3)
        board.place(B, 3, 3)
        board.place(B, 1, 3)
        board.place(B, 2, 4)
        self.assertNotIn((2,3), board.blocks)

if __name__ == '__main__':
    unittest.main()
