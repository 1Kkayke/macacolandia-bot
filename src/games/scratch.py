"""Scratch card game implementation"""

import random
from typing import Tuple, List


class ScratchCardGame:
    """Instant win scratch card game"""
    
    # Prize pool with probabilities (muito mais difícil - house edge alto)
    PRIZES = [
        {'multiplier': 0, 'label': 'Lost', 'emoji': '❌', 'weight': 70},  # 70% lose
        {'multiplier': 0.5, 'label': 'Half', 'emoji': '💸', 'weight': 15},  # 15% half (lose half)
        {'multiplier': 1.0, 'label': 'Tie', 'emoji': '🤝', 'weight': 8},  # 8% tie
        {'multiplier': 2.0, 'label': 'Double', 'emoji': '💰', 'weight': 4},  # 4% double
        {'multiplier': 3.0, 'label': 'Triple', 'emoji': '💎', 'weight': 1.8},  # 1.8% triple
        {'multiplier': 5.0, 'label': 'x5', 'emoji': '🌟', 'weight': 0.8},  # 0.8% x5
        {'multiplier': 10.0, 'label': 'x10', 'emoji': '⭐', 'weight': 0.3},  # 0.3% x10
        {'multiplier': 25.0, 'label': 'x25', 'emoji': '🎊', 'weight': 0.08},  # 0.08% x25
        {'multiplier': 100.0, 'label': 'JACKPOT!', 'emoji': '🎰', 'weight': 0.02},  # 0.02% jackpot
    ]
    
    CARD_SIZE = 9  # 3x3 grid
    
    @staticmethod
    def generate_card() -> List[dict]:
        """Generate a scratch card with random prizes"""
        prizes = []
        weights = [p['weight'] for p in ScratchCardGame.PRIZES]
        
        for _ in range(ScratchCardGame.CARD_SIZE):
            prize = random.choices(ScratchCardGame.PRIZES, weights=weights, k=1)[0]
            prizes.append(prize)
        
        return prizes
    
    @staticmethod
    def calculate_best_prize(card: List[dict]) -> Tuple[bool, float, dict]:
        """
        Get the best prize from the card
        Returns: (won, multiplier, prize_info)
        """
        best_prize = max(card, key=lambda p: p['multiplier'])
        won = best_prize['multiplier'] > 0
        return won, best_prize['multiplier'], best_prize
    
    @staticmethod
    def format_card_hidden() -> str:
        """Format hidden scratch card"""
        card = "```\n"
        card += "┌─────────┐\n"
        card += "│ ❓ ❓ ❓ │\n"
        card += "│ ❓ ❓ ❓ │\n"
        card += "│ ❓ ❓ ❓ │\n"
        card += "└─────────┘\n"
        card += "```"
        return card
    
    @staticmethod
    def format_card_revealed(card: List[dict], highlight_index: int = -1) -> str:
        """Format revealed scratch card"""
        card_str = "```\n"
        card_str += "┌─────────┐\n"
        
        for row in range(3):
            card_str += "│ "
            for col in range(3):
                index = row * 3 + col
                prize = card[index]
                emoji = prize['emoji']
                
                if index == highlight_index:
                    card_str += f">{emoji}< "
                else:
                    card_str += f"{emoji} "
            
            card_str += "│\n"
        
        card_str += "└─────────┘\n"
        card_str += "```"
        return card_str
    
    @staticmethod
    def format_prizes_list() -> str:
        """Format list of possible prizes"""
        prizes_text = "**Possible Prizes:**\n"
        for prize in ScratchCardGame.PRIZES:
            if prize['multiplier'] > 0:
                prizes_text += f"{prize['emoji']} {prize['label']} - {prize['multiplier']}x\n"
        return prizes_text
    
    @staticmethod
    def get_prize_distribution() -> str:
        """Get prize distribution info"""
        total_weight = sum(p['weight'] for p in ScratchCardGame.PRIZES)
        
        text = "**Odds:**\n"
        for prize in ScratchCardGame.PRIZES:
            if prize['multiplier'] >= 1.0:
                chance = (prize['weight'] / total_weight) * 100
                text += f"{prize['emoji']} {prize['label']}: {chance:.1f}%\n"
        
        return text
