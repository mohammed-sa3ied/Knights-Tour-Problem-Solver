"""
Database module for storing Knight's Tour solutions.
"""

import sqlite3
import json
from datetime import datetime
import os


class KnightTourDatabase:
    """Database manager for Knight's Tour solutions."""
    
    def __init__(self, db_path=None):
        if db_path is None:
            # Get the project root directory
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(project_root, "db", "knight_tour_new.db")
        
        self.db_path = db_path
        self._create_database()
    
    def _create_database(self):
        """Create database and tables if they don't exist."""
        # Create directory if it doesn't exist
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Solutions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                board_size INTEGER NOT NULL,
                start_position INTEGER NOT NULL,
                algorithm TEXT NOT NULL,
                chromosome TEXT NOT NULL,
                fitness INTEGER NOT NULL,
                generations INTEGER,
                time_seconds REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                board_size INTEGER NOT NULL,
                algorithm TEXT NOT NULL,
                avg_generations REAL,
                avg_time REAL,
                success_rate REAL,
                total_runs INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_solution(self, board_size, start_pos, algorithm, chromosome, 
                     fitness, generations=None, time_seconds=None):
        """
        Save a solution to the database.
        
        Args:
            board_size: Size of the board
            start_pos: Starting square index
            algorithm: Algorithm used ("CA", "Backtracking", etc.)
            chromosome: Solution chromosome (list of square indices)
            fitness: Fitness value
            generations: Number of generations (for evolutionary algorithms)
            time_seconds: Time taken in seconds
        
        Returns:
            int: ID of the saved solution
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO solutions 
            (board_size, start_position, algorithm, chromosome, fitness, generations, time_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (board_size, start_pos, algorithm, json.dumps(chromosome), 
              fitness, generations, time_seconds))
        
        solution_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return solution_id
    
    def get_solution(self, solution_id):
        """
        Retrieve a solution by ID.
        
        Returns:
            dict: Solution data or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM solutions WHERE id = ?', (solution_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'board_size': row['board_size'],
                'start_position': row['start_position'],
                'algorithm': row['algorithm'],
                'chromosome': json.loads(row['chromosome']),
                'fitness': row['fitness'],
                'generations': row['generations'],
                'time_seconds': row['time_seconds'],
                'timestamp': row['timestamp']
            }
        return None
    
    def get_solutions_by_board_size(self, board_size, limit=10):
        """Get recent solutions for a specific board size."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM solutions 
            WHERE board_size = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (board_size, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        solutions = []
        for row in rows:
            solutions.append({
                'id': row['id'],
                'board_size': row['board_size'],
                'start_position': row['start_position'],
                'algorithm': row['algorithm'],
                'chromosome': json.loads(row['chromosome']),
                'fitness': row['fitness'],
                'generations': row['generations'],
                'time_seconds': row['time_seconds'],
                'timestamp': row['timestamp']
            })
        
        return solutions
    
    def get_best_solutions(self, board_size, algorithm=None, limit=5):
        """Get best solutions for a board size and algorithm."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if algorithm:
            cursor.execute('''
                SELECT * FROM solutions 
                WHERE board_size = ? AND algorithm = ?
                ORDER BY fitness DESC, time_seconds ASC
                LIMIT ?
            ''', (board_size, algorithm, limit))
        else:
            cursor.execute('''
                SELECT * FROM solutions 
                WHERE board_size = ?
                ORDER BY fitness DESC, time_seconds ASC
                LIMIT ?
            ''', (board_size, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        solutions = []
        for row in rows:
            solutions.append({
                'id': row['id'],
                'board_size': row['board_size'],
                'start_position': row['start_position'],
                'algorithm': row['algorithm'],
                'fitness': row['fitness'],
                'generations': row['generations'],
                'time_seconds': row['time_seconds'],
                'timestamp': row['timestamp']
            })
        
        return solutions
    
    def update_statistics(self, board_size, algorithm, avg_generations, 
                         avg_time, success_rate, total_runs):
        """Update algorithm statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO statistics 
            (board_size, algorithm, avg_generations, avg_time, success_rate, total_runs)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (board_size, algorithm, avg_generations, avg_time, success_rate, total_runs))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self, board_size=None, algorithm=None):
        """Get statistics summary."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = 'SELECT * FROM statistics WHERE 1=1'
        params = []
        
        if board_size:
            query += ' AND board_size = ?'
            params.append(board_size)
        
        if algorithm:
            query += ' AND algorithm = ?'
            params.append(algorithm)
        
        query += ' ORDER BY timestamp DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        stats = []
        for row in rows:
            stats.append({
                'board_size': row['board_size'],
                'algorithm': row['algorithm'],
                'avg_generations': row['avg_generations'],
                'avg_time': row['avg_time'],
                'success_rate': row['success_rate'],
                'total_runs': row['total_runs'],
                'timestamp': row['timestamp']
            })
        
        return stats
    
    def clear_database(self):
        """Clear all data from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM solutions')
        cursor.execute('DELETE FROM statistics')
        
        conn.commit()
        conn.close()
