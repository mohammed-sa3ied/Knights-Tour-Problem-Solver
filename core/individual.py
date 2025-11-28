import random

class Individual:
    def __init__(self, board, chromosome=None):
        self.board = board
        if chromosome is None:
            self.chromosome = random.sample(range(board.num_squares), board.num_squares)
        else:
            self.chromosome = chromosome[:]
        self.fitness_value = self._calculate_fitness_value()

    def _calculate_fitness_value(self):
        valid_count = 0
        chromo = self.chromosome
        for i in range(len(chromo) - 1):
            if self.board.is_valid_move(chromo[i], chromo[i + 1]):
                valid_count += 1
        return valid_count

    def mutate_culturally(self, belief_space, mutation_prob=0.05):
        if random.random() > mutation_prob:
            return

        chromo = self.chromosome
        break_point = -1
        
        for i in range(len(chromo) - 1):
            if not self.board.is_valid_move(chromo[i], chromo[i+1]):
                break_point = i
                break
        
        if break_point != -1:
            current = chromo[break_point]
            suggestion = belief_space.suggest_next_move(current)

            if suggestion is not None and suggestion != chromo[break_point+1]:
                try:
                    swap_idx = chromo.index(suggestion)
                    target_idx = break_point + 1
                    chromo[target_idx], chromo[swap_idx] = chromo[swap_idx], chromo[target_idx]
                except ValueError:
                    pass 
            else:
                j = random.randint(0, len(chromo) - 1)
                target = break_point + 1
                chromo[target], chromo[j] = chromo[j], chromo[target]
        else:
            i = random.randint(0, len(chromo) - 1)
            j = random.randint(0, len(chromo) - 1)
            chromo[i], chromo[j] = chromo[j], chromo[i]

        self.fitness_value = self._calculate_fitness_value()

    def get_fitness(self):
        return self.fitness_value
