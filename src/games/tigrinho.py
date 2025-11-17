"""Tigrinho (Fortune Tiger) slot machine game implementation"""

import random
import asyncio
from typing import Tuple, List


class TigrinhoGame:
    """
    Fortune Tiger (Tigrinho) slot machine game
    A 3x3 grid slot game with tiger-themed symbols
    """
    
    # Symbols with their weights and values
    # Higher weight = more common, higher value = bigger payout
    SYMBOLS = {
        '🪙': {'weight': 40, 'value': 2, 'name': 'Moeda'},      # Coin - most common
        '🎋': {'weight': 30, 'value': 3, 'name': 'Bambu'},      # Bamboo
        '🏮': {'weight': 25, 'value': 5, 'name': 'Lanterna'},   # Lantern
        '💰': {'weight': 20, 'value': 8, 'name': 'Ouro'},       # Gold
        '🐉': {'weight': 15, 'value': 12, 'name': 'Dragão'},    # Dragon
        '🎴': {'weight': 10, 'value': 20, 'name': 'Carta'},     # Card
        '🐅': {'weight': 5, 'value': 50, 'name': 'Tigre'},      # Tiger - rare, big win
        '💎': {'weight': 2, 'value': 100, 'name': 'Diamante'},  # Diamond - very rare jackpot
    }
    
    @staticmethod
    def spin() -> List[List[str]]:
        """
        Spin the Tigrinho slot machine (3x3 grid)
        Returns a 3x3 matrix of symbols
        """
        symbols = []
        weights = []
        
        for symbol, data in TigrinhoGame.SYMBOLS.items():
            symbols.append(symbol)
            weights.append(data['weight'])
        
        # Create 3x3 grid
        grid = []
        for _ in range(3):
            row = random.choices(symbols, weights=weights, k=3)
            grid.append(row)
        
        return grid
    
    @staticmethod
    def check_lines(grid: List[List[str]]) -> List[Tuple[str, int, str]]:
        """
        Check all winning lines in the grid
        Returns list of (symbol, multiplier, line_type) for each winning line
        """
        wins = []
        
        # Check horizontal lines (rows)
        for i, row in enumerate(grid):
            if row[0] == row[1] == row[2]:
                symbol = row[0]
                multiplier = TigrinhoGame.SYMBOLS[symbol]['value']
                wins.append((symbol, multiplier, f'Linha {i+1}'))
        
        # Check vertical lines (columns)
        for col in range(3):
            if grid[0][col] == grid[1][col] == grid[2][col]:
                symbol = grid[0][col]
                multiplier = TigrinhoGame.SYMBOLS[symbol]['value']
                wins.append((symbol, multiplier, f'Coluna {col+1}'))
        
        # Check diagonal lines
        if grid[0][0] == grid[1][1] == grid[2][2]:
            symbol = grid[0][0]
            multiplier = TigrinhoGame.SYMBOLS[symbol]['value']
            wins.append((symbol, multiplier, 'Diagonal ↘️'))
        
        if grid[0][2] == grid[1][1] == grid[2][0]:
            symbol = grid[0][2]
            multiplier = TigrinhoGame.SYMBOLS[symbol]['value']
            wins.append((symbol, multiplier, 'Diagonal ↙️'))
        
        return wins
    
    @staticmethod
    def calculate_win(grid: List[List[str]]) -> Tuple[bool, float, List[str]]:
        """
        Calculate total winnings from grid
        Returns: (won, total_multiplier, descriptions)
        """
        wins = TigrinhoGame.check_lines(grid)
        
        if not wins:
            return False, 0.0, []
        
        total_multiplier = sum(multiplier for _, multiplier, _ in wins)
        descriptions = []
        
        for symbol, multiplier, line_type in wins:
            name = TigrinhoGame.SYMBOLS[symbol]['name']
            descriptions.append(f'{line_type}: 3x {symbol} {name} ({multiplier}x)')
        
        return True, float(total_multiplier), descriptions
    
    @staticmethod
    def format_grid(grid: List[List[str]]) -> str:
        """Format grid for display"""
        lines = []
        lines.append('┌─────────┐')
        for row in grid:
            lines.append(f'│ {row[0]} {row[1]} {row[2]} │')
        lines.append('└─────────┘')
        return '\n'.join(lines)
    
    @staticmethod
    def format_spinning_frame(frame: int) -> str:
        """
        Create spinning animation frame
        Shows different random symbols for animation effect
        """
        symbols = list(TigrinhoGame.SYMBOLS.keys())
        grid = []
        for _ in range(3):
            row = [random.choice(symbols) for _ in range(3)]
            grid.append(row)
        
        return TigrinhoGame.format_grid(grid)
    
    @staticmethod
    def get_symbol_name(symbol: str) -> str:
        """Get the name of a symbol"""
        return TigrinhoGame.SYMBOLS.get(symbol, {}).get('name', 'Desconhecido')
