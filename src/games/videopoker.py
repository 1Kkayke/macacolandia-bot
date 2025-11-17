"""Video Poker game implementation"""

import random
from typing import Tuple, List, Dict
from collections import Counter


class VideoPokerGame:
    """Simplified Video Poker (Jacks or Better)"""
    
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUITS = ['♠', '♥', '♦', '♣']
    
    # Hand rankings and payouts
    HAND_RANKS = {
        'Royal Flush': 800,
        'Straight Flush': 50,
        'Four of a Kind': 25,
        'Full House': 9,
        'Flush': 6,
        'Straight': 4,
        'Three of a Kind': 3,
        'Two Pair': 2,
        'Jacks or Better': 1,
    }
    
    def __init__(self):
        """Initialize video poker game"""
        self.deck = self._create_deck()
        self.hand = []
        self.held = [False] * 5
    
    def _create_deck(self) -> List[Dict[str, str]]:
        """Create a shuffled deck"""
        deck = []
        for rank in VideoPokerGame.RANKS:
            for suit in VideoPokerGame.SUITS:
                deck.append({'rank': rank, 'suit': suit})
        random.shuffle(deck)
        return deck
    
    def deal(self) -> List[Dict[str, str]]:
        """Deal initial 5 cards"""
        self.hand = [self.deck.pop() for _ in range(5)]
        self.held = [False] * 5
        return self.hand
    
    def hold_cards(self, positions: List[int]) -> bool:
        """Mark cards to hold (0-4)"""
        if not all(0 <= pos < 5 for pos in positions):
            return False
        
        self.held = [i in positions for i in range(5)]
        return True
    
    def draw(self) -> List[Dict[str, str]]:
        """Draw new cards for non-held positions"""
        for i in range(5):
            if not self.held[i]:
                self.hand[i] = self.deck.pop()
        return self.hand
    
    def evaluate_hand(self) -> Tuple[str, float]:
        """
        Evaluate poker hand
        Returns: (hand_name, multiplier)
        """
        ranks = [card['rank'] for card in self.hand]
        suits = [card['suit'] for card in self.hand]
        
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)
        
        # Convert face cards to numbers for straight checking
        rank_values = []
        for rank in ranks:
            if rank == 'A':
                rank_values.append(14)
            elif rank == 'K':
                rank_values.append(13)
            elif rank == 'Q':
                rank_values.append(12)
            elif rank == 'J':
                rank_values.append(11)
            else:
                rank_values.append(int(rank))
        
        rank_values.sort()
        
        # Check for flush
        is_flush = len(suit_counts) == 1
        
        # Check for straight
        is_straight = False
        if rank_values == list(range(rank_values[0], rank_values[0] + 5)):
            is_straight = True
        # Special case: A-2-3-4-5 (wheel)
        elif rank_values == [2, 3, 4, 5, 14]:
            is_straight = True
        
        # Get count patterns
        counts = sorted(rank_counts.values(), reverse=True)
        
        # Royal Flush (10-J-Q-K-A of same suit)
        if is_flush and is_straight and rank_values == [10, 11, 12, 13, 14]:
            return 'Royal Flush', VideoPokerGame.HAND_RANKS['Royal Flush']
        
        # Straight Flush
        if is_flush and is_straight:
            return 'Straight Flush', VideoPokerGame.HAND_RANKS['Straight Flush']
        
        # Four of a Kind
        if counts == [4, 1]:
            return 'Four of a Kind', VideoPokerGame.HAND_RANKS['Four of a Kind']
        
        # Full House
        if counts == [3, 2]:
            return 'Full House', VideoPokerGame.HAND_RANKS['Full House']
        
        # Flush
        if is_flush:
            return 'Flush', VideoPokerGame.HAND_RANKS['Flush']
        
        # Straight
        if is_straight:
            return 'Straight', VideoPokerGame.HAND_RANKS['Straight']
        
        # Three of a Kind
        if counts == [3, 1, 1]:
            return 'Three of a Kind', VideoPokerGame.HAND_RANKS['Three of a Kind']
        
        # Two Pair
        if counts == [2, 2, 1]:
            return 'Two Pair', VideoPokerGame.HAND_RANKS['Two Pair']
        
        # Jacks or Better (pair of J, Q, K, or A)
        if counts == [2, 1, 1, 1]:
            for rank, count in rank_counts.items():
                if count == 2 and rank in ['J', 'Q', 'K', 'A']:
                    return 'Jacks or Better', VideoPokerGame.HAND_RANKS['Jacks or Better']
        
        # No winning hand
        return 'High Card', 0.0
    
    @staticmethod
    def format_card(card: Dict[str, str]) -> str:
        """Format a card for display"""
        rank = card['rank']
        suit = card['suit']
        
        # Color suits
        if suit in ['♥', '♦']:
            return f"[{rank}{suit}]"
        else:
            return f"[{rank}{suit}]"
    
    def format_hand(self, show_held: bool = False) -> str:
        """Format hand for display"""
        hand_str = ""
        for i, card in enumerate(self.hand):
            card_str = VideoPokerGame.format_card(card)
            if show_held and self.held[i]:
                hand_str += f"**{card_str}** "
            else:
                hand_str += f"{card_str} "
        return hand_str
    
    def format_hand_with_positions(self) -> str:
        """Format hand with position numbers"""
        cards = self.format_hand()
        positions = "  0     1     2     3     4"
        return f"{cards}\n{positions}"
    
    @staticmethod
    def get_paytable() -> str:
        """Get paytable display"""
        table = "**💎 Tabela de Pagamento 💎**\n\n"
        for hand, payout in VideoPokerGame.HAND_RANKS.items():
            table += f"{hand}: **{payout}x**\n"
        return table
