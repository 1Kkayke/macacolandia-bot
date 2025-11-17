"""Coin flip game implementation"""

import random
from typing import Tuple


class CoinFlipGame:
    """Simple coin flip betting game"""
    
    SIDES = {
        'cara': '👤',
        'coroa': '👑',
        'heads': '👤',
        'tails': '👑'
    }
    
    @staticmethod
    def flip() -> str:
        """Flip a coin and return the result"""
        return random.choice(['cara', 'coroa'])
    
    @staticmethod
    def validate_choice(choice: str) -> bool:
        """Validate if the choice is valid"""
        return choice.lower() in CoinFlipGame.SIDES
    
    @staticmethod
    def normalize_choice(choice: str) -> str:
        """Normalize the choice to cara or coroa"""
        choice_lower = choice.lower()
        if choice_lower in ['heads', 'cara']:
            return 'cara'
        elif choice_lower in ['tails', 'coroa']:
            return 'coroa'
        return choice_lower
    
    @staticmethod
    def check_win(result: str, bet: str) -> Tuple[bool, float]:
        """
        Check if bet won
        Returns: (won, multiplier)
        """
        normalized_bet = CoinFlipGame.normalize_choice(bet)
        won = result == normalized_bet
        multiplier = 2.0 if won else 0.0
        return won, multiplier
    
    @staticmethod
    def format_result(result: str) -> str:
        """Format result for display"""
        emoji = CoinFlipGame.SIDES.get(result, '🪙')
        name = 'Cara' if result == 'cara' else 'Coroa'
        return f"{emoji} **{name}**"
    
    @staticmethod
    def get_animation_frames() -> list:
        """Get animation frames for coin flipping"""
        return ['🪙', '💫', '✨', '⭐']
