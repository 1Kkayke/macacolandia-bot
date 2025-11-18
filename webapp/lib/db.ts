import Database from 'better-sqlite3';
import path from 'path';

const DB_PATH = path.join(process.cwd(), '..', 'data', 'macacolandia.db');

export interface User {
  user_id: string;
  username: string;
  coins: number;
  total_won: number;
  total_lost: number;
  games_played: number;
  games_won: number;
  created_at: string;
  last_daily: string | null;
  streak: number;
}

export interface Transaction {
  id: number;
  user_id: string;
  amount: number;
  transaction_type: string;
  description: string | null;
  timestamp: string;
}

export interface GameHistory {
  id: number;
  user_id: string;
  game_type: string;
  bet_amount: number;
  result: string;
  winnings: number;
  timestamp: string;
}

export interface Achievement {
  id: number;
  user_id: string;
  achievement_name: string;
  unlocked_at: string;
}

export interface ServerConfig {
  guild_id: string;
  guild_name: string;
  user_count: number;
}

let db: Database.Database | null = null;

export function getDatabase() {
  if (!db) {
    try {
      db = new Database(DB_PATH, { readonly: false });
      db.pragma('journal_mode = WAL');
    } catch (error) {
      console.error('Failed to open database:', error);
      throw new Error('Database connection failed');
    }
  }
  return db;
}

// User operations
export function getAllUsers(guildId?: string): User[] {
  const db = getDatabase();
  // For now, return all users. In production, filter by guild_id if available
  const users = db.prepare('SELECT * FROM users ORDER BY coins DESC').all() as User[];
  return users;
}

export function getUser(userId: string): User | undefined {
  const db = getDatabase();
  return db.prepare('SELECT * FROM users WHERE user_id = ?').get(userId) as User | undefined;
}

export function updateUserCoins(userId: string, newCoins: number): boolean {
  const db = getDatabase();
  try {
    const result = db.prepare('UPDATE users SET coins = ? WHERE user_id = ?').run(newCoins, userId);
    return result.changes > 0;
  } catch (error) {
    console.error('Failed to update user coins:', error);
    return false;
  }
}

export function addCoinsToUser(userId: string, amount: number, description?: string): boolean {
  const db = getDatabase();
  try {
    db.transaction(() => {
      const user = db.prepare('SELECT coins FROM users WHERE user_id = ?').get(userId) as { coins: number } | undefined;
      if (!user) return false;
      
      const newCoins = user.coins + amount;
      db.prepare('UPDATE users SET coins = ? WHERE user_id = ?').run(newCoins, userId);
      
      // Add transaction record
      db.prepare(
        'INSERT INTO transactions (user_id, amount, transaction_type, description) VALUES (?, ?, ?, ?)'
      ).run(userId, amount, amount > 0 ? 'admin_add' : 'admin_remove', description || 'Admin adjustment');
    })();
    return true;
  } catch (error) {
    console.error('Failed to add coins:', error);
    return false;
  }
}

// Transaction operations
export function getUserTransactions(userId: string, limit = 50): Transaction[] {
  const db = getDatabase();
  return db
    .prepare('SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?')
    .all(userId, limit) as Transaction[];
}

// Game history operations
export function getUserGameHistory(userId: string, limit = 50): GameHistory[] {
  const db = getDatabase();
  return db
    .prepare('SELECT * FROM game_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?')
    .all(userId, limit) as GameHistory[];
}

export function getGameStats(gameType?: string) {
  const db = getDatabase();
  if (gameType) {
    return db
      .prepare(
        `SELECT 
          COUNT(*) as total_games,
          SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as wins,
          SUM(bet_amount) as total_bet,
          SUM(winnings) as total_winnings
        FROM game_history 
        WHERE game_type = ?`
      )
      .get(gameType);
  }
  return db
    .prepare(
      `SELECT 
        game_type,
        COUNT(*) as total_games,
        SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as wins,
        SUM(bet_amount) as total_bet,
        SUM(winnings) as total_winnings
      FROM game_history 
      GROUP BY game_type`
    )
    .all();
}

// Achievement operations
export function getUserAchievements(userId: string): Achievement[] {
  const db = getDatabase();
  return db
    .prepare('SELECT * FROM achievements WHERE user_id = ? ORDER BY unlocked_at DESC')
    .all(userId) as Achievement[];
}

// Statistics
export function getGlobalStats() {
  const db = getDatabase();
  return {
    totalUsers: db.prepare('SELECT COUNT(*) as count FROM users').get() as { count: number },
    totalCoins: db.prepare('SELECT SUM(coins) as total FROM users').get() as { total: number },
    totalGames: db.prepare('SELECT COUNT(*) as count FROM game_history').get() as { count: number },
    avgCoinsPerUser: db.prepare('SELECT AVG(coins) as avg FROM users').get() as { avg: number },
  };
}

// Simulated server data (since we don't have guild_id in the current schema)
// In production, you would extend the schema to track which users belong to which guild
export function getServers(): ServerConfig[] {
  const db = getDatabase();
  const userCount = db.prepare('SELECT COUNT(*) as count FROM users').get() as { count: number };
  
  // Simulate two servers as mentioned in requirements
  return [
    {
      guild_id: 'server_1',
      guild_name: 'Servidor Principal',
      user_count: Math.floor(userCount.count * 0.6),
    },
    {
      guild_id: 'server_2',
      guild_name: 'Servidor Secundário',
      user_count: Math.floor(userCount.count * 0.4),
    },
  ];
}
