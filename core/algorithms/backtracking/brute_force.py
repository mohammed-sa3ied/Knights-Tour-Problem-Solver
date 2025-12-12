# -*- coding: utf-8 -*-
"""
Brute Force Backtracking for Knight's Tour
Pure backtracking without any heuristics
WARNING: Very slow, use only for small boards (5×5 or smaller)
"""

from core.board import Board


class BruteForceBacktracking:
    """
    Pure brute force backtracking.
    Tries all possible moves without optimization.
    """
    
    MOVES = [
        (+2, +1), (+1, +2), (-1, +2), (-2, +1),
        (-2, -1), (-1, -2), (+1, -2), (+2, -1)
    ]
    
    def __init__(self, board):
        self.board = board
        self.size = board.size
        self.total_squares = board.num_squares
        self.solution = []
        self.callback = None
        self.running = True
        
        self.grid_visited = None
        
    def solve(self, start_square, callback=None):
        """
        Solve using brute force.
        
        Args:
            start_square: Starting square index
            callback: Optional callback(path, step)
        
        Returns:
            list: Solution path or None
        """
        self.callback = callback
        self.running = True
        
        # Convert to (row, col)
        start_x = start_square // self.size
        start_y = start_square % self.size
        
        # Initialize
        self.grid_visited = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        self.grid_visited[start_x][start_y] = 0
        self.solution = [(start_x, start_y)]
        
        if self._backtrack(start_x, start_y, 1):
            return [r * self.size + c for r, c in self.solution]
        return None
    
    def _is_valid(self, x, y):
        """Check if (x, y) is valid and unvisited."""
        return (0 <= x < self.size and 
                0 <= y < self.size and 
                self.grid_visited[x][y] == -1)
    
    def _backtrack(self, x, y, step):
        """Recursive backtracking."""
        if not self.running:
            return False
        
        # Success
        if step == self.total_squares:
            return True
        
        # Callback
        if self.callback:
            path_indices = [r * self.size + c for r, c in self.solution]
            self.callback(path_indices, step)
        
        # Try all 8 moves (NO HEURISTIC)
        for dx, dy in self.MOVES:
            nx, ny = x + dx, y + dy
            
            if self._is_valid(nx, ny):
                self.grid_visited[nx][ny] = step
                self.solution.append((nx, ny))
                
                if self._backtrack(nx, ny, step + 1):
                    return True
                
                # Backtrack
                self.grid_visited[nx][ny] = -1
                self.solution.pop()
                
                if self.callback:
                    path_indices = [r * self.size + c for r, c in self.solution]
                    self.callback(path_indices, step)
        
        return False
    
    def stop(self):
        """Stop the search."""
        self.running = False
