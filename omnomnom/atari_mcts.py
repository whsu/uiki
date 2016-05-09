from uiki.mcts import *

class AtariMCTS(MCTS):
    def __init__(self, board, visited, color, num_sims, score_func, exp_const,
                       num_caps):
        super(AtariMCTS, self).__init__(
                  board, visited, color, num_sims, score_func, exp_const)
        self.num_caps = num_caps

    def place_move(self, board, color, move, visited):
        oppcolor = opponent(color)
        board.place(color, move[0], move[1])
        state = board.get_state()
        if state in visited:
            outcome = self.repeat_outcome(color)
        elif board.captures[color] >= self.num_caps:
            outcome = self.win_outcome(color)
        elif board.captures[oppcolor] >= self.num_caps:
            outcome = self.win_outcome(oppcolor)
        else:
            visited.add(state)
            outcome = None
        return outcome

    def win_outcome(self, color):
        return self.board.size() if color==self.color else -self.board.size()
