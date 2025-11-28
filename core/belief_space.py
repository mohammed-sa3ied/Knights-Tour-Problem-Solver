class BeliefSpace:
    def __init__(self, board):
        self.board = board
        self.num_squares = board.num_squares

        self.matrix = [[0] * self.num_squares for _ in range(self.num_squares)]
        self.best_moves = [None] * self.num_squares

    def update(self, elites):
        for ind in elites:
            chromo = ind.chromosome
            for u, v in zip(chromo, chromo[1:]):
                if self.board.is_valid_move(u, v):
                    self.matrix[u][v] += 1

        for u in range(self.num_squares):
            row = self.matrix[u]
            max_val = 0
            best_v = None
            for v, count in enumerate(row):
                if count > max_val:
                    max_val = count
                    best_v = v
            self.best_moves[u] = best_v

    def suggest_next_move(self, current_sq):
        return self.best_moves[current_sq]
