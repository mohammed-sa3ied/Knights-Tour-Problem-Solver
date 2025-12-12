# Knight's Tour Problem Solver 🐴♟️

A comprehensive solution to the **Knight's Tour Problem** using **Cultural Algorithm** and **Backtracking** with an interactive GUI.

## 📋 Project Overview

The Knight's Tour is a classic chess problem where a knight must visit every square on a chessboard exactly once. This project implements two approaches:

1. **Cultural Algorithm (CA)** - An evolutionary approach with belief space
2. **Backtracking** - A systematic search with Warnsdorff's heuristic

## 🚀 Features

✅ Interactive GUI with chessboard visualization  
✅ Two powerful algorithms (Cultural Algorithm & Backtracking)  
✅ Adjustable board size (5×5 to 10×10)  
✅ Click to select starting position  
✅ Real-time path visualization  
✅ Solution database for tracking results  
✅ Progress monitoring and statistics

## 📁 Project Structure

```
KnightTourProject/
│
├── README.md
├── requirements.txt
│
├── config/
│   └── config.py              # Configuration parameters
│
├── core/
│   ├── board.py               # Board representation
│   ├── individual.py          # Individual chromosome
│   ├── population.py          # Population management
│   ├── belief_space.py        # Belief space for CA
│   ├── fitness.py             # Fitness evaluation functions
│   ├── cultural_algorithm.py  # Cultural Algorithm implementation
│   └── backtracking.py        # Backtracking solver
│
├── gui/
│   └── visualization.py       # GUI implementation
│
├── db/
│   └── database.py            # Solution database
│
├── utils/
│   └── utils.py               # Utility functions
│
└── main.py                    # Main entry point
```

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- tkinter (usually comes with Python)

### Setup

1. **Clone the repository:**

```bash
git clone <repository-url>
cd KnightTourProject
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the application:**

```bash
python main.py
```

## 📖 Usage

### GUI Mode

1. **Launch the application:**

   ```bash
   python main.py
   ```

2. **Select board size** (5-10) using the spinner

3. **Click on any square** to set the starting position

4. **Choose algorithm:**

   - **Cultural Algorithm**: Faster, uses evolutionary approach
   - **Backtracking**: Systematic, guaranteed solution (if exists)

5. **Click START** to begin solving

6. **Watch** the knight's path being visualized in real-time

### Command Line Mode

You can also use the core algorithms directly:

```python
from core.cultural_algorithm import CulturalAlgorithm
from core.board import Board

# Create and run Cultural Algorithm
ca = CulturalAlgorithm(board_size=8, start_pos=0)
solution = ca.run()

if solution:
    print(f"Solution found! Fitness: {solution.get_fitness()}")
    print(f"Path: {solution.chromosome}")
```

## 🧬 Algorithms Explained

### Cultural Algorithm

The Cultural Algorithm combines:

- **Population Space**: Evolving candidate solutions
- **Belief Space**: Storing learned knowledge
  - Situational: Best solutions found
  - Normative: Statistical patterns
  - Historical: Common move sequences

**Key Features:**

- Smart initialization with Warnsdorff's heuristic
- Order crossover for permutation chromosomes
- Adaptive mutation based on belief space
- Stagnation detection and population restart

### Backtracking

Classic recursive approach with optimizations:

- **Warnsdorff's Heuristic**: Always choose the square with fewest onward moves
- Efficient pruning of search tree
- Guaranteed to find solution if one exists

## ⚙️ Configuration

Edit `config/config.py` to customize:

```python
# Cultural Algorithm Parameters
CA_POPULATION_SIZE = 400
CA_MAX_GENERATIONS = 3000
CA_CROSSOVER_PROB = 0.9
CA_MUTATION_PROB = 0.3

# GUI Settings
GUI_CELL_SIZE = 60
GUI_UPDATE_INTERVAL = 5
```

## 📊 Database

Solutions are automatically saved to `db/knight_tour.db` including:

- Board size and starting position
- Algorithm used
- Complete solution path
- Fitness and generation count
- Execution time

View saved solutions:

```python
from db.database import KnightTourDatabase

db = KnightTourDatabase()
solutions = db.get_solutions_by_board_size(8)
for sol in solutions:
    print(f"Solution {sol['id']}: Fitness {sol['fitness']}")
```

## 🎓 Educational Value

This project demonstrates:

- **Evolutionary Algorithms**: Cultural Algorithm implementation
- **Search Algorithms**: Backtracking with heuristics
- **GUI Programming**: Tkinter-based interactive interface
- **Software Design**: Modular, extensible architecture
- **Data Persistence**: SQLite database integration

## 🐛 Troubleshooting

**Issue**: GUI doesn't start

- **Solution**: Ensure tkinter is installed (`sudo apt-get install python3-tk` on Linux)

**Issue**: Algorithm is too slow

- **Solution**: Reduce `CA_POPULATION_SIZE` or `CA_MAX_GENERATIONS` in config

**Issue**: No solution found for larger boards

- **Solution**: Try Backtracking or increase `CA_MAX_GENERATIONS`

## 📝 License

This project is created for educational purposes.

## 👥 Contributors

- [Your Name]

## 🙏 Acknowledgments

- Warnsdorff's heuristic for knight's tour
- Cultural Algorithm framework by Reynolds
- Chess board visualization inspired by classical chess programs

---

**Made with ♞ for AI Course Project**
