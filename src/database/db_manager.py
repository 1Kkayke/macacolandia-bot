"""Database manager for SQLite operations"""

import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Tuple


class DatabaseManager:
    """Manages all database operations for the bot"""
    
    def __init__(self, db_path='data/macacolandia.db'):
        """Initialize database manager"""
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                coins INTEGER DEFAULT 1000,
                total_won INTEGER DEFAULT 0,
                total_lost INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                games_won INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_daily TIMESTAMP,
                streak INTEGER DEFAULT 0
            )
        ''')
        
        # Add games_won column if it doesn't exist (for existing databases)
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'games_won' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN games_won INTEGER DEFAULT 0')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                amount INTEGER NOT NULL,
                transaction_type TEXT NOT NULL,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Game history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                game_type TEXT NOT NULL,
                bet_amount INTEGER NOT NULL,
                result TEXT NOT NULL,
                winnings INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Achievements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                achievement_name TEXT NOT NULL,
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                UNIQUE(user_id, achievement_name)
            )
        ''')

        # Guilds table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guilds (
                guild_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                member_count INTEGER DEFAULT 0,
                icon_url TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Guild Members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guild_members (
                guild_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (guild_id, user_id),
                FOREIGN KEY (guild_id) REFERENCES guilds(guild_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        # Guild Coins table - Separate balance per server per user
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guild_coins (
                guild_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                coins INTEGER DEFAULT 1000,
                total_won INTEGER DEFAULT 0,
                total_lost INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                games_won INTEGER DEFAULT 0,
                last_daily TIMESTAMP,
                streak INTEGER DEFAULT 0,
                PRIMARY KEY (guild_id, user_id),
                FOREIGN KEY (guild_id) REFERENCES guilds(guild_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # Guild operations
    def update_guild(self, guild_id: str, name: str, member_count: int, icon_url: str = None):
        """Update or insert guild information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO guilds (guild_id, name, member_count, icon_url, joined_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(guild_id) DO UPDATE SET
                name = excluded.name,
                member_count = excluded.member_count,
                icon_url = excluded.icon_url
        ''', (str(guild_id), name, member_count, icon_url))
        
        conn.commit()
        conn.close()

    def remove_guild(self, guild_id: str):
        """Remove a guild from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM guilds WHERE guild_id = ?', (str(guild_id),))
        cursor.execute('DELETE FROM guild_members WHERE guild_id = ?', (str(guild_id),))
        
        conn.commit()
        conn.close()

    def add_guild_member(self, guild_id: str, user_id: str):
        """Add a member to a guild"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Ensure user exists first
        self.get_user(user_id)
        
        cursor.execute('''
            INSERT OR IGNORE INTO guild_members (guild_id, user_id)
            VALUES (?, ?)
        ''', (str(guild_id), str(user_id)))
        
        conn.commit()
        conn.close()

    def remove_guild_member(self, guild_id: str, user_id: str):
        """Remove a member from a guild"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM guild_members WHERE guild_id = ? AND user_id = ?', 
                      (str(guild_id), str(user_id)))
        
        conn.commit()
        conn.close()

    def get_all_guilds(self) -> List[sqlite3.Row]:
        """Get all guilds"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM guilds ORDER BY member_count DESC')
        
        guilds = cursor.fetchall()
        conn.close()
        return guilds

    # User operations
    def get_user(self, user_id: str, username: str = None, guild_id: str = None) -> sqlite3.Row:
        """Get or create a user (with guild-specific balance if guild_id provided)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            cursor.execute('''
                INSERT INTO users (user_id, username, coins)
                VALUES (?, ?, 0)
            ''', (user_id, username or 'Unknown'))
            conn.commit()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
        
        # If guild_id provided, get guild-specific balance
        if guild_id:
            cursor.execute('''
                SELECT * FROM guild_coins WHERE guild_id = ? AND user_id = ?
            ''', (str(guild_id), user_id))
            guild_coins = cursor.fetchone()
            
            if not guild_coins:
                # Initialize guild-specific balance
                cursor.execute('''
                    INSERT INTO guild_coins (guild_id, user_id, coins)
                    VALUES (?, ?, 1000)
                ''', (str(guild_id), user_id))
                conn.commit()
                cursor.execute('''
                    SELECT * FROM guild_coins WHERE guild_id = ? AND user_id = ?
                ''', (str(guild_id), user_id))
                guild_coins = cursor.fetchone()
            
            # Return guild-specific data merged with user data
            conn.close()
            return guild_coins
        
        conn.close()
        return user
    
    def update_coins(self, user_id: str, amount: int, guild_id: str = None) -> bool:
        """Update user coins (can be negative for deduction) - guild-specific if guild_id provided"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if guild_id:
            # Update guild-specific balance
            cursor.execute('SELECT coins FROM guild_coins WHERE guild_id = ? AND user_id = ?', 
                          (str(guild_id), user_id))
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return False
            
            new_balance = user['coins'] + amount
            if new_balance < 0:
                conn.close()
                return False
            
            cursor.execute('UPDATE guild_coins SET coins = ? WHERE guild_id = ? AND user_id = ?', 
                          (new_balance, str(guild_id), user_id))
        else:
            # Update global balance (for legacy compatibility)
            cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            
            if not user:
                conn.close()
                return False
            
            new_balance = user['coins'] + amount
            if new_balance < 0:
                conn.close()
                return False
            
            cursor.execute('UPDATE users SET coins = ? WHERE user_id = ?', (new_balance, user_id))
        
        conn.commit()
        conn.close()
        return True
    
    def process_bet_atomic(self, user_id: str, bet_amount: int, net_change: int, 
                          game_type: str, won: bool, guild_id: str = None) -> bool:
        """
        Process a bet atomically in a single transaction (guild-specific if guild_id provided)
        This prevents race conditions when multiple users play simultaneously
        
        Args:
            user_id: User identifier
            bet_amount: Amount wagered
            net_change: Net change in balance (negative for loss, positive for win)
            game_type: Type of game played
            won: Whether the user won
            guild_id: Guild ID for server-specific balance
        
        Returns:
            bool: True if successful, False if insufficient balance or error
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check current balance (guild-specific if guild_id provided)
            if guild_id:
                cursor.execute('SELECT coins FROM guild_coins WHERE guild_id = ? AND user_id = ?', 
                              (str(guild_id), user_id))
                user = cursor.fetchone()
                
                if not user:
                    # Initialize if doesn't exist
                    cursor.execute('''
                        INSERT INTO guild_coins (guild_id, user_id, coins)
                        VALUES (?, ?, 1000)
                    ''', (str(guild_id), user_id))
                    conn.commit()
                    cursor.execute('SELECT coins FROM guild_coins WHERE guild_id = ? AND user_id = ?', 
                                  (str(guild_id), user_id))
                    user = cursor.fetchone()
            else:
                cursor.execute('SELECT coins FROM users WHERE user_id = ?', (user_id,))
                user = cursor.fetchone()
            
            if not user:
                conn.close()
                return False
            
            current_balance = user['coins']
            
            # Check if user can afford the bet
            if current_balance < bet_amount:
                conn.close()
                return False
            
            # Calculate new balance (deduct bet, add winnings if won)
            new_balance = current_balance + net_change
            
            # Ensure balance doesn't go negative
            if new_balance < 0:
                conn.close()
                return False
            
            # Update balance (guild-specific or global)
            if guild_id:
                cursor.execute('UPDATE guild_coins SET coins = ? WHERE guild_id = ? AND user_id = ?', 
                              (new_balance, str(guild_id), user_id))
            else:
                cursor.execute('UPDATE users SET coins = ? WHERE user_id = ?', (new_balance, user_id))
            
            # Record transactions
            cursor.execute('''
                INSERT INTO transactions (user_id, amount, transaction_type, description)
                VALUES (?, ?, 'spend', ?)
            ''', (user_id, -bet_amount, f'{game_type} - Aposta'))
            
            if won and net_change > 0:
                winnings = bet_amount + net_change
                cursor.execute('''
                    INSERT INTO transactions (user_id, amount, transaction_type, description)
                    VALUES (?, ?, 'earn', ?)
                ''', (user_id, winnings, f'{game_type} - Vitória'))
            
            # Record game history
            result_str = 'win' if won else 'loss'
            cursor.execute('''
                INSERT INTO game_history (user_id, game_type, bet_amount, result, winnings)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, game_type, bet_amount, result_str, net_change))
            
            # Update user stats (guild-specific or global)
            if guild_id:
                cursor.execute('''
                    UPDATE guild_coins 
                    SET games_played = games_played + 1,
                        games_won = games_won + ?,
                        total_won = total_won + ?,
                        total_lost = total_lost + ?
                    WHERE guild_id = ? AND user_id = ?
                ''', (1 if won else 0, max(0, net_change), max(0, -net_change), str(guild_id), user_id))
            else:
                cursor.execute('''
                    UPDATE users 
                    SET games_played = games_played + 1,
                        games_won = games_won + ?,
                        total_won = total_won + ?,
                        total_lost = total_lost + ?
                    WHERE user_id = ?
                ''', (1 if won else 0, max(0, net_change), max(0, -net_change), user_id))
            
            # Commit all changes atomically
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            # Rollback on any error
            conn.rollback()
            conn.close()
            print(f"Error in process_bet_atomic: {e}")
            return False
    
    def transfer_coins(self, from_user: str, to_user: str, amount: int) -> Tuple[bool, str]:
        """Transfer coins between users"""
        if amount <= 0:
            return False, "Quantidade inválida!"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check sender balance
        cursor.execute('SELECT coins FROM users WHERE user_id = ?', (from_user,))
        sender = cursor.fetchone()
        
        if not sender or sender['coins'] < amount:
            conn.close()
            return False, "Saldo insuficiente!"
        
        # Update both users
        cursor.execute('UPDATE users SET coins = coins - ? WHERE user_id = ?', (amount, from_user))
        cursor.execute('UPDATE users SET coins = coins + ? WHERE user_id = ?', (amount, to_user))
        
        # Log transactions
        cursor.execute('''
            INSERT INTO transactions (user_id, amount, transaction_type, description)
            VALUES (?, ?, 'transfer_out', ?)
        ''', (from_user, -amount, f'Transferência para {to_user}'))
        
        cursor.execute('''
            INSERT INTO transactions (user_id, amount, transaction_type, description)
            VALUES (?, ?, 'transfer_in', ?)
        ''', (to_user, amount, f'Transferência de {from_user}'))
        
        conn.commit()
        conn.close()
        return True, "Transferência realizada com sucesso!"
    
    def add_transaction(self, user_id: str, amount: int, transaction_type: str, description: str = None):
        """Add a transaction record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (user_id, amount, transaction_type, description)
            VALUES (?, ?, ?, ?)
        ''', (user_id, amount, transaction_type, description))
        
        conn.commit()
        conn.close()
    
    def get_transaction_history(self, user_id: str, limit: int = 10) -> List[sqlite3.Row]:
        """Get user transaction history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM transactions
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    
    # Game operations
    def record_game(self, user_id: str, game_type: str, bet_amount: int, 
                   result: str, winnings: int):
        """Record a game result"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Record game history
        cursor.execute('''
            INSERT INTO game_history (user_id, game_type, bet_amount, result, winnings)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, game_type, bet_amount, result, winnings))
        
        # Update user stats
        cursor.execute('''
            UPDATE users 
            SET games_played = games_played + 1,
                total_won = total_won + ?,
                total_lost = total_lost + ?
            WHERE user_id = ?
        ''', (max(0, winnings), max(0, -winnings), user_id))
        
        conn.commit()
        conn.close()
    
    def get_game_history(self, user_id: str, limit: int = 10) -> List[sqlite3.Row]:
        """Get user game history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM game_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        games = cursor.fetchall()
        conn.close()
        return games
    
    def get_leaderboard(self, limit: int = 10) -> List[sqlite3.Row]:
        """Get top users by coins"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, coins, games_played, total_won, total_lost
            FROM users
            ORDER BY coins DESC
            LIMIT ?
        ''', (limit,))
        
        leaders = cursor.fetchall()
        conn.close()
        return leaders
    
    # Achievement operations
    def unlock_achievement(self, user_id: str, achievement_name: str) -> bool:
        """Unlock an achievement for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO achievements (user_id, achievement_name)
                VALUES (?, ?)
            ''', (user_id, achievement_name))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Achievement already unlocked
            conn.close()
            return False
    
    def get_user_achievements(self, user_id: str) -> List[sqlite3.Row]:
        """Get all achievements for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT achievement_name, unlocked_at
            FROM achievements
            WHERE user_id = ?
            ORDER BY unlocked_at DESC
        ''', (user_id,))
        
        achievements = cursor.fetchall()
        conn.close()
        return achievements
    
    # Daily reward operations
    def claim_daily_reward(self, user_id: str) -> Tuple[bool, int, int]:
        """
        Claim daily reward
        Returns: (success, coins_earned, current_streak)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT last_daily, streak, coins FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return False, 0, 0
        
        now = datetime.now()
        last_daily = user['last_daily']
        
        # Check if already claimed today
        if last_daily:
            last_daily_dt = datetime.fromisoformat(last_daily)
            if (now - last_daily_dt).days < 1:
                conn.close()
                return False, 0, user['streak']
        
        # Calculate streak
        streak = user['streak']
        if last_daily:
            last_daily_dt = datetime.fromisoformat(last_daily)
            if (now - last_daily_dt).days == 1:
                streak += 1
            else:
                streak = 1
        else:
            streak = 1
        
        # Calculate reward (base + streak bonus)
        base_reward = 100
        streak_bonus = min(streak * 10, 200)  # Max 200 bonus
        total_reward = base_reward + streak_bonus
        
        # Update user
        cursor.execute('''
            UPDATE users
            SET last_daily = ?,
                streak = ?,
                coins = coins + ?
            WHERE user_id = ?
        ''', (now.isoformat(), streak, total_reward, user_id))
        
        # Log transaction
        cursor.execute('''
            INSERT INTO transactions (user_id, amount, transaction_type, description)
            VALUES (?, ?, 'daily_reward', ?)
        ''', (user_id, total_reward, f'Recompensa diária (streak: {streak})'))
        
        conn.commit()
        conn.close()
        
        return True, total_reward, streak
