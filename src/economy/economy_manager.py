"""Economy management system"""

from typing import Tuple
from src.database.db_manager import DatabaseManager


class EconomyManager:
    """Manages the bot's economy system"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def get_balance(self, user_id: str, username: str) -> int:
        """Get user's coin balance"""
        user = self.db.get_user(user_id, username)
        return user['coins']
    
    def add_coins(self, user_id: str, amount: int, reason: str = None) -> bool:
        """Add coins to user account"""
        if self.db.update_coins(user_id, amount):
            self.db.add_transaction(user_id, amount, 'earn', reason)
            return True
        return False
    
    def remove_coins(self, user_id: str, amount: int, reason: str = None) -> bool:
        """Remove coins from user account"""
        if self.db.update_coins(user_id, -amount):
            self.db.add_transaction(user_id, -amount, 'spend', reason)
            return True
        return False
    
    def transfer_coins(self, from_user: str, to_user: str, amount: int) -> Tuple[bool, str]:
        """Transfer coins between users"""
        return self.db.transfer_coins(from_user, to_user, amount)
    
    def can_afford(self, user_id: str, username: str, amount: int) -> bool:
        """Check if user can afford an amount"""
        balance = self.get_balance(user_id, username)
        return balance >= amount
    
    def process_bet(self, user_id: str, username: str, bet_amount: int, 
                   game_type: str, won: bool, multiplier: float = 1.0) -> Tuple[bool, int]:
        """
        Process a bet outcome
        Returns: (success, net_change)
        """
        if not self.can_afford(user_id, username, bet_amount):
            return False, 0
        
        # Remove bet amount
        self.remove_coins(user_id, bet_amount, f'{game_type} - Aposta')
        
        if won:
            winnings = int(bet_amount * multiplier)
            self.add_coins(user_id, winnings, f'{game_type} - Vitória')
            net_change = winnings - bet_amount
            
            # Record game
            self.db.record_game(user_id, game_type, bet_amount, 'win', net_change)
            return True, net_change
        else:
            # Record game
            self.db.record_game(user_id, game_type, bet_amount, 'loss', -bet_amount)
            return True, -bet_amount
