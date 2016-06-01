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
        self.board = Board(rows, cols, komi, suicide_allowed)
        self.pass_allowed = pass_allowed
        self.states_visited = set()
        self.init_mcts(BLACK)

    def init_mcts(self, color):
        self.mcts = MCTS(self.playouts, lambda x: int(x>0), 1.0)

    def reset_game(self):
        self.board.reset()
        self.states_visited = set()
        self.init_mcts(BLACK)

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
        self.mcts.move_root(color, (row, col))
        return True

    def gen_move(self, color):
        moves = self.mcts.search(self.board, self.states_visited, color)
        move =  self.make_move(color, moves)
        if move != RESIGN:
            self.mcts.move_root(color, move)

        return move

    def make_move(self, color, moves):
        for move in moves:
            if move == PASS:
                if self.pass_allowed:
                    return PASS
                else:
                    continue

            board = copy.deepcopy(self.board)
            board.place(color, move[0], move[1])

            state = board.get_state()
            if state in self.states_visited:
                continue

            self.board = board
            self.states_visited.add(state)
            return move
        return RESIGN

    def place_pass(self, color):
        pass

    def show_board(self):
        return str(self.board)
