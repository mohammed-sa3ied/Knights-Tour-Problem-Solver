# Import classes with aliases to match naming convention
from .ga_classic import GeneticAlgorithm as GeneticAlgorithmClassic
from .GA_classic_opt import GeneticAlgorithm as GeneticAlgorithmOptimized
from .GA_Warnsdorff import GeneticAlgorithm as GeneticAlgorithmElitism

__all__ = [
    'GeneticAlgorithmClassic',
    'GeneticAlgorithmOptimized',
    'GeneticAlgorithmElitism'
]
