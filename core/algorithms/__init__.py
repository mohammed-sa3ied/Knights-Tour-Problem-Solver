"""
Algorithms package for Knight's Tour Problem.

Organized by type:
- backtracking: Brute Force, Warnsdorff, Randomized Heuristic
- genetic: GA Classic, GA Optimized
- cultural: Cultural Algorithm
"""

# ----------------------------
# Backtracking algorithms
# ----------------------------
from .backtracking.brute_force import BruteForceBacktracking
from .backtracking.warnsdorff import WarnsdorffBacktracking
from .backtracking.randomized_heuristic import BacktrackingSolver as RandomizedHeuristicBacktracking

# ----------------------------
# Genetic algorithms
# ----------------------------
from .genetic.ga_classic import GeneticAlgorithm as GeneticAlgorithmClassic
from .genetic.GA_classic_opt import GeneticAlgorithm as GeneticAlgorithmOptimized
from .genetic.GA_Warnsdorff import GeneticAlgorithm as GeneticAlgorithmElitism  # optional if needed

# ----------------------------
# Cultural algorithm
# ----------------------------
from .cultural.cultural_algorithm import CulturalAlgorithm

# ----------------------------
# Expose all algorithms for easy import
# ----------------------------
__all__ = [
    # Backtracking
    'BruteForceBacktracking',
    'WarnsdorffBacktracking',
    'RandomizedHeuristicBacktracking',

    # Genetic
    'GeneticAlgorithmClassic',
    'GeneticAlgorithmOptimized',
    'GeneticAlgorithmElitism',  

    # Cultural
    'CulturalAlgorithm'
]
