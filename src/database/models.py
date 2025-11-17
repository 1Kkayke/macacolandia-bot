"""Data models for the database"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User model"""
    user_id: str
    username: str
    coins: int = 1000
    total_won: int = 0
    total_lost: int = 0
    games_played: int = 0
    created_at: datetime = None
    last_daily: Optional[datetime] = None
    streak: int = 0


@dataclass
class Transaction:
    """Transaction model"""
    id: int
    user_id: str
    amount: int
    transaction_type: str
    description: Optional[str]
    timestamp: datetime


@dataclass
class Achievement:
    """Achievement model"""
    id: int
    user_id: str
    achievement_name: str
    unlocked_at: datetime


@dataclass
class GameHistory:
    """Game history model"""
    id: int
    user_id: str
    game_type: str
    bet_amount: int
    result: str
    winnings: int
    timestamp: datetime
