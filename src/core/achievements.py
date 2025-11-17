"""Achievement definitions and management"""

from typing import Dict, List, Callable
from src.database.db_manager import DatabaseManager


class Achievement:
    """Achievement definition"""
    
    def __init__(self, name: str, title: str, description: str, 
                 emoji: str, condition: Callable, reward: int = 0):
        self.name = name
        self.title = title
        self.description = description
        self.emoji = emoji
        self.condition = condition
        self.reward = reward


class AchievementManager:
    """Manages achievements and checks"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.achievements = self._define_achievements()
    
    def _define_achievements(self) -> Dict[str, Achievement]:
        """Define all achievements"""
        achievements = {
            'first_game': Achievement(
                'first_game',
                'Primeira Aposta',
                'Jogou seu primeiro jogo',
                '🎮',
                lambda user_stats: user_stats['games_played'] >= 1,
                100
            ),
            'high_roller': Achievement(
                'high_roller',
                'Apostador de Elite',
                'Tenha 10.000 moedas ou mais',
                '💎',
                lambda user_stats: user_stats['coins'] >= 10000,
                500
            ),
            'veteran': Achievement(
                'veteran',
                'Veterano',
                'Jogue 100 jogos',
                '🎖️',
                lambda user_stats: user_stats['games_played'] >= 100,
                1000
            ),
            'lucky_streak': Achievement(
                'lucky_streak',
                'Sortudo',
                'Mantenha uma sequência de 7 dias de recompensas diárias',
                '🍀',
                lambda user_stats: user_stats['streak'] >= 7,
                500
            ),
            'big_winner': Achievement(
                'big_winner',
                'Grande Vencedor',
                'Ganhe 5.000 moedas no total',
                '🏆',
                lambda user_stats: user_stats['total_won'] >= 5000,
                250
            ),
            'millionaire': Achievement(
                'millionaire',
                'Milionário',
                'Acumule 50.000 moedas',
                '💰',
                lambda user_stats: user_stats['coins'] >= 50000,
                5000
            ),
        }
        return achievements
    
    def check_achievements(self, user_id: str, username: str) -> List[Achievement]:
        """Check and unlock new achievements for a user"""
        user = self.db.get_user(user_id, username)
        user_stats = dict(user)
        
        unlocked = []
        
        for achievement in self.achievements.values():
            if achievement.condition(user_stats):
                if self.db.unlock_achievement(user_id, achievement.name):
                    # Achievement just unlocked, give reward
                    if achievement.reward > 0:
                        self.db.update_coins(user_id, achievement.reward)
                        self.db.add_transaction(
                            user_id, 
                            achievement.reward, 
                            'achievement',
                            f'Conquista desbloqueada: {achievement.title}'
                        )
                    unlocked.append(achievement)
        
        return unlocked
    
    def get_achievement(self, name: str) -> Achievement:
        """Get achievement by name"""
        return self.achievements.get(name)
    
    def get_all_achievements(self) -> List[Achievement]:
        """Get all achievements"""
        return list(self.achievements.values())
