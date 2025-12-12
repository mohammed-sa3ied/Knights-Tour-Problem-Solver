import random

class Individual:
    def __init__(self, board, start_pos=None, chromosome=None):
        self.board = board
        self.size = board.num_squares
        
        if chromosome:
            self.chromosome = chromosome
        else:
            self.chromosome = self._randomized_warnsdorff(start_pos)
            
        self.fitness = self._calc_fitness()

    def _randomized_warnsdorff(self, start_pos):
        path = [start_pos]
        visited = {start_pos}
        current = start_pos

        while len(path) < self.size:
            moves = [m for m in self.board.valid_moves[current] if m not in visited]
            if not moves: 
                break
            
            # Warnsdorff with Random Tie-Breaking
            scored_moves = []
            for m in moves:
                onward = sum(1 for n in self.board.valid_moves[m] if n not in visited)
                scored_moves.append((onward, m))
            scored_moves.sort(key=lambda x: x[0])
            best_score = scored_moves[0][0]
            best_candidates = [m for score, m in scored_moves if score == best_score]
            next_move = random.choice(best_candidates)
            
            path.append(next_move)
            visited.add(next_move)
            current = next_move

        if len(path) < self.size:
            remaining = list(set(range(self.size)) - visited)
            random.shuffle(remaining)
            path.extend(remaining)
            
        return path

    def _calc_fitness(self):
        return sum(1 for i in range(self.size - 1) 
                   if self.board.is_valid_move(self.chromosome[i], self.chromosome[i+1]))

    def mutate(self):
        original = self.chromosome[:]
        
        # 2-opt Inversion Mutation
        break_point = -1
        for i in range(self.size - 1):
            if not self.board.is_valid_move(self.chromosome[i], self.chromosome[i+1]):
                break_point = i
                break
        
        if break_point != -1 and random.random() < 0.5:
            u = self.chromosome[break_point]
            valid_neighbors = self.board.valid_moves[u]
            candidates = [idx for idx, val in enumerate(self.chromosome) 
                          if val in valid_neighbors and idx > break_point + 1]
            
            if candidates:
                cut = random.choice(candidates)
                segment = self.chromosome[break_point+1 : cut+1]
                self.chromosome[break_point+1 : cut+1] = segment[::-1]
        else:
            i, j = sorted(random.sample(range(self.size), 2))
            self.chromosome[i:j+1] = self.chromosome[i:j+1][::-1]

        self.fitness = self._calc_fitness()
        return self.chromosome != original