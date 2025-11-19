import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';

const DB_PATH = path.join(process.cwd(), '..', 'data', 'macacolandia.db');

// Ensure data directory exists
const dataDir = path.dirname(DB_PATH);
if (!fs.existsSync(dataDir)) {
  console.log('[AUTH-DB] Criando diretório de dados:', dataDir);
  fs.mkdirSync(dataDir, { recursive: true });
}

export interface AuthUser {
  id: number;
  name: string;
  email: string;
  password: string;
  role: 'admin' | 'user';
  approved: boolean;
  blocked: boolean;
  created_at: string;
  updated_at: string;
}

export interface PendingRegistration {
  id: number;
  name: string;
  email: string;
  password: string;
  ip_address: string | null;
  user_agent: string | null;
  requested_at: string;
  status: 'pending' | 'approved' | 'rejected';
}

let db: Database.Database | null = null;

export function getAuthDatabase() {
  if (!db) {
    try {
      console.log('[AUTH-DB] Tentando conectar ao banco:', DB_PATH);
      db = new Database(DB_PATH, { readonly: false });
      db.pragma('journal_mode = WAL');
      console.log('[AUTH-DB] Banco conectado, inicializando tabelas...');
      initAuthTables();
      console.log('[AUTH-DB] Tabelas inicializadas com sucesso!');
    } catch (error) {
      console.error('[AUTH-DB] Falha ao abrir banco de dados:', error);
      console.error('[AUTH-DB] Caminho do banco:', DB_PATH);
      throw new Error(`Database connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }
  return db;
}

function initAuthTables() {
  const db = getAuthDatabase();
  
  // Auth users table
  db.exec(`
    CREATE TABLE IF NOT EXISTS auth_users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL,
      role TEXT DEFAULT 'user' CHECK(role IN ('admin', 'user')),
      approved BOOLEAN DEFAULT 0,
      blocked BOOLEAN DEFAULT 0,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Pending registrations table
  db.exec(`
    CREATE TABLE IF NOT EXISTS pending_registrations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT NOT NULL,
      password TEXT NOT NULL,
      ip_address TEXT,
      user_agent TEXT,
      requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected'))
    )
  `);

  // Activity logs table
  db.exec(`
    CREATE TABLE IF NOT EXISTS activity_logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      action TEXT NOT NULL,
      details TEXT,
      ip_address TEXT,
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES auth_users(id)
    )
  `);
}

// User operations
export function createPendingRegistration(
  name: string,
  email: string,
  hashedPassword: string,
  ipAddress: string | null,
  userAgent: string | null
): number {
  try {
    const db = getAuthDatabase();
    console.log('[AUTH-DB] Inserindo registro pendente:', { name, email });
    const result = db
      .prepare(
        'INSERT INTO pending_registrations (name, email, password, ip_address, user_agent) VALUES (?, ?, ?, ?, ?)'
      )
      .run(name, email, hashedPassword, ipAddress, userAgent);
    console.log('[AUTH-DB] Registro inserido com ID:', result.lastInsertRowid);
    return result.lastInsertRowid as number;
  } catch (error) {
    console.error('[AUTH-DB] Erro ao criar registro pendente:', error);
    throw error;
  }
}

export function getPendingRegistrations(): PendingRegistration[] {
  const db = getAuthDatabase();
  return db
    .prepare('SELECT * FROM pending_registrations WHERE status = ? ORDER BY requested_at DESC')
    .all('pending') as PendingRegistration[];
}

export function approvePendingRegistration(id: number): boolean {
  const db = getAuthDatabase();
  
  return db.transaction(() => {
    // Get pending registration
    const pending = db
      .prepare('SELECT * FROM pending_registrations WHERE id = ?')
      .get(id) as PendingRegistration | undefined;
    
    if (!pending || pending.status !== 'pending') {
      return false;
    }

    // Create auth user
    db.prepare(
      'INSERT INTO auth_users (name, email, password, role, approved) VALUES (?, ?, ?, ?, ?)'
    ).run(pending.name, pending.email, pending.password, 'user', 1);

    // Update pending status
    db.prepare('UPDATE pending_registrations SET status = ? WHERE id = ?').run('approved', id);

    return true;
  })();
}

export function rejectPendingRegistration(id: number): boolean {
  const db = getAuthDatabase();
  const result = db
    .prepare('UPDATE pending_registrations SET status = ? WHERE id = ?')
    .run('rejected', id);
  return result.changes > 0;
}

export function getUserByEmail(email: string): AuthUser | undefined {
  const db = getAuthDatabase();
  return db.prepare('SELECT * FROM auth_users WHERE email = ?').get(email) as AuthUser | undefined;
}

export function getUserById(id: number): AuthUser | undefined {
  const db = getAuthDatabase();
  return db.prepare('SELECT * FROM auth_users WHERE id = ?').get(id) as AuthUser | undefined;
}

export function getAllAuthUsers(): AuthUser[] {
  const db = getAuthDatabase();
  return db.prepare('SELECT * FROM auth_users ORDER BY created_at DESC').all() as AuthUser[];
}

export function updateUserApproval(userId: number, approved: boolean): boolean {
  const db = getAuthDatabase();
  const result = db
    .prepare('UPDATE auth_users SET approved = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?')
    .run(approved ? 1 : 0, userId);
  return result.changes > 0;
}

export function updateUserBlocked(userId: number, blocked: boolean): boolean {
  const db = getAuthDatabase();
  const result = db
    .prepare('UPDATE auth_users SET blocked = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?')
    .run(blocked ? 1 : 0, userId);
  return result.changes > 0;
}

export function updateUserRole(userId: number, role: 'admin' | 'user'): boolean {
  const db = getAuthDatabase();
  const result = db
    .prepare('UPDATE auth_users SET role = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?')
    .run(role, userId);
  return result.changes > 0;
}

export function deleteAuthUser(userId: number): boolean {
  const db = getAuthDatabase();
  const result = db.prepare('DELETE FROM auth_users WHERE id = ?').run(userId);
  return result.changes > 0;
}

export function logActivity(
  userId: number | null,
  action: string,
  details: string | null,
  ipAddress: string | null
): void {
  const db = getAuthDatabase();
  db.prepare(
    'INSERT INTO activity_logs (user_id, action, details, ip_address) VALUES (?, ?, ?, ?)'
  ).run(userId, action, details, ipAddress);
}

export function getActivityLogs(limit = 100) {
  const db = getAuthDatabase();
  return db
    .prepare(
      `SELECT al.*, au.name as user_name, au.email as user_email 
       FROM activity_logs al 
       LEFT JOIN auth_users au ON al.user_id = au.id 
       ORDER BY al.timestamp DESC 
       LIMIT ?`
    )
    .all(limit);
}
