"""
Genetic Algorithm (Optimized) for Knight's Tour
Uses Warnsdorff initialization for better starting population
"""

import random
import copy
import time
from core.board import Board


class IndividualOptimized:
    """Individual with Warnsdorff initialization."""
    
    def __init__(self, board, chromosome=None):
        self.board = board
        self.chromosome = chromosome if chromosome else self._generate_smart_chromosome()
        self.fitness_value = self._calculate_fitness()

    def _generate_smart_chromosome(self):
        """Generate using Warnsdorff's heuristic."""
        path = []
        visited = [False] * self.board.num_squares
        current = random.randint(0, self.board.num_squares - 1)
        path.append(current)
        visited[current] = True

        for _ in range(self.board.num_squares - 1):
            candidates = [c for c in self.board.valid_moves[current] if not visited[c]]
            if not candidates:
                break
            # Warnsdorff: pick fewest onward moves
            candidates.sort(key=lambda x: len([y for y in self.board.valid_moves[x] if not visited[y]]))
            current = candidates[0]
            path.append(current)
            visited[current] = True

        # Fill remaining randomly
        remaining = [sq for sq in range(self.board.num_squares) if not visited[sq]]
        random.shuffle(remaining)
        path.extend(remaining)
        return path

    def _calculate_fitness(self):
        """Calculate fitness."""
        valid_count = 0
        for i in range(len(self.chromosome) - 1):
            if self.board.is_valid_move(self.chromosome[i], self.chromosome[i + 1]):
                valid_count += 1
        return valid_count

    def mutate(self, mutation_prob=0.03):
        """Swap mutation."""
        for i in range(len(self.chromosome)):
            if random.random() < mutation_prob:
                j = random.randint(0, len(self.chromosome) - 1)
                self.chromosome[i], self.chromosome[j] = self.chromosome[j], self.chromosome[i]
        self.fitness_value = self._calculate_fitness()

    def get_fitness(self):
        return self.fitness_value


class PopulationOptimized:
    """Population for GA Optimized."""
    
    def __init__(self, board, size=100):
        self.board = board
        self.size = size
        self.individuals = [IndividualOptimized(self.board) for _ in range(self.size)]

    def get_best_individual(self):
        return max(self.individuals, key=lambda ind: ind.get_fitness())

    def select_parent(self, tournament_size=3):
        """Tournament selection."""
        candidates = random.sample(self.individuals, tournament_size)
        return max(candidates, key=lambda ind: ind.get_fitness())

    def evolve(self, cx_prob=0.7, mut_prob=0.2, elite_ratio=0.1):
        """Evolve to next generation."""
        new_pop = []
        num_elites = int(self.size * elite_ratio)
        sorted_inds = sorted(self.individuals, key=lambda ind: ind.get_fitness(), reverse=True)
        new_pop.extend(copy.deepcopy(sorted_inds[:num_elites]))

        while len(new_pop) < self.size:
            parent1 = self.select_parent()
            parent2 = self.select_parent()
            
            if random.random() < cx_prob:
                child1_chromo, child2_chromo = self._crossover(parent1.chromosome, parent2.chromosome)
                child1 = IndividualOptimized(self.board, child1_chromo)
                child2 = IndividualOptimized(self.board, child2_chromo)
            else:
                child1 = copy.deepcopy(parent1)
                child2 = copy.deepcopy(parent2)
            
            if random.random() < mut_prob:
                child1.mutate(mut_prob)
            if random.random() < mut_prob:
                child2.mutate(mut_prob)
            
            new_pop.extend([child1, child2])
        
        self.individuals = new_pop[:self.size]

    def _crossover(self, chromo1, chromo2):
        """Order Crossover (OX)."""
        size = len(chromo1)
        cx1 = random.randint(0, size - 1)
        cx2 = random.randint(cx1 + 1, size)
        
        child1 = [-1] * size
        child1[cx1:cx2] = chromo1[cx1:cx2]
        p2_iter = iter(chromo2[cx2:] + chromo2[:cx2])
        for i in list(range(cx2, size)) + list(range(0, cx1)):
            while True:
                val = next(p2_iter)
                if val not in child1:
                    child1[i] = val
                    break
        
        child2 = [-1] * size
        child2[cx1:cx2] = chromo2[cx1:cx2]
        p1_iter = iter(chromo1[cx2:] + chromo1[:cx2])
        for i in list(range(cx2, size)) + list(range(0, cx1)):
            while True:
                val = next(p1_iter)
                if val not in child2:
                    child2[i] = val
                    break
        
        return child1, child2


class GeneticAlgorithmOptimized:
    """Genetic Algorithm with Warnsdorff initialization."""
    
    def __init__(self, board_size=8, pop_size=100, generations=500, 
                 cx_prob=0.7, mut_prob=0.2, elite_ratio=0.1, callback=None):
        self.board = Board(board_size)
        self.population = PopulationOptimized(self.board, pop_size)
        self.generations = generations
        self.cx_prob = cx_prob
        self.mut_prob = mut_prob
        self.elite_ratio = elite_ratio
        self.callback = callback
        self.running = True

    def run(self):
        """Run the GA."""
        start_time = time.time()
        
        for gen in range(self.generations):
            if not self.running:
                return None
            
            best = self.population.get_best_individual()
            
            if self.callback:
                self.callback(gen, best, self.board.num_squares - 1)
            
            if best.get_fitness() == self.board.num_squares - 1:
                return best
            
            self.population.evolve(self.cx_prob, self.mut_prob, self.elite_ratio)
        
        return self.population.get_best_individual()

    def stop(self):
        """Stop the algorithm."""
        self.running = False
