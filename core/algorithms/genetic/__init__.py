"""
Genetic Algorithms for Knight's Tour.
"""

from .ga_classic import GeneticAlgorithmClassic
from .ga_optimized import GeneticAlgorithmOptimized

__all__ = [
    'GeneticAlgorithmClassic',
    'GeneticAlgorithmOptimized'
]