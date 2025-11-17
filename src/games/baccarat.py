"""Baccarat card game implementation"""

import random
from typing import Tuple, List


class BaccaratGame:
    """Simplified Baccarat casino game"""
    
    # Card values in Baccarat
    CARD_VALUES = {
        'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
        '6': 6, '7': 7, '8': 8, '9': 9,
        '10': 0, 'J': 0, 'Q': 0, 'K': 0
    }
    
    CARDS = list(CARD_VALUES.keys())
    
    BET_TYPES = ['jogador', 'banca', 'empate', 'player', 'banker', 'tie']
    
    @staticmethod
    def normalize_bet(bet_type: str) -> str:
        """Normalize bet type"""
        bet_lower = bet_type.lower()
        if bet_lower in ['jogador', 'player']:
            return 'jogador'
        elif bet_lower in ['banca', 'banker']:
            return 'banca'
        elif bet_lower in ['empate', 'tie']:
            return 'empate'
        return bet_lower
    
    @staticmethod
    def validate_bet(bet_type: str) -> bool:
        """Validate bet type"""
        return bet_type.lower() in BaccaratGame.BET_TYPES
    
    @staticmethod
    def deal_hand() -> List[str]:
        """Deal a hand of 2 cards"""
        return random.choices(BaccaratGame.CARDS, k=2)
    
    @staticmethod
    def calculate_hand_value(hand: List[str]) -> int:
        """Calculate hand value (last digit of sum)"""
        total = sum(BaccaratGame.CARD_VALUES[card] for card in hand)
        return total % 10
    
    @staticmethod
    def should_draw_third(hand_value: int, is_banker: bool = False, player_third: str = None) -> bool:
        """Determine if third card should be drawn (simplified rules)"""
        if is_banker:
            # Simplified banker rules
            if hand_value <= 2:
                return True
            elif hand_value == 3 and (player_third is None or BaccaratGame.CARD_VALUES.get(player_third, 0) != 8):
                return True
            elif hand_value <= 5 and player_third is None:
                return True
            return False
        else:
            # Player draws on 0-5, stands on 6-7
            return hand_value <= 5
    
    @staticmethod
    def play_game() -> Tuple[str, List[str], List[str], int, int]:
        """
        Play a complete baccarat game
        Returns: (winner, player_hand, banker_hand, player_value, banker_value)
        """
        # Deal initial hands
        player_hand = BaccaratGame.deal_hand()
        banker_hand = BaccaratGame.deal_hand()
        
        player_value = BaccaratGame.calculate_hand_value(player_hand)
        banker_value = BaccaratGame.calculate_hand_value(banker_hand)
        
        # Check for natural win (8 or 9)
        if player_value >= 8 or banker_value >= 8:
            if player_value > banker_value:
                return 'jogador', player_hand, banker_hand, player_value, banker_value
            elif banker_value > player_value:
                return 'banca', player_hand, banker_hand, player_value, banker_value
            else:
                return 'empate', player_hand, banker_hand, player_value, banker_value
        
        # Player's third card
        player_third = None
        if BaccaratGame.should_draw_third(player_value):
            player_third = random.choice(BaccaratGame.CARDS)
            player_hand.append(player_third)
            player_value = BaccaratGame.calculate_hand_value(player_hand)
        
        # Banker's third card
        if BaccaratGame.should_draw_third(banker_value, is_banker=True, player_third=player_third):
            banker_hand.append(random.choice(BaccaratGame.CARDS))
            banker_value = BaccaratGame.calculate_hand_value(banker_hand)
        
        # Determine winner
        if player_value > banker_value:
            winner = 'jogador'
        elif banker_value > player_value:
            winner = 'banca'
        else:
            winner = 'empate'
        
        return winner, player_hand, banker_hand, player_value, banker_value
    
    @staticmethod
    def calculate_win(winner: str, bet_type: str) -> Tuple[bool, float]:
        """
        Calculate win and multiplier
        Returns: (won, multiplier)
        """
        bet_type = BaccaratGame.normalize_bet(bet_type)
        
        if bet_type == winner:
            if bet_type == 'jogador':
                return True, 2.0  # 1:1 payout (2x total)
            elif bet_type == 'banca':
                return True, 1.95  # 1:1 minus 5% commission
            elif bet_type == 'empate':
                return True, 9.0   # 8:1 payout
        
        return False, 0.0
    
    @staticmethod
    def format_hand(hand: List[str], value: int) -> str:
        """Format hand for display"""
        cards_str = ' '.join(hand)
        return f"🃏 {cards_str} = **{value}**"
