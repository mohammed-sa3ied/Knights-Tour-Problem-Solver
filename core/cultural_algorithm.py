import time
import random
from core.board import Board
from core.population import Population

class CulturalAlgorithm:
    def __init__(self, board_size=8, pop_size=100, generations=500, cx_prob=0.7, mut_prob=0.2, elite_ratio=0.1):
        self.board = Board(board_size)
        self.population = Population(self.board, pop_size)
        self.generations = generations
        self.cx_prob = cx_prob
        self.mut_prob = mut_prob
        self.elite_ratio = elite_ratio

    def run(self):
        start_time = time.time()
        for gen in range(self.generations):
            best = self.population.get_best_individual()
            print(f"Generation {gen}: Best fitness = {best.get_fitness()}/{self.board.num_squares-1}")

            if best.get_fitness() == self.board.num_squares - 1:
                print(f"Full tour found in Generation {gen}!")
                print(f"Tour: {best.chromosome}")
                return best

            self.population.evolve(self.cx_prob, self.mut_prob, self.elite_ratio)

        end_time = time.time()
        print(f"Cultural Algorithm completed in {end_time - start_time:.2f}s")
        return self.population.get_best_individual()
