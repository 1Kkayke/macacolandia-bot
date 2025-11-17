"""Slot machine game implementation"""

import random
from typing import Tuple, List


class SlotsGame:
    """Slot machine game with 3 reels"""
    
    # Slot symbols with their weights (higher = more common)
    SYMBOLS = {
        '🍒': {'weight': 35, 'value': 2},    # Cherry - common, low value
        '🍋': {'weight': 30, 'value': 3},    # Lemon
        '🍊': {'weight': 25, 'value': 4},    # Orange
        '🍇': {'weight': 20, 'value': 5},    # Grape
        '🍉': {'weight': 15, 'value': 7},    # Watermelon
        '⭐': {'weight': 10, 'value': 10},   # Star
        '💎': {'weight': 5, 'value': 20},    # Diamond - rare, high value
        '🎰': {'weight': 3, 'value': 50},    # Jackpot - very rare
    }
    
    @staticmethod
    def spin() -> List[str]:
        """Spin the slot machine (3 reels)"""
        symbols = []
        weights = []
        
        for symbol, data in SlotsGame.SYMBOLS.items():
            symbols.append(symbol)
            weights.append(data['weight'])
        
        # Pick 3 symbols
        result = random.choices(symbols, weights=weights, k=3)
        return result
    
    @staticmethod
    def calculate_win(reels: List[str]) -> Tuple[bool, float, str]:
        """
        Calculate winnings from reel result
        Returns: (won, multiplier, description)
        """
        # Check for 3 of a kind
        if reels[0] == reels[1] == reels[2]:
            symbol = reels[0]
            multiplier = SlotsGame.SYMBOLS[symbol]['value']
            return True, float(multiplier), f'🎉 JACKPOT! 3x {symbol}'
        
        # Check for 2 of a kind
        if reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
            # Get the matching symbol
            if reels[0] == reels[1]:
                symbol = reels[0]
            elif reels[1] == reels[2]:
                symbol = reels[1]
            else:
                symbol = reels[0]
            
            multiplier = SlotsGame.SYMBOLS[symbol]['value'] * 0.5
            return True, multiplier, f'✨ 2x {symbol}'
        
        # No match
        return False, 0.0, 'Sem combinação'
    
    @staticmethod
    def format_reels(reels: List[str]) -> str:
        """Format reels for display"""
        return f"[ {reels[0]} | {reels[1]} | {reels[2]} ]"
