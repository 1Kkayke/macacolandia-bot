"""Mines (Campo Minado) casino game implementation"""

import random
from typing import List, Tuple, Set


class MinesGame:
    """
    Mines game - A grid-based bomb avoidance game
    Player selects tiles to reveal. Each safe tile increases multiplier.
    Hit a mine and lose everything.
    """
    
    def __init__(self, grid_size: int = 5, num_mines: int = 5):
        """
        Initialize a new Mines game
        
        Args:
            grid_size: Size of the square grid (default 5x5 = 25 tiles)
            num_mines: Number of mines in the grid (default 5)
        """
        self.grid_size = grid_size
        self.num_mines = num_mines
        self.total_tiles = grid_size * grid_size
        self.safe_tiles = self.total_tiles - num_mines
        
        # Place mines randomly
        all_positions = [(i, j) for i in range(grid_size) for j in range(grid_size)]
        self.mine_positions = set(random.sample(all_positions, num_mines))
        
        # Track revealed tiles
        self.revealed: Set[Tuple[int, int]] = set()
        self.game_over = False
        self.hit_mine = False
    
    def reveal_tile(self, row: int, col: int) -> Tuple[bool, float]:
        """
        Reveal a tile at position (row, col)
        
        Returns:
            (is_safe, current_multiplier)
        """
        if self.game_over:
            return False, self.get_multiplier()
        
        if (row, col) in self.revealed:
            # Already revealed
            return True, self.get_multiplier()
        
        self.revealed.add((row, col))
        
        if (row, col) in self.mine_positions:
            # Hit a mine!
            self.hit_mine = True
            self.game_over = True
            return False, 0.0
        
        # Safe tile
        return True, self.get_multiplier()
    
    def get_multiplier(self) -> float:
        """
        Calculate current multiplier based on tiles revealed
        Multiplier increases exponentially with each safe tile
        """
        if self.hit_mine:
            return 0.0
        
        revealed_safe = len(self.revealed)
        if revealed_safe == 0:
            return 1.0
        
        # Multiplier formula: starts at 1.1x and increases exponentially
        # With 5 mines in 25 tiles (20 safe), full clear gives ~13x
        base = 1.0 + (0.5 * self.num_mines / self.safe_tiles)
        multiplier = base ** revealed_safe
        return round(multiplier, 2)
    
    def cash_out(self) -> float:
        """
        Cash out with current multiplier
        Returns final multiplier
        """
        if not self.hit_mine and not self.game_over:
            self.game_over = True
        return self.get_multiplier()
    
    def format_grid(self, reveal_all: bool = False) -> str:
        """
        Format the grid for display
        
        Args:
            reveal_all: If True, show all mines (for game over)
        """
        lines = []
        
        # Header with column numbers
        header = '   ' + ' '.join([str(i) for i in range(self.grid_size)])
        lines.append(header)
        lines.append('  ┌' + '─' * (self.grid_size * 2 - 1) + '┐')
        
        for i in range(self.grid_size):
            row_str = f'{i} │'
            for j in range(self.grid_size):
                if (i, j) in self.revealed:
                    if (i, j) in self.mine_positions:
                        row_str += '💣'  # Revealed mine
                    else:
                        row_str += '💎'  # Safe tile
                elif reveal_all and (i, j) in self.mine_positions:
                    row_str += '💣'  # Show mines at game end
                else:
                    row_str += '⬜'  # Unrevealed tile
                
                if j < self.grid_size - 1:
                    row_str += ' '
            
            row_str += '│'
            lines.append(row_str)
        
        lines.append('  └' + '─' * (self.grid_size * 2 - 1) + '┘')
        
        return '\n'.join(lines)
    
    def get_safe_tiles_remaining(self) -> int:
        """Get number of safe tiles not yet revealed"""
        return self.safe_tiles - len(self.revealed)
    
    @staticmethod
    def get_difficulty_settings(difficulty: str) -> Tuple[int, int]:
        """
        Get grid size and mine count for difficulty level
        
        Returns:
            (grid_size, num_mines)
        """
        settings = {
            'facil': (5, 3),    # 5x5 grid, 3 mines - easier, lower multiplier
            'medio': (5, 5),    # 5x5 grid, 5 mines - balanced
            'dificil': (5, 8),  # 5x5 grid, 8 mines - harder, higher multiplier
            'extremo': (5, 10), # 5x5 grid, 10 mines - very hard, very high multiplier
        }
        return settings.get(difficulty.lower(), settings['medio'])
