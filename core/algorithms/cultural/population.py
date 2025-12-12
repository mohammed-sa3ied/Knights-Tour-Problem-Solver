from .individual import Individual

class Population:
    """Population management for the Cultural Algorithm"""
    
    def __init__(self, board, start_pos, size=100):
        self.board = board
        self.start_pos = start_pos
        self.size = size
        self.individuals = [Individual(board, start_pos) for _ in range(size)]
    
    def sort_by_fitness(self):
        """Sort population by fitness in descending order"""
        self.individuals.sort(key=lambda x: x.fitness, reverse=True)
    
    def get_best(self):
        """Return the best individual"""
        return max(self.individuals, key=lambda x: x.fitness)
    
    def get_average_fitness(self):
        """Calculate average fitness of population"""
        return sum(ind.fitness for ind in self.individuals) / len(self.individuals)