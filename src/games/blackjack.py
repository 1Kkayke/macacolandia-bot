"""Blackjack game implementation"""

import random
from typing import List, Tuple
from enum import Enum


class CardSuit(Enum):
    """Card suits"""
    HEARTS = '♥️'
    DIAMONDS = '♦️'
    CLUBS = '♣️'
    SPADES = '♠️'


class Card:
    """Playing card"""
    
    def __init__(self, rank: str, suit: CardSuit):
        self.rank = rank
        self.suit = suit
    
    def get_value(self) -> int:
        """Get card value for blackjack"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Aces are handled specially in hand calculation
        else:
            return int(self.rank)
    
    def __str__(self):
        return f"{self.rank}{self.suit.value}"


class Hand:
    """Blackjack hand"""
    
    def __init__(self):
        self.cards: List[Card] = []
    
    def add_card(self, card: Card):
        """Add a card to the hand"""
        self.cards.append(card)
    
    def get_value(self) -> int:
        """Calculate hand value with ace handling"""
        value = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                value += 11
            else:
                value += card.get_value()
        
        # Adjust for aces if busted
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def is_blackjack(self) -> bool:
        """Check if hand is a blackjack (21 with 2 cards)"""
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_busted(self) -> bool:
        """Check if hand is busted"""
        return self.get_value() > 21
    
    def __str__(self):
        return ' '.join([str(card) for card in self.cards])


class BlackjackGame:
    """Blackjack game"""
    
    def __init__(self):
        self.deck: List[Card] = []
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self._init_deck()
    
    def _init_deck(self):
        """Initialize a standard 52-card deck"""
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = list(CardSuit)
        
        self.deck = [Card(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(self.deck)
    
    def deal_card(self) -> Card:
        """Deal a card from the deck"""
        if len(self.deck) < 10:  # Reshuffle if running low
            self._init_deck()
        return self.deck.pop()
    
    def start_game(self):
        """Start a new game"""
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        
        # Deal initial cards
        self.player_hand.add_card(self.deal_card())
        self.dealer_hand.add_card(self.deal_card())
        self.player_hand.add_card(self.deal_card())
        self.dealer_hand.add_card(self.deal_card())
    
    def player_hit(self):
        """Player hits (takes another card)"""
        self.player_hand.add_card(self.deal_card())
    
    def dealer_play(self):
        """Dealer plays according to standard rules (hit until 17+)"""
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deal_card())
    
    def determine_winner(self) -> Tuple[str, float]:
        """
        Determine game winner and payout multiplier
        Returns: (result, multiplier)
        """
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        # Player busted
        if self.player_hand.is_busted():
            return 'dealer_win', 0.0
        
        # Player blackjack
        if self.player_hand.is_blackjack():
            if self.dealer_hand.is_blackjack():
                return 'push', 1.0  # Tie, return bet
            return 'player_blackjack', 2.5  # Blackjack pays 3:2
        
        # Dealer busted
        if self.dealer_hand.is_busted():
            return 'player_win', 2.0
        
        # Compare values
        if player_value > dealer_value:
            return 'player_win', 2.0
        elif player_value < dealer_value:
            return 'dealer_win', 0.0
        else:
            return 'push', 1.0  # Tie, return bet
    
    def get_player_hand_str(self) -> str:
        """Get formatted player hand"""
        return f"{self.player_hand} (Valor: {self.player_hand.get_value()})"
    
    def get_dealer_hand_str(self, hide_second: bool = False) -> str:
        """Get formatted dealer hand"""
        if hide_second and len(self.dealer_hand.cards) >= 2:
            return f"{self.dealer_hand.cards[0]} 🂠"
        return f"{self.dealer_hand} (Valor: {self.dealer_hand.get_value()})"
    
    def can_player_hit(self) -> bool:
        """Check if player can hit"""
        return not self.player_hand.is_busted() and not self.player_hand.is_blackjack()
