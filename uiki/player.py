import copy

from util.const import *
from util.board import *
from .mcts import *

class Player:
    __name__ = 'Uiki'
    __version__ = '0.2-dev'

    def __init__(self, playouts=1000):
        self.playouts = playouts

    def new_game(self, rows, cols, komi=6.5, suicide_allowed=False, pass_allowed=True):
        self.board = Board(rows, cols, komi)
        self.suicide_allowed = suicide_allowed
        self.pass_allowed = pass_allowed
        self.states_visited = set()

    def reset_game(self):
        self.board.reset()
        self.states_visited = set()

    def set_komi(self, komi):
        self.board.set_komi(komi)

    def place_move(self, color, row, col):
        '''Place a given move on the board and return True if move is legal.
           Return False if move is illegal.'''
        if self.board[row,col] != EMPTY:
            return False

        self.board.place(color, row, col)
        newstate = self.board.get_state()
        self.states_visited.add(newstate)
        return True

    def gen_move(self, color):
        m = self.create_mcts_searcher(color)
        moves = m.search(self.board, self.states_visited, color)
        move = moves[0]
        for move in moves:
            if move == PASS:
                if self.pass_allowed:
                    return PASS
                else:
                    continue

            board = copy.deepcopy(self.board)
            captured = board.place(color, move[0], move[1])

            if len(captured[color]) > 0 and not self.suicide_allowed:
                continue

            state = board.get_state()
            if state in self.states_visited:
                continue

            self.board = board
            self.states_visited.add(self.board.get_state())
            return move
        return RESIGN

    def create_mcts_searcher(self, color):
        m = MCTS(self.playouts, lambda x: int(x>0), 1.0)
        return m

    def place_pass(self, color):
        pass

    def show_board(self):
        return str(self.board)
