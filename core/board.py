import random

class Board:
    def __init__(self, size=8):
        self.size = size
        self.num_squares = size * size 
        self.valid_moves = self._precompute_valid_moves()  

    def _precompute_valid_moves(self):
        deltas = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                  (-2, -1), (-1, -2), (1, -2), (2, -1)]
        moves = {}
        for square in range(self.num_squares):
            row, col = divmod(square, self.size)
            neighbors = []
            for dr, dc in deltas:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < self.size and 0 <= new_col < self.size:
                    target = new_row * self.size + new_col
                    neighbors.append(target)
            moves[square] = neighbors
        return moves

    def is_valid_move(self, from_sq, to_sq):
        return to_sq in self.valid_moves[from_sq]
