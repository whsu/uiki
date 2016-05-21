import math
import copy
import random

from util.const import *
from util.board import *

class Node:
    def __init__(self, color):
        self.color = color
        self.total = 0.0;
        self.count = 0;
        self.children = {}

    def update(self, value):
        self.total += value
        self.count += 1

    def value(self):
        return self.total / self.count

    def possible_moves(self, board):
        for pos in board.legal_moves(self.color):
            yield pos
        yield PASS

    def move_values(self, board, root_color, c):
        values = {}
        for pos in self.possible_moves(board):
            if pos in self.children:
                child = self.children[pos]
                v = child.value()
                if self.color != root_color:
                    v = -v
                values[pos] = v + c * math.sqrt(
                                math.log(self.count+1) / (child.count+1) )
            else:
                values[pos] = c * math.sqrt(math.log(self.count+1))
        return values

    def select_move(self, board, root_color, c):
        values = self.move_values(board, root_color, c)
        return max(values, key=lambda move:values[move])

    def select_moves(self, board, root_color, c):
        values = self.move_values(board, root_color, c)
        return sorted(values, key=lambda move:-values[move])

class MCTS:
    def __init__(self, board, visited, color, num_sims, score_func, exp_const):
        self.board = board
        self.visited = visited
        self.num_sims = num_sims
        self.score_func = score_func
        self.exp_const = exp_const
        self.max_depth = board.size()*2
        self.root = Node(color)

    def search(self):
        for k in range(self.num_sims):
            board, node, moves, visited, outcome = self.simulate_tree()
            if outcome is None:
                outcome = self.simulate_default(board, node.color, visited)
            self.update_tree(moves, outcome)

        return self.root.select_moves(self.board, self.root.color, 0)

    def simulate_tree(self):
        board = copy.deepcopy(self.board)
        visited = copy.copy(self.visited)
        moves = []
        outcome = None

        node = self.root
        while node.count > 0 and outcome is None:
            move = node.select_move(board, self.root.color, self.exp_const)
            moves.append(move)

            if move not in node.children:
                node.children[move] = Node(opponent(node.color))
            child = node.children[move]

            if move != PASS:
                outcome = self.place_move(board, node.color, move, visited)

            node = child

        return board, node, moves, visited, outcome

    def simulate_default(self, board, color, visited):
        outcome = None
        while len(visited) < self.max_depth and outcome is None:
            move = self.default_move(board, color)
            outcome = self.place_move(board, color, move, visited)
            color = opponent(color)

        if outcome is None:
            return board.score(self.root.color)
        else:
            return outcome

    def place_move(self, board, color, move, visited):
        board.place(color, move[0], move[1])
        state = board.get_state()
        if state in visited:
            outcome = self.repeat_outcome(color)
        else:
            visited.add(state)
            outcome = None
        return outcome

    def default_move(self, board, color):
        positions = list(board.legal_moves(color))
        if len(positions) > 0:
            return random.choice(positions)
        else:
            return PASS

    def update_tree(self, moves, outcome):
        value = self.score_func(outcome)
        self.root.update(value)
        node = self.root
        for move in moves:
            node = node.children[move]
            node.update(value)

    def repeat_outcome(self, color):
        return -self.board.size() if color==self.root.color else self.board.size()
