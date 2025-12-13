from .board import Board

# Backtracking algorithms
from .algorithms.backtracking.brute_force import BruteForceBacktracking
from .algorithms.backtracking.randomized_heuristic import BacktrackingSolver as RandomizedBacktracking
from .algorithms.backtracking.warnsdorff import WarnsdorffBacktracking

# Cultural algorithm
try:
    from .algorithms.cultural.cultural_algorithm import CulturalAlgorithm
    CA_AVAILABLE = True
except ImportError:
    CA_AVAILABLE = False

# Genetic algorithms with aliases
from .algorithms.genetic.ga_classic import GeneticAlgorithm as GeneticAlgorithmClassic
from .algorithms.genetic.GA_classic_opt import GeneticAlgorithm as GeneticAlgorithmOptimized
from .algorithms.genetic.GA_Warnsdorff import GeneticAlgorithm as GeneticAlgorithmElitism

__all__ = [
    'Board',
    'BruteForceBacktracking',
    'RandomizedBacktracking', 
    'WarnsdorffBacktracking',
    'CulturalAlgorithm',
    'GeneticAlgorithmClassic',
    'GeneticAlgorithmOptimized',
    'GeneticAlgorithmElitism'
]
