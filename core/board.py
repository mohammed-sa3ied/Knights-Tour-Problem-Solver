class Board:
    def __init__(self, size):
        self.size = size
        self.num_squares = size * size
        self.valid_moves = self._precompute_valid_moves()

    def _precompute_valid_moves(self):
        deltas = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        moves = {}
        for sq in range(self.num_squares):
            r, c = divmod(sq, self.size)
            neighbors = []
            for dr, dc in deltas:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    neighbors.append(nr * self.size + nc)
            moves[sq] = neighbors
        return moves

    def is_valid_move(self, a, b):
        return b in self.valid_moves[a]