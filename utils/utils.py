"""
Utility functions for Knight's Tour Project
"""

def square_to_position(square, board_size):
    """
    Convert square index to (row, col) position.
    
    Args:
        square: Square index (0 to board_size^2 - 1)
        board_size: Size of the board
    
    Returns:
        tuple: (row, col)
    """
    row = square // board_size
    col = square % board_size
    return (row, col)


def position_to_square(row, col, board_size):
    """
    Convert (row, col) position to square index.
    
    Args:
        row: Row number (0-indexed)
        col: Column number (0-indexed)
        board_size: Size of the board
    
    Returns:
        int: Square index
    """
    return row * board_size + col


def square_to_chess_notation(square, board_size):
    """
    Convert square index to chess notation (e.g., "a1", "h8").
    
    Args:
        square: Square index
        board_size: Size of the board
    
    Returns:
        str: Chess notation
    """
    row, col = square_to_position(square, board_size)
    file = chr(ord('a') + col)
    rank = str(row + 1)
    return f"{file}{rank}"


def chess_notation_to_square(notation, board_size):
    """
    Convert chess notation to square index.
    
    Args:
        notation: Chess notation (e.g., "a1")
        board_size: Size of the board
    
    Returns:
        int: Square index
    """
    file = notation[0]
    rank = int(notation[1:])
    col = ord(file) - ord('a')
    row = rank - 1
    return position_to_square(row, col, board_size)


def format_time(seconds):
    """
    Format seconds to human-readable string.
    
    Args:
        seconds: Time in seconds
    
    Returns:
        str: Formatted time string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{int(minutes)}m {secs:.1f}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)}h {int(minutes)}m"


def chromosome_to_path(chromosome, board_size):
    """
    Convert chromosome (list of square indices) to path (list of (row, col)).
    
    Args:
        chromosome: List of square indices
        board_size: Size of the board
    
    Returns:
        list: List of (row, col) tuples
    """
    return [square_to_position(sq, board_size) for sq in chromosome]


def path_to_chromosome(path, board_size):
    """
    Convert path (list of (row, col)) to chromosome (list of square indices).
    
    Args:
        path: List of (row, col) tuples
        board_size: Size of the board
    
    Returns:
        list: List of square indices
    """
    return [position_to_square(row, col, board_size) for row, col in path]


def validate_chromosome(chromosome, board_size):
    """
    Validate that chromosome is a valid permutation.
    
    Args:
        chromosome: List of square indices
        board_size: Size of the board
    
    Returns:
        bool: True if valid, False otherwise
    """
    expected_length = board_size * board_size
    if len(chromosome) != expected_length:
        return False
    
    if len(set(chromosome)) != expected_length:
        return False
    
    if not all(0 <= sq < expected_length for sq in chromosome):
        return False
    
    return True


def print_tour(chromosome, board_size):
    """
    Print tour in a formatted grid showing move order.
    
    Args:
        chromosome: List of square indices
        board_size: Size of the board
    """
    grid = [[0] * board_size for _ in range(board_size)]
    
    for move_num, square in enumerate(chromosome, 1):
        row, col = square_to_position(square, board_size)
        grid[row][col] = move_num
    
    # Print grid
    print("\nTour:")
    for row in grid:
        print(" ".join(f"{num:3d}" for num in row))
    print()


def save_tour_to_file(chromosome, board_size, filename):
    """
    Save tour to a text file.
    
    Args:
        chromosome: List of square indices
        board_size: Size of the board
        filename: Output filename
    """
    with open(filename, 'w') as f:
        f.write(f"Board Size: {board_size}x{board_size}\n")
        f.write(f"Tour Length: {len(chromosome)}\n\n")
        
        # Write as grid
        grid = [[0] * board_size for _ in range(board_size)]
        for move_num, square in enumerate(chromosome, 1):
            row, col = square_to_position(square, board_size)
            grid[row][col] = move_num
        
        for row in grid:
            f.write(" ".join(f"{num:3d}" for num in row) + "\n")
        
        # Write as sequence
        f.write("\nSequence:\n")
        for i, square in enumerate(chromosome, 1):
            notation = square_to_chess_notation(square, board_size)
            f.write(f"{i}. {notation} ")
            if i % 8 == 0:
                f.write("\n")


def load_tour_from_file(filename):
    """
    Load tour from a text file.
    
    Args:
        filename: Input filename
    
    Returns:
        tuple: (chromosome, board_size) or (None, None) if failed
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        # Parse board size
        board_size = int(lines[0].split(":")[1].split("x")[0].strip())
        
        # Parse grid
        grid_lines = lines[3:3+board_size]
        grid = []
        for line in grid_lines:
            grid.append([int(x) for x in line.split()])
        
        # Convert to chromosome
        chromosome = [0] * (board_size * board_size)
        for row_idx, row in enumerate(grid):
            for col_idx, move_num in enumerate(row):
                square = position_to_square(row_idx, col_idx, board_size)
                chromosome[move_num - 1] = square
        
        return chromosome, board_size
    except:
        return None, None