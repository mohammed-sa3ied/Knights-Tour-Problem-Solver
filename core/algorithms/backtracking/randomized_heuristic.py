# -*- coding: utf-8 -*-
"""
Backtracking algorithm with Randomized Heuristic for Knight's Tour.
Uses Warnsdorff's heuristic with randomization for equal-degree moves.
"""

import random


class BacktrackingSolver:
    """
    Backtracking algorithm with Randomized Warnsdorff's heuristic.
    
    The algorithm:
    1. Tries moves in order of accessibility (fewest onward moves first)
    2. Randomizes the order when multiple moves have the same accessibility
    3. This adds variability while maintaining the heuristic's power
    """
    
    # Knight's possible moves (L-shaped)
    MOVES = [
        (+2, +1), (+1, +2), (-1, +2), (-2, +1),
        (-2, -1), (-1, -2), (+1, -2), (+2, -1)
    ]
    
    def __init__(self, board):
        """
        Initialize the solver.
        
        Args:
            board: Board object with valid_moves dictionary
        """
        self.board = board
        self.solution = []
        self.callback = None
        self.running = True
        
        # Track visited squares
        self.visited = None
        
    def solve(self, start_square, callback=None):
        """
        Solve Knight's Tour starting from start_square.
        
        Args:
            start_square: Starting position (square index)
            callback: Optional callback function(path, step) for visualization
        
        Returns:
            list: Solution path (list of square indices) or None if no solution
        """
        self.callback = callback
        self.solution = [start_square]
        self.running = True
        
        # Initialize visited array
        self.visited = [False] * self.board.num_squares
        self.visited[start_square] = True
        
        # Start backtracking
        if self._backtrack_randomized(start_square, 1):
            return self.solution
        return None
    
    def _backtrack_randomized(self, current_sq, move_count):
        """
        Recursive backtracking with randomized Warnsdorff's heuristic.
        
        Args:
            current_sq: Current square index
            move_count: Number of moves made so far
        
        Returns:
            bool: True if solution found, False otherwise
        """
        if not self.running:
            return False
            
        # Base case: all squares visited
        if move_count == self.board.num_squares:
            return True
        
        # Callback for visualization
        if self.callback:
            self.callback(self.solution[:], move_count)
        
        # Get valid unvisited moves
        candidates = [sq for sq in self.board.valid_moves[current_sq] 
                     if not self.visited[sq]]
        
        if not candidates:
            return False
        
        # Apply randomized Warnsdorff's heuristic
        candidates = self._sort_moves_randomized(candidates)
        
        # Try each candidate
        for next_sq in candidates:
            self.visited[next_sq] = True
            self.solution.append(next_sq)
            
            if self._backtrack_randomized(next_sq, move_count + 1):
                return True
            
            # Backtrack
            self.visited[next_sq] = False
            self.solution.pop()
            
            # Callback for backtrack visualization
            if self.callback:
                self.callback(self.solution[:], move_count)
        
        return False
    
    def _sort_moves_randomized(self, candidates):
        """
        Sort moves by accessibility (Warnsdorff), randomizing ties.
        
        This is the key difference from pure Warnsdorff:
        - Moves are still sorted by degree (fewest onward moves first)
        - BUT moves with the same degree are shuffled randomly
        - This adds variability and can help escape local optima
        
        Args:
            candidates: List of candidate square indices
        
        Returns:
            list: Sorted and randomized list of candidates
        """
        # Calculate degree for each candidate
        degree_list = [(self._count_onward_moves(sq), sq) for sq in candidates]
        
        # Group by degree
        degree_groups = {}
        for degree, square in degree_list:
            if degree not in degree_groups:
                degree_groups[degree] = []
            degree_groups[degree].append(square)
        
        # Build sorted list with randomized ties
        sorted_candidates = []
        for degree in sorted(degree_groups.keys()):
            group = degree_groups[degree]
            random.shuffle(group)  # RANDOMIZE within equal-degree moves
            sorted_candidates.extend(group)
        
        return sorted_candidates
    
    def _count_onward_moves(self, square):
        """
        Count unvisited squares reachable from this square.
        Used for Warnsdorff's heuristic (accessibility).
        
        Args:
            square: Square index to check
        
        Returns:
            int: Number of unvisited accessible squares
        """
        return sum(1 for sq in self.board.valid_moves[square] 
                   if not self.visited[sq])
    
    def stop(self):
        """Stop the backtracking search."""
        self.running = False


class BacktrackingSolverClassic:
    """
    Classic Backtracking (pure Warnsdorff without randomization).
    Kept for comparison purposes.
    """
    
    def __init__(self, board):
        self.board = board
        self.solution = []
        self.callback = None
        self.running = True
        
    def solve(self, start_square, callback=None):
        self.callback = callback
        self.solution = [start_square]
        self.running = True
        visited = [False] * self.board.num_squares
        visited[start_square] = True
        
        if self._backtrack(start_square, visited, 1):
            return self.solution
        return None
    
    def _backtrack(self, current_sq, visited, move_count):
        if not self.running:
            return False
            
        if move_count == self.board.num_squares:
            return True
        
        if self.callback:
            self.callback(self.solution[:], move_count)
        
        candidates = [sq for sq in self.board.valid_moves[current_sq] 
                     if not visited[sq]]
        
        if not candidates:
            return False
        
        # Pure Warnsdorff (no randomization)
        candidates.sort(key=lambda sq: sum(1 for s in self.board.valid_moves[sq] 
                                          if not visited[s]))
        
        for next_sq in candidates:
            visited[next_sq] = True
            self.solution.append(next_sq)
            
            if self._backtrack(next_sq, visited, move_count + 1):
                return True
            
            visited[next_sq] = False
            self.solution.pop()
            
            if self.callback:
                self.callback(self.solution[:], move_count)
        
        return False
    
    def stop(self):
        self.running = False