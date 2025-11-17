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
        Process a bet outcome atomically
        Returns: (success, net_change)
        """
        # Ensure user exists first
        self.db.get_user(user_id, username)
        
        # Calculate the net change
        if won:
            winnings = int(bet_amount * multiplier)
            net_change = winnings - bet_amount
        else:
            net_change = -bet_amount
        
        # Process bet atomically in database
        success = self.db.process_bet_atomic(user_id, bet_amount, net_change, game_type, won)
        
        if not success:
            return False, 0
        
        return True, net_change
