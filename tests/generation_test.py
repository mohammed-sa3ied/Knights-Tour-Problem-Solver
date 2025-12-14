import random
import copy
import time
import pandas as pd
import sys
import os

# ==========================================
# PART 1: DEPENDENCIES (Board, Individual, BeliefSpace)
# ==========================================

class Board:
    def __init__(self, size):
        self.size = size
        self.num_squares = size * size
        self.moves = [
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1)
        ]

    def is_valid_move(self, start, end):
        """Check if a knight can move from start index to end index."""
        r1, c1 = divmod(start, self.size)
        r2, c2 = divmod(end, self.size)
        return (abs(r1 - r2), abs(c1 - c2)) in [(1, 2), (2, 1)]

    def get_legal_moves(self, idx):
        """Return list of valid target indices from a square."""
        r, c = divmod(idx, self.size)
        valid = []
        for dr, dc in self.moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                valid.append(nr * self.size + nc)
        return valid

def order_crossover(p1, p2):
    """Order Crossover (OX1) for permutations."""
    size = len(p1)
    cxpoint1 = random.randint(1, size - 1)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 < cxpoint1:
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1

    child = [None] * size
    child[cxpoint1:cxpoint2] = p1[cxpoint1:cxpoint2]
    
    current_p2_idx = 0
    for i in range(size):
        if child[i] is None:
            while p2[current_p2_idx] in child:
                current_p2_idx += 1
            child[i] = p2[current_p2_idx]
            
    if p1[0] == p2[0]: 
        start_node = p1[0]
        if child[0] != start_node:
            idx = child.index(start_node)
            child[0], child[idx] = child[idx], child[0]

    return child

class Individual:
    def __init__(self, board, start_pos=None, chromosome=None):
        self.board = board
        if chromosome:
            self.chromosome = chromosome
            self.start_pos = chromosome[0]
        else:
            self.start_pos = start_pos
            genes = [i for i in range(board.num_squares) if i != start_pos]
            random.shuffle(genes)
            self.chromosome = [start_pos] + genes
            
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        """Fitness = Length of the valid path starting from index 0."""
        fitness = 0
        for i in range(len(self.chromosome) - 1):
            if self.board.is_valid_move(self.chromosome[i], self.chromosome[i+1]):
                fitness += 1
            else:
                break
        return fitness

    def mutate(self):
        """Swap Mutation."""
        new_chromo = self.chromosome[:]
        if len(new_chromo) > 2:
            idx1, idx2 = random.sample(range(1, len(new_chromo)), 2)
            new_chromo[idx1], new_chromo[idx2] = new_chromo[idx2], new_chromo[idx1]
        return Individual(self.board, chromosome=new_chromo)

class BeliefSpace:
    """Stores 'Situation Knowledge' to influence mutation."""
    def __init__(self, board):
        self.board = board
        self.best_individual = None

    def update(self, population):
        if not population:
            return
        current_best = population[0]
        if self.best_individual is None or current_best.fitness > self.best_individual.fitness:
            self.best_individual = copy.deepcopy(current_best)

    def influence_mutation(self, chromosome):
        changed = False
        break_index = 0
        for i in range(len(chromosome) - 1):
            if self.board.is_valid_move(chromosome[i], chromosome[i+1]):
                break_index += 1
            else:
                break
        
        if break_index < len(chromosome) - 1:
            current_sq = chromosome[break_index]
            legal_moves = self.board.get_legal_moves(current_sq)
            
            swap_candidate_idx = -1
            for idx in range(break_index + 1, len(chromosome)):
                if chromosome[idx] in legal_moves:
                    swap_candidate_idx = idx
                    break
            
            if swap_candidate_idx != -1:
                chromosome[break_index+1], chromosome[swap_candidate_idx] = \
                    chromosome[swap_candidate_idx], chromosome[break_index+1]
                changed = True

        return chromosome, changed


# ==========================================
# PART 2: CULTURAL ALGORITHM
# ==========================================

class CulturalAlgorithm:
    def __init__(self, board_size, start_pos, pop_size=100, max_gen=1000, callback=None):
        self.board = Board(board_size)
        self.pop_size = pop_size
        self.max_gen = max_gen
        self.start_pos = start_pos
        self.callback = callback
        self.running = True
        self.belief_space = BeliefSpace(self.board)

        print(f"\n--- 1. INITIALIZATION ---")
        print(f"Creating {pop_size} individuals...")
        self.population = [Individual(self.board, start_pos) for _ in range(pop_size)]

    def stop(self):
        self.running = False

    def run(self):
        start_time = time.time()
        max_fitness = self.board.num_squares - 1
        stagnation_counter = 0
        previous_best_fitness = 0
        STAGNATION_LIMIT = 2000
        history_data = []

        self.population.sort(key=lambda x: x.fitness, reverse=True)

        # Record Gen 0
        current_best = self.population[0]
        avg_fit = sum(ind.fitness for ind in self.population) / self.pop_size
        history_data.append({'Generation': 0, 'Best_Fitness': current_best.fitness, 'Average_Fitness': avg_fit})

        if self.population[0].fitness == max_fitness:
            print(f"\nSOLUTION FOUND IN GENERATION 0!")
            pd.DataFrame(history_data).to_csv('convergence_log.csv', index=False)
            return self.population[0]

        print("\n--- 2. STARTING EVOLUTION ---")

        for gen in range(1, self.max_gen + 1):
            if not self.running:
                pd.DataFrame(history_data).to_csv('convergence_log.csv', index=False)
                return self.population[0]

            avg_fitness = sum(ind.fitness for ind in self.population) / self.pop_size
            self.belief_space.update(self.population)
            
            # Elitism
            new_pop = []
            elite_count = int(self.pop_size * 0.10)
            new_pop.extend(copy.deepcopy(self.population[:elite_count]))

            while len(new_pop) < self.pop_size:
                parents = random.sample(self.population[:50], 2)
                parents.sort(key=lambda x: x.fitness, reverse=True)
                p1, p2 = parents[0], parents[1] if random.random() < 0.5 else random.choice(self.population[:50])

                child_chromo = order_crossover(p1.chromosome, p2.chromosome)
                child_chromo, _ = self.belief_space.influence_mutation(child_chromo)
                child = Individual(self.board, chromosome=child_chromo)
                new_pop.append(child.mutate())

            self.population = new_pop
            self.population.sort(key=lambda x: x.fitness, reverse=True)
            best_ind = self.population[0]

            if gen % 10 == 0 or best_ind.fitness == max_fitness:
                print(f"   --> Gen {gen} | Best: {best_ind.fitness}/{max_fitness} | Avg: {avg_fitness:.2f}")

            history_data.append({'Generation': gen, 'Best_Fitness': best_ind.fitness, 'Average_Fitness': avg_fitness})

            if self.callback:
                self.callback(gen, best_ind, max_fitness)

            # Stagnation Check
            if best_ind.fitness == previous_best_fitness:
                stagnation_counter += 1
            else:
                stagnation_counter = 0
                previous_best_fitness = best_ind.fitness

            if best_ind.fitness == max_fitness:
                print(f"\n\n--- RESULT FOUND ---")
                print(f"Solution found in Generation {gen}!")
                pd.DataFrame(history_data).to_csv('convergence_log.csv', index=False)
                print("Convergence log saved to 'convergence_log.csv'")
                return best_ind

            if stagnation_counter >= STAGNATION_LIMIT:
                print(f"\n--- STAGNATION LIMIT REACHED ---")
                pd.DataFrame(history_data).to_csv('convergence_log.csv', index=False)
                print("Convergence log saved to 'convergence_log.csv'")
                return best_ind

        print("\nMax generations reached.")
        pd.DataFrame(history_data).to_csv('convergence_log.csv', index=False)
        return self.population[0]


# ==========================================
# PART 3: MAIN EXECUTION & SAVING
# ==========================================
if __name__ == "__main__":
    print("=== KNIGHT'S TOUR: EVOLUTIONARY SOLVER ===")

    # Input Size
    while True:
        try:
            sz = int(input("Enter Board Size (5-10): "))
            if 5 <= sz <= 10: break
        except: pass

    # Input Start Position
    while True:
        try:
            print(f"Enter Start Position (Row Col) from 1 to {sz}: ")
            inp = input("> ").split()
            r, c = int(inp[0]), int(inp[1])
            if 1 <= r <= sz and 1 <= c <= sz:
                start_node = (r-1) * sz + (c-1)
                break
        except: print("Invalid input.")

    # Run Algorithm
    ca = CulturalAlgorithm(board_size=sz, start_pos=start_node, pop_size=150, max_gen=2000)
    tour_ind = ca.run()
    tour = tour_ind.chromosome

    # Show Result
    print("\n--- FINAL CHROMOSOME (PATH) ---")
    valid = 0
    board = Board(sz)

    grid = [[0]*sz for _ in range(sz)]
    
    # Logic to build the grid visualization
    for idx, sq in enumerate(tour):
        r, c = divmod(sq, sz)
        grid[r][c] = idx + 1
        if idx < len(tour)-1:
            if board.is_valid_move(sq, tour[idx+1]):
                valid += 1

    # Print Grid
    for row in grid:
        print("\t".join(f"{x:2}" for x in row))

    print(f"\nFinal Validity: {valid}/{sz*sz - 1}")
    if valid == sz*sz - 1:
        print("Result: SUCCESS ✅")
    else:
        print("Result: FAILED ❌")

    # ==========================================
    # SAVING OUTPUT TO CSV
    # ==========================================
    print("\n--- SAVING OUTPUT ---")
    
    # 1. Save the Grid Layout
    # This creates a CSV that looks exactly like the board (rows and cols)
    df_grid = pd.DataFrame(grid)
    df_grid.to_csv('final_board.csv', index=False, header=False)
    print(f"1. Board Grid saved to: 'final_board.csv'")

    # 2. Save the Move Sequence
    # This creates a list: Step 1 -> Row 2, Col 3, etc.
    moves_data = []
    for step, sq in enumerate(tour):
        r, c = divmod(sq, sz)
        # Using 1-based indexing for Row/Col to match user input style
        moves_data.append({
            "Step": step + 1,
            "Row": r + 1,
            "Column": c + 1
        })
    
    df_moves = pd.DataFrame(moves_data)
    df_moves.to_csv('move_sequence.csv', index=False)
    print(f"2. Move Sequence saved to: 'move_sequence.csv'")