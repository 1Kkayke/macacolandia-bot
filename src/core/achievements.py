"""Achievement definitions and management"""

from typing import Dict, List, Callable
from src.database.db_manager import DatabaseManager


class Achievement:
    def __init__(self, name: str, title: str, description: str, 
                 emoji: str, condition: Callable, reward: int = 0):
        self.name = name
        self.title = title
        self.description = description
        self.emoji = emoji
        self.condition = condition
        self.reward = reward


class AchievementManager:
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.achievements = self._define_achievements()
    
    def _define_achievements(self) -> Dict[str, Achievement]:
        achievements = {
            # Starter achievements
            'first_game': Achievement('first_game', 'First Timer', 'Play your first game', '🎮', lambda u: u['games_played'] >= 1, 100),
            'beginner': Achievement('beginner', 'Beginner', 'Play 5 games', '🌱', lambda u: u['games_played'] >= 5, 50),
            'getting_started': Achievement('getting_started', 'Getting Started', 'Play 10 games', '🎯', lambda u: u['games_played'] >= 10, 100),
            
            # Game count achievements
            'casual_player': Achievement('casual_player', 'Casual Player', 'Play 25 games', '🎲', lambda u: u['games_played'] >= 25, 200),
            'regular': Achievement('regular', 'Regular', 'Play 50 games', '🎪', lambda u: u['games_played'] >= 50, 500),
            'veteran': Achievement('veteran', 'Veteran', 'Play 100 games', '🎖️', lambda u: u['games_played'] >= 100, 1000),
            'expert': Achievement('expert', 'Expert', 'Play 250 games', '🏅', lambda u: u['games_played'] >= 250, 2500),
            'master': Achievement('master', 'Casino Master', 'Play 500 games', '👑', lambda u: u['games_played'] >= 500, 5000),
            'legend': Achievement('legend', 'Living Legend', 'Play 1000 games', '⭐', lambda u: u['games_played'] >= 1000, 10000),
            'god_tier': Achievement('god_tier', 'God Tier', 'Play 2500 games', '🌟', lambda u: u['games_played'] >= 2500, 25000),
            'unstoppable': Achievement('unstoppable', 'Unstoppable', 'Play 5000 games', '💫', lambda u: u['games_played'] >= 5000, 50000),
            
            # Coin achievements
            'first_coins': Achievement('first_coins', 'Got Coins', 'Have 100 coins', '🪙', lambda u: u['coins'] >= 100, 50),
            'getting_rich': Achievement('getting_rich', 'Getting Rich', 'Have 500 coins', '💵', lambda u: u['coins'] >= 500, 100),
            'moneybags': Achievement('moneybags', 'Moneybags', 'Have 1,000 coins', '💰', lambda u: u['coins'] >= 1000, 200),
            'wealthy': Achievement('wealthy', 'Wealthy', 'Have 5,000 coins', '💎', lambda u: u['coins'] >= 5000, 500),
            'high_roller': Achievement('high_roller', 'High Roller', 'Have 10,000 coins', '🎰', lambda u: u['coins'] >= 10000, 1000),
            'tycoon': Achievement('tycoon', 'Tycoon', 'Have 25,000 coins', '🏦', lambda u: u['coins'] >= 25000, 2500),
            'millionaire': Achievement('millionaire', 'Millionaire', 'Have 50,000 coins', '🤑', lambda u: u['coins'] >= 50000, 5000),
            'multi_millionaire': Achievement('multi_millionaire', 'Multi-Millionaire', 'Have 100,000 coins', '💸', lambda u: u['coins'] >= 100000, 10000),
            'billionaire': Achievement('billionaire', 'Billionaire', 'Have 500,000 coins', '🏰', lambda u: u['coins'] >= 500000, 50000),
            'trillionaire': Achievement('trillionaire', 'Trillionaire', 'Have 1,000,000 coins', '👑', lambda u: u['coins'] >= 1000000, 100000),
            
            # Win achievements
            'first_win': Achievement('first_win', 'First Win', 'Win your first game', '🎉', lambda u: u['games_won'] >= 1, 100),
            'lucky_one': Achievement('lucky_one', 'Lucky', 'Win 5 times', '🍀', lambda u: u['games_won'] >= 5, 100),
            'winner': Achievement('winner', 'Winner', 'Win 10 times', '🏆', lambda u: u['games_won'] >= 10, 200),
            'champion': Achievement('champion', 'Champion', 'Win 25 times', '🥇', lambda u: u['games_won'] >= 25, 500),
            'big_winner': Achievement('big_winner', 'Big Winner', 'Win 50 times', '🎊', lambda u: u['games_won'] >= 50, 1000),
            'dominator': Achievement('dominator', 'Dominator', 'Win 100 times', '👊', lambda u: u['games_won'] >= 100, 2000),
            'conqueror': Achievement('conqueror', 'Conqueror', 'Win 250 times', '⚔️', lambda u: u['games_won'] >= 250, 5000),
            'destroyer': Achievement('destroyer', 'Destroyer', 'Win 500 times', '💥', lambda u: u['games_won'] >= 500, 10000),
            
            # Total winnings achievements
            'small_profit': Achievement('small_profit', 'Small Profit', 'Win 1,000 coins total', '💵', lambda u: u['total_won'] >= 1000, 100),
            'good_profit': Achievement('good_profit', 'Good Profit', 'Win 5,000 coins total', '💰', lambda u: u['total_won'] >= 5000, 250),
            'big_profit': Achievement('big_profit', 'Big Profit', 'Win 10,000 coins total', '💎', lambda u: u['total_won'] >= 10000, 500),
            'huge_profit': Achievement('huge_profit', 'Huge Profit', 'Win 25,000 coins total', '🤑', lambda u: u['total_won'] >= 25000, 1000),
            'massive_profit': Achievement('massive_profit', 'Massive Profit', 'Win 50,000 coins total', '💸', lambda u: u['total_won'] >= 50000, 2500),
            'insane_profit': Achievement('insane_profit', 'Insane Profit', 'Win 100,000 coins total', '🏆', lambda u: u['total_won'] >= 100000, 5000),
            
            # Streak achievements
            'consistent': Achievement('consistent', 'Consistent', '3 days streak', '📅', lambda u: u['streak'] >= 3, 100),
            'dedicated': Achievement('dedicated', 'Dedicated', '5 days streak', '🔥', lambda u: u['streak'] >= 5, 250),
            'lucky_streak': Achievement('lucky_streak', 'Lucky Streak', '7 days streak', '🍀', lambda u: u['streak'] >= 7, 500),
            'committed': Achievement('committed', 'Committed', '10 days streak', '💪', lambda u: u['streak'] >= 10, 1000),
            'persistent': Achievement('persistent', 'Persistent', '15 days streak', '🎯', lambda u: u['streak'] >= 15, 1500),
            'unstoppable_streak': Achievement('unstoppable_streak', 'Unstoppable', '21 days streak', '⚡', lambda u: u['streak'] >= 21, 2500),
            'month_streak': Achievement('month_streak', 'Full Month', '30 days streak', '📆', lambda u: u['streak'] >= 30, 5000),
            'two_months': Achievement('two_months', 'Two Months', '60 days streak', '🌟', lambda u: u['streak'] >= 60, 10000),
            'three_months': Achievement('three_months', 'Three Months', '90 days streak', '💫', lambda u: u['streak'] >= 90, 20000),
            'half_year': Achievement('half_year', 'Half Year', '180 days streak', '👑', lambda u: u['streak'] >= 180, 50000),
            'full_year': Achievement('full_year', 'Full Year', '365 days streak', '🏆', lambda u: u['streak'] >= 365, 100000),
            
            # Loss achievements
            'disaster': Achievement('disaster', 'Disaster', 'Lose 1,000 coins total', '💀', lambda u: u['total_lost'] >= 1000, 100),
            'bankruptcy': Achievement('bankruptcy', 'Bankruptcy', 'Lose 5,000 coins total', '☠️', lambda u: u['total_lost'] >= 5000, 250),
            'rock_bottom': Achievement('rock_bottom', 'Rock Bottom', 'Lose 10,000 coins total', '🕳️', lambda u: u['total_lost'] >= 10000, 500),
            
            # Special number achievements
            'lucky_number': Achievement('lucky_number', 'Lucky Number', 'Have exactly 6,969 coins', '😏', lambda u: u['coins'] == 6969, 6969),
            'illuminati': Achievement('illuminati', 'Illuminati Confirmed', 'Have exactly 666 or 777 coins', '👁️', lambda u: u['coins'] in [666, 777], 1000),
            
            # Meme achievements
            'skibidi_toilet': Achievement('skibidi_toilet', 'Skibidi Toilet', 'Play exactly 69 times', '🚽', lambda u: u['games_played'] == 69, 690),
            'rizz_god': Achievement('rizz_god', 'Rizz God', 'Have exactly 777 coins', '😎', lambda u: u['coins'] == 777, 777),
            'sigma_grindset': Achievement('sigma_grindset', 'Sigma Grindset', 'Play 500 times', '💪', lambda u: u['games_played'] >= 500, 5000),
            'alpha_male': Achievement('alpha_male', 'Alpha Male', 'Win 100 games', '🗿', lambda u: u['games_won'] >= 100, 2000),
            'based': Achievement('based', 'Based', 'Have exactly 1,337 coins', '🧠', lambda u: u['coins'] == 1337, 1337),
            'gigachad': Achievement('gigachad', 'Gigachad', 'Win 1,000 games', '💎', lambda u: u['games_won'] >= 1000, 10000),
            'no_cap': Achievement('no_cap', 'No Cap', 'Win 50,000 coins total', '🧢', lambda u: u['total_won'] >= 50000, 5000),
            'its_giving': Achievement('its_giving', 'Its Giving Broke', 'Have less than 10 coins', '💀', lambda u: u['coins'] < 10, 100),
            'slay': Achievement('slay', 'Slay Queen', 'Keep 10 days streak', '👑', lambda u: u['streak'] >= 10, 1000),
            
            # Number memes
            'stonks': Achievement('stonks', 'Stonks', 'Win 10,000 coins total', '📈', lambda u: u['total_won'] >= 10000, 1000),
            'not_stonks': Achievement('not_stonks', 'Not Stonks', 'Lose 10,000 coins total', '📉', lambda u: u['total_lost'] >= 10000, 1000),
            'over_9000': Achievement('over_9000', 'Its Over 9000!', 'Have more than 9,000 coins', '🐉', lambda u: u['coins'] > 9000, 9001),
            'ordem_66': Achievement('ordem_66', 'Order 66', 'Have exactly 66 coins', '⚔️', lambda u: u['coins'] == 66, 660),
            
            # Gaming achievements
            'respawn': Achievement('respawn', 'Respawn', 'Keep playing after losing coins', '♻️', lambda u: u['games_played'] >= 10 and u['total_lost'] >= 100, 100),
            'gg_ez': Achievement('gg_ez', 'GG EZ', 'Win 100 games', '🎮', lambda u: u['games_won'] >= 100, 1000),
            'noob': Achievement('noob', 'Noob', 'Play 5 times without winning', '🤡', lambda u: u['games_played'] >= 5 and u['games_won'] == 0, 500),
            'hacker': Achievement('hacker', 'Hacker (or lucky)', 'Win 25 games with high streak', '👨‍💻', lambda u: u['games_won'] >= 25 and u['streak'] >= 5, 2500),
            
            # Ironic achievements
            'todo_dia_isso': Achievement('todo_dia_isso', 'Every Day', 'Play for 30 days straight', '😩', lambda u: u['streak'] >= 30, 3000),
            'paciencia': Achievement('paciencia', 'Patience', 'Play 2,000 times', '🧘', lambda u: u['games_played'] >= 2000, 20000),
            'perdemo': Achievement('perdemo', 'We Lost', 'Have 0 coins', '☠️', lambda u: u['coins'] == 0, 1000),
            'confusion': Achievement('confusion', 'Confusion', 'Win and lose 10k coins each', '❓', lambda u: u['total_won'] >= 10000 and u['total_lost'] >= 10000, 2000),
        }
        return achievements
    
    def check_achievements(self, user_id: str, username: str) -> List[Achievement]:
        user = self.db.get_user(user_id, username)
        user_stats = dict(user)
        
        unlocked = []
        
        for achievement in self.achievements.values():
            if achievement.condition(user_stats):
                if self.db.unlock_achievement(user_id, achievement.name):
                    if achievement.reward > 0:
                        self.db.update_coins(user_id, achievement.reward)
                        self.db.add_transaction(
                            user_id, 
                            achievement.reward, 
                            'achievement',
                            f'Achievement unlocked: {achievement.title}'
                        )
                    unlocked.append(achievement)
        
        return unlocked
    
    def get_achievement(self, name: str) -> Achievement:
        return self.achievements.get(name)
    
    def get_all_achievements(self) -> List[Achievement]:
        return list(self.achievements.values())
