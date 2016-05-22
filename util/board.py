from .const import *

def opponent(color):
    if color == BLACK:
        return WHITE
    else:
        return BLACK

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
        '''Place a stone on the board. Does not check whether the move is legal.
        '''
        self.config[row][col] = color
        oppcolor = opponent(color)

        captured = self.try_place(color, row, col)

        self.capture_block(BLACK, captured[BLACK])
        self.capture_block(WHITE, captured[WHITE])

        self.update_ko(oppcolor, row, col, captured)

        return captured

    def update_ko(self, oppcolor, row, col, captured):
        if len(captured[oppcolor]) == 1:
            self.ko_color = oppcolor
            self.ko_move = list(captured[oppcolor])[0]
        else:
            self.ko_color = None
            self.ko_move = None

    def try_place(self, color, row, col):
        '''Return the stones that will be captured if the given move is made.
        '''
        origcolor = self.config[row][col]
        self.config[row][col] = color
        oppcolor = opponent(color)

        captured = {BLACK: set(), WHITE: set()}
        for i, j in self.neighbors(row, col):
            if self.config[i][j] == oppcolor and (i,j) not in captured[oppcolor]:
                block = self.try_capture(i, j)
                captured[oppcolor].update(block)

        if len(captured[oppcolor]) == 0:
            captured[color] = self.try_capture(row, col)

        self.config[row][col] = origcolor
        return captured

    def capture(self, row, col):
        '''Remove the block at (row, col) if it has no liberty.'''
        color = self.config[row][col]
        captured_block = try_capture(row, col)
        self.capture_block(color, captured_block)

    def capture_block(self, color, block):
        '''Capture the given block.'''
        self.remove_block(block)
        self.captures[opponent(color)] += len(block)

    def try_capture(self, row, col):
        '''Return the block at (row, col) if it has no liberty.'''
        block = self.get_block(row, col)
        if self.has_liberty(block):
            return set()
        else:
            return block

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

    def get_block(self, row, col):
        color = self.config[row][col]
        if color == EMPTY:
            return set()

        block = set()
        positions = [(row, col)]
        while len(positions) > 0:
            i, j = positions.pop()
            if (i, j) not in block and self.config[i][j] == color:
                block.add((i, j))
                positions.extend(self.neighbors(i, j))

        return block

    def has_liberty(self, block):
        for i, j in block:
            for ni, nj in self.neighbors(i, j):
                if self.config[ni][nj] == EMPTY:
                    return True
        return False

    def remove_block(self, block):
        for i, j in block:
            self.config[i][j] = EMPTY
