import time
import csv
import random
import os

from core.board import Board
from core.algorithms.backtracking.randomized_heuristic import BacktrackingSolver 
try:
    from core.algorithms.cultural.cultural_algorithm import CulturalAlgorithm
    CA_AVAILABLE = True
except ImportError:
    print("WARNING: Could not import CulturalAlgorithm. Ensure its supporting files (like belief_space) are present.")
    CA_AVAILABLE = False


# --- Experiment Settings ---
BOARD_SIZES = [5, 6, 7, 8, 9, 10]  # زودنا الأحجام
START_POSITIONS = [(0, 0), (0, -1), (-1, 0), (-1, -1), (2, 2)]  # الزوايا + مركز تقريبي

# --- Backtracking Experiment Function ---
def run_backtracking_experiment(size, start_pos_rc):
    board = Board(size)
    r, c = start_pos_rc
    # Adjust negative indices like -1 -> size-1
    r = r if r >= 0 else size + r
    c = c if c >= 0 else size + c
    start_square = r * size + c
    
    successful_runs = 0
    total_time = 0.0
    
    runs = 50 if size <= 6 else 20  # زيادة عدد التجارب للكبيرة
    print(f"\n[WARNSDORFF] Test {size}x{size} (Start: ({r},{c})), Runs: {runs}")
    
    for i in range(runs):
        solver = BacktrackingSolver(board)
        start_time = time.time()
        solution = solver.solve(start_square)
        end_time = time.time()
        
        run_time = end_time - start_time
        total_time += run_time
        
        if solution and len(solution) == board.num_squares:
            successful_runs += 1
            
    avg_time = total_time / runs
    success_rate = (successful_runs / runs) * 100
    
    print(f"   ✅ Success Rate: {success_rate:.2f}% | ⏱️ Avg Time: {avg_time:.6f}s")
    
    return {
        'Algorithm': 'Randomized Warnsdorff',
        'Size': size,
        'Start_R': r,
        'Start_C': c,
        'Success_Rate': success_rate,
        'Avg_Time_s': avg_time,
        'Best_Fitness': size*size - 1,
        'Runs': runs
    }


# --- Cultural Algorithm Experiment Function ---
def run_ca_experiment(size, start_pos_rc):
    if not CA_AVAILABLE:
        return None
        
    board = Board(size)
    r, c = start_pos_rc
    r = r if r >= 0 else size + r
    c = c if c >= 0 else size + c
    start_square = r * size + c
    
    successful_runs = 0
    total_time = 0.0
    best_fitness_overall = 0
    max_fitness = board.num_squares - 1
    runs = 5  # زيادة عدد التجارب
    
    print(f"\n[CULTURAL ALGORITHM] Test {size}x{size} (Start: ({r},{c})), Runs: {runs}")

    for i in range(runs):
        ca = CulturalAlgorithm(board_size=size, start_pos=start_square, pop_size=150, max_gen=1000)
        start_time = time.time()
        best_individual = ca.run()
        end_time = time.time()
        
        run_time = end_time - start_time
        total_time += run_time
        
        current_fitness = best_individual.fitness
        best_fitness_overall = max(best_fitness_overall, current_fitness)
        
        if current_fitness == max_fitness:
            successful_runs += 1
            
    avg_time = total_time / runs
    success_rate = (successful_runs / runs) * 100
    
    print(f"   ✅ Success Rate: {success_rate:.2f}% | 🔝 Best Fitness: {best_fitness_overall}/{max_fitness} | ⏱️ Avg Time: {avg_time:.4f}s")
    
    return {
        'Algorithm': 'Cultural Algorithm',
        'Size': size,
        'Start_R': r,
        'Start_C': c,
        'Success_Rate': success_rate,
        'Avg_Time_s': avg_time,
        'Best_Fitness': best_fitness_overall,
        'Runs': runs
    }


# --- Main Execution ---
if __name__ == "__main__":
    all_results = []
    
    for size in BOARD_SIZES:
        for r, c in START_POSITIONS:
            if r >= size or c >= size: continue 
            result = run_backtracking_experiment(size, (r, c))
            all_results.append(result)

    if CA_AVAILABLE:
        for size in BOARD_SIZES:
            for r, c in START_POSITIONS:
                if r >= size or c >= size: continue
                result = run_ca_experiment(size, (r, c))
                if result:
                    all_results.append(result)

    # Save CSV
    csv_file = 'comparison_results_extended.csv'
    fieldnames = ['Algorithm', 'Size', 'Start_R', 'Start_C', 'Success_Rate', 'Avg_Time_s', 'Best_Fitness', 'Runs']
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\n✅ Extended testing complete. Results saved to {csv_file}")
