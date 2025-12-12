import random
import copy
import time
from core.board import Board
from .belief_space import BeliefSpace
from .individual import Individual
from .fitness import order_crossover

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
        
        print("\n[Sample of Initial Population (First 10)]")
        for i in range(min(10, pop_size)):
            ind = self.population[i]
            print(f"ID {i}: Fitness {ind.fitness} | Path: {ind.chromosome}")

    def stop(self):
        """Stop the algorithm execution."""
        self.running = False

    def run(self):
        start_time = time.time()
        max_fitness = self.board.num_squares - 1
        
        # Stagnation variables
        stagnation_counter = 0
        previous_best_fitness = 0
        STAGNATION_LIMIT = 500

        # Check Gen 0 immediately
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        if self.population[0].fitness == max_fitness:
            print(f"\nSOLUTION FOUND IN GENERATION 0 (Initialization)!")
            print(f"Time: {time.time() - start_time:.4f}s")
            return self.population[0]

        print("\n--- 2. STARTING EVOLUTION ---")
        
        for gen in range(1, self.max_gen + 1):
            # Check if algorithm was stopped
            if not self.running:
                print("\nAlgorithm stopped by user")
                return self.population[0]
            
            # Calculate Average Fitness
            total_fitness = sum(ind.fitness for ind in self.population)
            avg_fitness = total_fitness / self.pop_size
            
            # Evolution Logic
            self.belief_space.update(self.population)
            new_pop = []
            
            # Elitism
            elite_count = int(self.pop_size * 0.10)
            new_pop.extend(copy.deepcopy(self.population[:elite_count]))
            
            shown_demo = False
            print(f"\n>> GENERATION {gen} Processing...")

            while len(new_pop) < self.pop_size:
                parents = random.sample(self.population[:50], 2)
                parents.sort(key=lambda x: x.fitness, reverse=True)
                p1 = parents[0]
                p2 = parents[1] if random.random() < 0.5 else random.choice(self.population[:50])
                
                # Crossover
                child_chromo = order_crossover(p1.chromosome, p2.chromosome)

                if not shown_demo:
                    print(f"   [PARENTS SELECTED]")
                    print(f"   Parent 1 (Fit {p1.fitness}): {p1.chromosome}")
                    print(f"   Parent 2 (Fit {p2.fitness}): {p2.chromosome}")

                # Belief Space influence
                child_chromo, changed = self.belief_space.influence_mutation(child_chromo)
                child = Individual(self.board, chromosome=child_chromo)
                
                if not shown_demo:
                    print(f"   [CHILD AFTER CROSSOVER]: {child.chromosome}")

                # Mutation
                mutated = child.mutate()
                
                if not shown_demo:
                    print(f"   [CHILD AFTER MUTATION ]: {child.chromosome}")
                    shown_demo = True
                    
                new_pop.append(child)
            
            self.population = new_pop
            self.population.sort(key=lambda x: x.fitness, reverse=True)
            best_ind = self.population[0]
            
            print(f"   --> Gen {gen} Stats | Best: {best_ind.fitness}/{max_fitness} | Avg: {avg_fitness:.2f}")

            # Call callback for GUI updates
            if self.callback:
                self.callback(gen, best_ind, max_fitness)

            # Check Stagnation
            if best_ind.fitness == previous_best_fitness:
                stagnation_counter += 1
            else:
                stagnation_counter = 0
                previous_best_fitness = best_ind.fitness

            if best_ind.fitness == max_fitness:
                print(f"\n\n--- RESULT FOUND ---")
                print(f"Solution found in Generation {gen}!")
                print(f"Time: {time.time() - start_time:.4f}s")
                return best_ind

            if stagnation_counter >= STAGNATION_LIMIT:
                print(f"\n--- STAGNATION LIMIT REACHED ({STAGNATION_LIMIT} gens) ---")
                print(f"Stopping early. Best solution found so far has fitness {best_ind.fitness}.")
                print(f"Time: {time.time() - start_time:.4f}s")
                return best_ind

        print("\nMax generations reached.")
        return self.population[0]


# Main Execution
if __name__ == "__main__":
    print("=== KNIGHT'S TOUR: EVOLUTIONARY SOLVER ===")
    
    # Input Size
    while True:
        try:
            sz = int(input("Enter Board Size (5-10): "))
            if 5 <= sz <= 10: 
                break
            print("Please enter a number between 5 and 10.")
        except: 
            pass

    # Input Start Position
    while True:
        try:
            print(f"Enter Start Position (Row Col) from 1 to {sz}: ")
            inp = input("> ").split()
            r, c = int(inp[0]), int(inp[1])
            if 1 <= r <= sz and 1 <= c <= sz:
                start_node = (r-1) * sz + (c-1)
                break
            print("Out of bounds.")
        except:
            print("Invalid input. Format: 1 1")

    # Run Algorithm
    ca = CulturalAlgorithm(board_size=sz, start_pos=start_node, pop_size=150, max_gen=1000)
    tour_ind = ca.run()
    tour = tour_ind.chromosome
    
    # Show Result
    print("\n--- FINAL CHROMOSOME (PATH) ---")
    valid = 0
    board = Board(sz)
    
    grid = [[0]*sz for _ in range(sz)]
    for idx, sq in enumerate(tour):
        r, c = divmod(sq, sz)
        grid[r][c] = idx + 1
        if idx < len(tour)-1:
            if board.is_valid_move(sq, tour[idx+1]): 
                valid += 1

    for row in grid:
        print("\t".join(f"{x:2}" for x in row))
        
    print(f"\nFinal Validity: {valid}/{sz*sz - 1}")
    if valid == sz*sz - 1:
        print("Result: SUCCESS ✅")
    else:
        print("Result: FAILED ❌")