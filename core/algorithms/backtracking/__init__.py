"""
Backtracking algorithms for Knight's Tour.
"""


from .brute_force import BruteForceBacktracking
from .warnsdorff import WarnsdorffBacktracking
from .randomized_heuristic import BacktrackingSolver  # تم تعديل الاسم ليتوافق مع الملف

__all__ = [
    'BruteForceBacktracking',
    'WarnsdorffBacktracking',
    'BacktrackingSolver'  # نفس الاسم الجديد
]
