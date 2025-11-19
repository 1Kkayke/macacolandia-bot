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
  id: string;
  name: string;
  member_count: number;
  icon: string | null;
  joined_at: string;
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
  
  if (guildId) {
    // Check if guild_coins has any data for this guild
    const guildCoinsCount = db.prepare('SELECT COUNT(*) as count FROM guild_coins WHERE guild_id = ?').get(guildId) as { count: number };
    
    if (guildCoinsCount.count === 0) {
      // Fallback to global user data for guild members
      return db.prepare(`
        SELECT 
          u.user_id, 
          u.username,
          u.coins,
          u.total_won,
          u.total_lost,
          u.games_played,
          u.games_won,
          u.created_at,
          u.last_daily,
          u.streak
        FROM users u
        INNER JOIN guild_members gm ON u.user_id = gm.user_id
        WHERE gm.guild_id = ?
        ORDER BY u.coins DESC
      `).all(guildId) as User[];
    }
    
    // Return guild-specific user data with guild-specific coins
    return db.prepare(`
      SELECT 
        u.user_id, 
        u.username,
        gc.coins,
        gc.total_won,
        gc.total_lost,
        gc.games_played,
        gc.games_won,
        u.created_at,
        gc.last_daily,
        gc.streak
      FROM users u
      INNER JOIN guild_members gm ON u.user_id = gm.user_id
      INNER JOIN guild_coins gc ON gc.user_id = u.user_id AND gc.guild_id = gm.guild_id
      WHERE gm.guild_id = ?
      ORDER BY gc.coins DESC
    `).all(guildId) as User[];
  }
  
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

export function getGameStats(gameType?: string, guildId?: string) {
  const db = getDatabase();
  
  let query = `
    SELECT 
      ${gameType ? '' : 'gh.game_type,'}
      COUNT(*) as total_games,
      SUM(CASE WHEN gh.result = 'win' THEN 1 ELSE 0 END) as wins,
      SUM(gh.bet_amount) as total_bet,
      SUM(gh.winnings) as total_winnings
    FROM game_history gh
  `;
  
  const params: any[] = [];
  const conditions: string[] = [];
  
  if (guildId) {
    query += ` INNER JOIN guild_members gm ON gh.user_id = gm.user_id `;
    conditions.push('gm.guild_id = ?');
    params.push(guildId);
  }
  
  if (gameType) {
    conditions.push('gh.game_type = ?');
    params.push(gameType);
  }
  
  if (conditions.length > 0) {
    query += ' WHERE ' + conditions.join(' AND ');
  }
  
  if (!gameType) {
    query += ' GROUP BY gh.game_type';
    return db.prepare(query).all(...params);
  }
  
  return db.prepare(query).get(...params);
}

// Achievement operations
export function getUserAchievements(userId: string): Achievement[] {
  const db = getDatabase();
  return db
    .prepare('SELECT * FROM achievements WHERE user_id = ? ORDER BY unlocked_at DESC')
    .all(userId) as Achievement[];
}

// Statistics
export function getGlobalStats(guildId?: string) {
  const db = getDatabase();
  
  if (guildId) {
    // Check if guild_coins has any data for this guild
    const guildCoinsCount = db.prepare('SELECT COUNT(*) as count FROM guild_coins WHERE guild_id = ?').get(guildId) as { count: number };
    
    if (guildCoinsCount.count === 0) {
      // Fallback to global stats for guild members
      const memberIds = db.prepare('SELECT user_id FROM guild_members WHERE guild_id = ?').all(guildId) as { user_id: string }[];
      const memberIdList = memberIds.map(m => m.user_id);
      
      if (memberIdList.length === 0) {
        return {
          totalUsers: { count: 0 },
          totalCoins: { total: 0 },
          totalGames: { count: 0 },
          avgCoinsPerUser: { avg: 0 },
        };
      }
      
      const placeholders = memberIdList.map(() => '?').join(',');
      return {
        totalUsers: { count: memberIdList.length },
        totalCoins: db.prepare(`SELECT COALESCE(SUM(coins), 0) as total FROM users WHERE user_id IN (${placeholders})`).get(...memberIdList) as { total: number },
        totalGames: db.prepare(`SELECT COALESCE(SUM(games_played), 0) as count FROM users WHERE user_id IN (${placeholders})`).get(...memberIdList) as { count: number },
        avgCoinsPerUser: db.prepare(`SELECT COALESCE(AVG(coins), 0) as avg FROM users WHERE user_id IN (${placeholders})`).get(...memberIdList) as { avg: number },
      };
    }
    
    return {
      totalUsers: db.prepare('SELECT COUNT(*) as count FROM guild_members WHERE guild_id = ?').get(guildId) as { count: number },
      totalCoins: db.prepare(`
        SELECT COALESCE(SUM(gc.coins), 0) as total 
        FROM guild_coins gc
        WHERE gc.guild_id = ?
      `).get(guildId) as { total: number },
      totalGames: db.prepare(`
        SELECT COALESCE(SUM(gc.games_played), 0) as count 
        FROM guild_coins gc
        WHERE gc.guild_id = ?
      `).get(guildId) as { count: number },
      avgCoinsPerUser: db.prepare(`
        SELECT COALESCE(AVG(gc.coins), 0) as avg 
        FROM guild_coins gc
        WHERE gc.guild_id = ?
      `).get(guildId) as { avg: number },
    };
  }

  return {
    totalUsers: db.prepare('SELECT COUNT(*) as count FROM users').get() as { count: number },
    totalCoins: db.prepare('SELECT SUM(coins) as total FROM users').get() as { total: number },
    totalGames: db.prepare('SELECT COUNT(*) as count FROM game_history').get() as { count: number },
    avgCoinsPerUser: db.prepare('SELECT AVG(coins) as avg FROM users').get() as { avg: number },
  };
}

// Get real server data from database
export function getServers(): ServerConfig[] {
  const db = getDatabase();
  try {
    // Check if table exists first (migration safety)
    const tableExists = db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='guilds'").get();
    
    if (!tableExists) {
      // Fallback if bot hasn't run yet
      return [];
    }

    const guilds = db.prepare('SELECT guild_id, name, member_count, icon_url, joined_at FROM guilds ORDER BY member_count DESC').all() as any[];
    
    // Map database columns to frontend interface
    return guilds.map(guild => ({
      id: guild.guild_id,
      name: guild.name,
      member_count: guild.member_count,
      icon: guild.icon_url,
      joined_at: guild.joined_at
    }));
  } catch (error) {
    console.error('Error fetching servers:', error);
    return [];
  }
}
