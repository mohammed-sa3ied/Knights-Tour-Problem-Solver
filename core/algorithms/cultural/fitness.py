import random

def order_crossover(parent1, parent2):
    """
    Order Crossover (OX1) for Knight's Tour problem.
    Preserves order and flow from both parents.
    """
    size = len(parent1)
    p1 = parent1[:]
    p2 = parent2[:]
    start, end = sorted(random.sample(range(size), 2))
    
    child = [-1] * size
    child[start:end] = p1[start:end]
    
    current_p2_idx = 0
    for i in range(size):
        if child[i] == -1:
            while p2[current_p2_idx] in child:
                current_p2_idx += 1
            child[i] = p2[current_p2_idx]
    
    return child