"""Dice game implementation"""

import random
from typing import Tuple


class DiceGame:
    """Simple dice betting game"""
    
    @staticmethod
    def roll_dice(num_dice: int = 2) -> list:
        """Roll dice"""
        return [random.randint(1, 6) for _ in range(num_dice)]
    
    @staticmethod
    def play_over_under(bet_type: str, threshold: int = 7) -> Tuple[bool, list, int, float]:
        """
        Play over/under game with 2 dice
        Returns: (won, dice, total, multiplier)
        """
        dice = DiceGame.roll_dice(2)
        total = sum(dice)
        
        bet_type = bet_type.lower()
        
        won = False
        multiplier = 2.0
        
        if bet_type in ['over', 'acima'] and total > threshold:
            won = True
        elif bet_type in ['under', 'abaixo'] and total < threshold:
            won = True
        elif bet_type == 'seven' or bet_type == 'sete' and total == threshold:
            won = True
            multiplier = 5.0  # Higher payout for exact 7
        
        return won, dice, total, multiplier
    
    @staticmethod
    def play_high_low(prediction: str) -> Tuple[bool, int, float]:
        """
        Play high/low game with 1 die
        Returns: (won, roll, multiplier)
        """
        roll = random.randint(1, 6)
        prediction = prediction.lower()
        
        won = False
        multiplier = 2.0
        
        # High = 4, 5, 6 | Low = 1, 2, 3
        if prediction in ['high', 'alto'] and roll >= 4:
            won = True
        elif prediction in ['low', 'baixo'] and roll <= 3:
            won = True
        
        return won, roll, multiplier
    
    @staticmethod
    def play_specific_number(bet_number: int) -> Tuple[bool, int, float]:
        """
        Bet on a specific number
        Returns: (won, roll, multiplier)
        """
        roll = random.randint(1, 6)
        won = roll == bet_number
        multiplier = 6.0  # 6x payout for specific number
        
        return won, roll, multiplier
    
    @staticmethod
    def format_dice(dice: list) -> str:
        """Format dice with emojis"""
        dice_emoji = {
            1: '⚀',
            2: '⚁',
            3: '⚂',
            4: '⚃',
            5: '⚄',
            6: '⚅'
        }
        return ' '.join([dice_emoji.get(d, '?') for d in dice])
