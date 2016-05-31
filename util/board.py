from .const import *

def opponent(color):
    if color == BLACK:
        return WHITE
    else:
        return BLACK

class Block:
    def __init__(self):
        self.members = set()
        self.free_neighbors = set()

    def is_in_atari(self):
        return len(self.free_neighbors) == 1

    def is_captured(self):
        return len(self.free_neighbors) == 0

    def add(self, pos, free_neighbors):
        self.members.add(pos)
        self.free_neighbors.remove(pos)
        self.free_neighbors.update(free_neighbors)

class Board:
    def __init__(self, rows, cols, komi=0.0):
        self.rows = rows
        self.cols = cols
        self.set_komi(komi)
        self.reset()

    def __str__(self):
        return '{0}\nBlack: {1}\nWhite: {2}\n'.format(
                    '\n'.join(map(lambda x:''.join(x), reversed(self.config))),
                    self.captures[BLACK], self.captures[WHITE])

    def __getitem__(self, position):
        row, col = position
        return self.config[row][col]

    def reset(self):
        '''Reset the board.'''
        self.config = [None] * self.rows
        for i in range(self.rows):
            self.config[i] = [EMPTY] * self.cols
        self.captures = {BLACK: 0, WHITE: 0}
        self.ko_move = None
        self.ko_color = None

        self.blocks = {}

    def set_komi(self, komi):
        '''Set the komi.'''
        self.komi = komi

    def size(self):
        '''Number of intersections on the board.'''
        return self.rows * self.cols

    def get_state(self):
        '''Return a hashable representation of board configuration.'''
        return ''.join(map(lambda x:''.join(x), self.config))

    def score(self, color):
        '''Return score for given color.'''
        black_score = self.captures[BLACK] - self.captures[WHITE] - self.komi
        if color == BLACK:
            return black_score
        else:
            return -black_score

    def empty_positions(self):
        '''Iterator over empty positions.'''
        for row in range(self.rows):
            for col in range(self.cols):
                if self.config[row][col] == EMPTY:
                    yield row, col

    def legal_moves(self, color, suicide_allowed=False):
        '''Iterator over legal moves for given color.

        Scenarios covered:
        - Simple ko : not legal
        - Superko : legal
        - One-stone suicide : not legal
        - Multi-stone suicide : legal if suicide_allowed=True
        '''
        oppcolor = opponent(color)
        for pos in self.empty_positions():
            if pos == self.ko_move and color == self.ko_color:
                continue
            if EMPTY not in self.neighbors(pos[0], pos[1]):
                captured = self.try_place(color, pos[0], pos[1])
                numcapped = len(captured[color])
                if numcapped == 1 or (numcapped > 1 and not suicide_allowed):
                    continue
            yield pos

    def place(self, color, row, col):
        '''Place a stone on the board if the given position is empty.'''
        if self.config[row][col] != EMPTY:
            return

        pos = (row, col)
        oppcolor = opponent(color)

        self.add_stone(color, row, col)

        captured = []
        for npos in self.neighbors(row, col):
            if npos in self.blocks and self.blocks[npos].is_captured():
                captured.append(self.blocks[npos].members)
                self.remove_block(self.blocks[npos])

        self.update_ko(oppcolor, pos, captured)

        if len(captured) > 0:
            self.captures[color] += len(captured)
        elif self.blocks[pos].is_captured():
            self.captures[oppcolor] += len(self.blocks[pos].members)
            self.remove_block(self.blocks[pos])

    def update_ko(self, oppcolor, pos, captured):
        if len(self.blocks[pos].members) == 1 and \
           len(self.blocks[pos].free_neighbors) == 0 and \
           len(captured) == 1:
            self.ko_color = oppcolor
            self.ko_move = captured[0]
        else:
            self.ko_color = None
            self.ko_move = None

    def out_of_bounds(self, row, col):
        return row < 0 or row >= self.rows or col < 0 or col >= self.cols

    def neighbors(self, row, col):
        if row > 0:
            yield (row-1, col)
        if col > 0:
            yield (row, col-1)
        if row < self.rows-1:
            yield (row+1, col)
        if col < self.cols-1:
            yield (row, col+1)

    def free_neighbors(self, row, col):
        for i, j in self.neighbors(row, col):
            if self.config[i][j] == EMPTY:
                yield (i, j)

    def remove_stone(self, row, col):
        pos = (row, col)
        self.config[row][col] = EMPTY
        self.blocks.remove(pos)
        for npos in self.neighbors(row, col):
            if npos in self.blocks:
                self.blocks[npos].free_neighbors.add(pos)

    def remove_block(self, pos):
        if pos in self.blocks:
            for i, j in self.blocks[pos]:
                self.remove_stone(i, j)

    def add_stone(self, color, row, col):
        self.config[row][col] = color
        pos = (row, col)
        oppcolor = opponent(color)
        for npos in self.neighbors(row, col):
            if self[npos] == color:
                if pos not in self.blocks:
                    self.blocks[npos].add(pos, self.free_neighbors(row, col))
                elif self.blocks[npos] != self.blocks[pos]:
                    self.join_blocks(npos, pos)
            elif self[npos] == oppcolor:
                self.blocks[npos].free_neighbors.remove(pos)

        if pos not in self.blocks:
            self.blocks[pos] = Block()
            self.blocks[pos].members.add(pos)
            self.blocks[pos].free_neighbors.update(self.free_neighbors(pos[0], pos[1]))


    def join_blocks(self, p1, p2):
        b1 = self.blocks[p1]
        b2 = self.blocks[p2]
        b1.members.update(b2.members)
        b1.free_neighbors.update(b2.free_neighbors).difference_update(b1.members)
        self.blocks[p2] = b1
