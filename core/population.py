import random
import copy
from core.individual import Individual
from core.belief_space import BeliefSpace

class Population:
    def __init__(self, board, size=100):
        self.board = board
        self.size = size
        self.individuals = [Individual(self.board) for _ in range(self.size)]
        self.belief_space = BeliefSpace(board)

    def get_best_individual(self):
        return max(self.individuals, key=lambda ind: ind.get_fitness())

    def select_parent(self, tournament_size=3):
        candidates = random.sample(self.individuals, tournament_size)
        return max(candidates, key=lambda ind: ind.get_fitness())

    def evolve(self, cx_prob=0.7, mut_prob=0.2, elite_ratio=0.1):
        sorted_inds = sorted(self.individuals, key=lambda ind: ind.get_fitness(), reverse=True)

        num_learners = int(self.size * 0.2)
        self.belief_space.update(sorted_inds[:num_learners])

        new_pop = []
        num_elites = int(self.size * elite_ratio)
        new_pop.extend(copy.deepcopy(sorted_inds[:num_elites]))

        while len(new_pop) < self.size:
            parent1 = self.select_parent()
            parent2 = self.select_parent()

            if random.random() < cx_prob:
                c1, c2 = self._crossover(parent1.chromosome, parent2.chromosome)
                child1 = Individual(self.board, c1)
                child2 = Individual(self.board, c2)
            else:
                child1 = copy.deepcopy(parent1)
                child2 = copy.deepcopy(parent2)

            child1.mutate_culturally(self.belief_space, mut_prob)
            child2.mutate_culturally(self.belief_space, mut_prob)

            new_pop.extend([child1, child2])

        self.individuals = new_pop[:self.size]

    def _crossover(self, chromo1, chromo2):
        size = len(chromo1)
        cx1 = random.randint(0, size - 1)
        cx2 = random.randint(cx1 + 1, size)

        def make_child(p1, p2):
            child = [-1] * size
            child[cx1:cx2] = p1[cx1:cx2]
            p2_iter = iter(p2[cx2:] + p2[:cx2])
            for i in list(range(cx2, size)) + list(range(0, cx1)):
                while True:
                    val = next(p2_iter)
                    if val not in child:
                        child[i] = val
                        break
            return child

        return make_child(chromo1, chromo2), make_child(chromo2, chromo1)
