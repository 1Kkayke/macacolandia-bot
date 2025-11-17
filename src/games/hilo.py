"""Hi-Lo card game implementation"""

import random
from typing import Tuple


class HiLoGame:
    """Hi-Lo card guessing game"""
    
    CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    CARD_VALUES = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }
    
    CARD_EMOJIS = {
        '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣', '6': '6️⃣',
        '7': '7️⃣', '8': '8️⃣', '9': '9️⃣', '10': '🔟',
        'J': '🃏', 'Q': '👸', 'K': '🤴', 'A': '🅰️'
    }
    
    @staticmethod
    def draw_card() -> str:
        """Draw a random card"""
        return random.choice(HiLoGame.CARDS)
    
    @staticmethod
    def validate_guess(guess: str) -> bool:
        """Validate guess"""
        return guess.lower() in ['alto', 'baixo', 'igual', 'high', 'low', 'same']
    
    @staticmethod
    def normalize_guess(guess: str) -> str:
        """Normalize guess"""
        guess_lower = guess.lower()
        if guess_lower in ['alto', 'high']:
            return 'alto'
        elif guess_lower in ['baixo', 'low']:
            return 'baixo'
        elif guess_lower in ['igual', 'same']:
            return 'igual'
        return guess_lower
    
    @staticmethod
    def compare_cards(current: str, next_card: str, guess: str) -> Tuple[bool, float]:
        """
        Compare cards and check if guess was correct
        Returns: (won, multiplier)
        """
        current_value = HiLoGame.CARD_VALUES[current]
        next_value = HiLoGame.CARD_VALUES[next_card]
        
        guess = HiLoGame.normalize_guess(guess)
        
        won = False
        multiplier = 0.0
        
        if guess == 'alto' and next_value > current_value:
            won = True
            multiplier = 2.0
        elif guess == 'baixo' and next_value < current_value:
            won = True
            multiplier = 2.0
        elif guess == 'igual' and next_value == current_value:
            won = True
            multiplier = 14.0  # Higher payout for exact match
        
        return won, multiplier
    
    @staticmethod
    def format_card(card: str) -> str:
        """Format card for display"""
        emoji = HiLoGame.CARD_EMOJIS.get(card, '🎴')
        return f"{emoji} **{card}**"
    
    @staticmethod
    def get_odds(current: str) -> str:
        """Get odds description for current card"""
        value = HiLoGame.CARD_VALUES[current]
        
        higher = sum(1 for v in HiLoGame.CARD_VALUES.values() if v > value)
        lower = sum(1 for v in HiLoGame.CARD_VALUES.values() if v < value)
        same = sum(1 for v in HiLoGame.CARD_VALUES.values() if v == value) - 1  # -1 for current card
        
        total = len(HiLoGame.CARDS) - 1
        
        return (
            f"📊 **Probabilidades:**\n"
            f"🔺 Alto: {higher}/{total} ({higher/total*100:.1f}%)\n"
            f"🔻 Baixo: {lower}/{total} ({lower/total*100:.1f}%)\n"
            f"➖ Igual: {same}/{total} ({same/total*100:.1f}%) - 14x"
        )
