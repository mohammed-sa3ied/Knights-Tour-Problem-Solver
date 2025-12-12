import random
import copy
from collections import defaultdict

class BeliefSpace:
    def __init__(self, board):
        self.board = board
        self.situational = [] 
        self.normative = defaultdict(int)

    def update(self, population):
        sorted_pop = sorted(population, key=lambda x: x.fitness, reverse=True)
        best_of_gen = sorted_pop[0]
        
        # Situational (Elitism)
        if not any(ind.fitness == best_of_gen.fitness for ind in self.situational):
            self.situational.append(copy.deepcopy(best_of_gen))
            self.situational.sort(key=lambda x: x.fitness, reverse=True)
            self.situational = self.situational[:5]

        # Normative (Learn good moves)
        top_tier = sorted_pop[:max(1, len(population)//10)]
        for ind in top_tier:
            for i in range(len(ind.chromosome)-1):
                u, v = ind.chromosome[i], ind.chromosome[i+1]
                if self.board.is_valid_move(u, v):
                    self.normative[(u, v)] += 1

    def influence_mutation(self, chromosome):
        """
        Tries to fix a broken link using Normative knowledge.
        Returns: (modified_chromosome, did_change_occur)
        """
        if random.random() > 0.6: 
            return chromosome, False
        
        break_idx = -1
        for i in range(len(chromosome)-1):
            if not self.board.is_valid_move(chromosome[i], chromosome[i+1]):
                break_idx = i
                break
        
        if break_idx != -1:
            u = chromosome[break_idx]
            candidates = [m for m in self.board.valid_moves[u] if (u, m) in self.normative]
            candidates.sort(key=lambda m: self.normative[(u, m)], reverse=True)
            
            for target in candidates:
                if target in chromosome:
                    target_idx = chromosome.index(target)
                    if target_idx != break_idx and target_idx != break_idx + 1:
                        original = chromosome[:]
                        chromosome[break_idx+1], chromosome[target_idx] = chromosome[target_idx], chromosome[break_idx+1]
                        return chromosome, True

        return chromosome, False