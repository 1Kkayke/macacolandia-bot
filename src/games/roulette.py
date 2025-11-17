"""Roulette game implementation"""

import random
from typing import Tuple


class RouletteGame:
    """European Roulette game"""
    
    # Roulette numbers with colors
    RED_NUMBERS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    BLACK_NUMBERS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    
    @staticmethod
    def spin() -> int:
        """Spin the roulette wheel (0-36)"""
        return random.randint(0, 36)
    
    @staticmethod
    def get_color(number: int) -> str:
        """Get the color of a number"""
        if number == 0:
            return 'verde'
        elif number in RouletteGame.RED_NUMBERS:
            return 'vermelho'
        else:
            return 'preto'
    
    @staticmethod
    def check_bet(number: int, bet_type: str, bet_value: str) -> Tuple[bool, float]:
        """
        Check if bet wins and return multiplier
        Returns: (won, multiplier)
        """
        bet_type = bet_type.lower()
        bet_value = bet_value.lower()
        
        # Straight up (single number)
        if bet_type == 'numero' or bet_type == 'número':
            try:
                bet_num = int(bet_value)
                if number == bet_num:
                    return True, 35.0
            except ValueError:
                pass
            return False, 0.0
        
        # Red/Black
        if bet_type == 'cor':
            color = RouletteGame.get_color(number)
            if bet_value in ['vermelho', 'preto'] and bet_value == color:
                return True, 2.0
            return False, 0.0
        
        # Even/Odd
        if bet_type == 'paridade':
            if number == 0:
                return False, 0.0
            is_even = number % 2 == 0
            if (bet_value == 'par' and is_even) or (bet_value == 'impar' or bet_value == 'ímpar') and not is_even:
                return True, 2.0
            return False, 0.0
        
        # High/Low
        if bet_type == 'altura':
            if number == 0:
                return False, 0.0
            if (bet_value == 'baixo' and 1 <= number <= 18) or (bet_value == 'alto' and 19 <= number <= 36):
                return True, 2.0
            return False, 0.0
        
        return False, 0.0
    
    @staticmethod
    def get_bet_types() -> str:
        """Get formatted bet types description"""
        return """
**Tipos de Aposta:**
• `numero <0-36>` - Aposta em um número específico (35x)
• `cor <vermelho/preto>` - Aposta na cor (2x)
• `paridade <par/impar>` - Aposta em par ou ímpar (2x)
• `altura <baixo/alto>` - Baixo (1-18) ou Alto (19-36) (2x)
        """
