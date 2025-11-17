"""Keno lottery game implementation"""

import random
from typing import Tuple, List


class KenoGame:
    """Keno number lottery game"""
    
    MIN_NUMBERS = 1
    MAX_NUMBERS = 10
    NUMBER_RANGE = 40  # Numbers 1-40
    DRAW_COUNT = 10    # Draw 10 numbers
    
    # Multipliers based on matches
    MULTIPLIERS = {
        1: {1: 3.0},
        2: {1: 1.5, 2: 5.0},
        3: {2: 2.0, 3: 10.0},
        4: {2: 1.5, 3: 4.0, 4: 20.0},
        5: {3: 2.0, 4: 8.0, 5: 40.0},
        6: {3: 1.5, 4: 5.0, 5: 15.0, 6: 75.0},
        7: {4: 2.0, 5: 6.0, 6: 20.0, 7: 100.0},
        8: {5: 3.0, 6: 10.0, 7: 30.0, 8: 200.0},
        9: {5: 2.0, 6: 7.0, 7: 20.0, 8: 50.0, 9: 300.0},
        10: {6: 3.0, 7: 10.0, 8: 30.0, 9: 100.0, 10: 500.0}
    }
    
    @staticmethod
    def validate_numbers(numbers: List[int], count: int) -> bool:
        """Validate user selected numbers"""
        if len(numbers) != count:
            return False
        if count < KenoGame.MIN_NUMBERS or count > KenoGame.MAX_NUMBERS:
            return False
        if len(set(numbers)) != len(numbers):  # Check for duplicates
            return False
        if any(n < 1 or n > KenoGame.NUMBER_RANGE for n in numbers):
            return False
        return True
    
    @staticmethod
    def draw_numbers() -> List[int]:
        """Draw random numbers"""
        return random.sample(range(1, KenoGame.NUMBER_RANGE + 1), KenoGame.DRAW_COUNT)
    
    @staticmethod
    def check_matches(player_numbers: List[int], drawn_numbers: List[int]) -> int:
        """Check how many numbers matched"""
        return len(set(player_numbers) & set(drawn_numbers))
    
    @staticmethod
    def calculate_win(player_count: int, matches: int) -> Tuple[bool, float]:
        """
        Calculate win based on matches
        Returns: (won, multiplier)
        """
        if player_count not in KenoGame.MULTIPLIERS:
            return False, 0.0
        
        multiplier_table = KenoGame.MULTIPLIERS[player_count]
        multiplier = multiplier_table.get(matches, 0.0)
        won = multiplier > 0
        
        return won, multiplier
    
    @staticmethod
    def format_numbers(numbers: List[int], highlighted: List[int] = None) -> str:
        """Format numbers for display"""
        if highlighted is None:
            highlighted = []
        
        formatted = []
        for num in sorted(numbers):
            if num in highlighted:
                formatted.append(f"**{num}**")
            else:
                formatted.append(str(num))
        
        return ', '.join(formatted)
    
    @staticmethod
    def get_help_text() -> str:
        """Get help text for the game"""
        return (
            "**Como Jogar Keno:**\n"
            "1. Escolha de 1 a 10 números entre 1 e 40\n"
            "2. 10 números serão sorteados\n"
            "3. Quanto mais acertos, maior o prêmio!\n\n"
            "**Exemplos:**\n"
            "• Escolhendo 5 números: 3 acertos = 2x, 4 acertos = 8x, 5 acertos = 40x\n"
            "• Escolhendo 10 números: 10 acertos = 500x jackpot!"
        )
