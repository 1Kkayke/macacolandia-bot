import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';

// Use environment variable or default to ./data relative to project root
const DB_DIR = process.env.DATABASE_DIR || path.join(process.cwd(), 'data');
const DB_PATH = path.join(DB_DIR, 'macacolandia.db');

// Ensure data directory exists
if (!fs.existsSync(DB_DIR)) {
  console.log('[AUTH-DB] Criando diretório de dados:', DB_DIR);
  fs.mkdirSync(DB_DIR, { recursive: true });
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
      initSecurityTables();
      console.log('[AUTH-DB] Tabelas inicializadas com sucesso!');
    } catch (error) {
      console.error('[AUTH-DB] Falha ao abrir banco de dados:', error);
      console.error('[AUTH-DB] Caminho do banco:', DB_PATH);
      throw new Error(`Database connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }
  return db;
}

function initSecurityTables() {
  if (!db) return;
  
  // Failed attempts table
  db.exec(`
    CREATE TABLE IF NOT EXISTS failed_attempts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT NOT NULL,
      ip_address TEXT NOT NULL,
      user_agent TEXT,
      attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      reason TEXT
    )
  `);
  
  db.exec(`CREATE INDEX IF NOT EXISTS idx_failed_email ON failed_attempts(email)`);
  db.exec(`CREATE INDEX IF NOT EXISTS idx_failed_ip ON failed_attempts(ip_address)`);
  db.exec(`CREATE INDEX IF NOT EXISTS idx_failed_time ON failed_attempts(attempt_time)`);

  // Account lockouts table
  db.exec(`
    CREATE TABLE IF NOT EXISTS account_lockouts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT NOT NULL UNIQUE,
      locked_until TIMESTAMP NOT NULL,
      locked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      reason TEXT
    )
  `);
  
  db.exec(`CREATE INDEX IF NOT EXISTS idx_lockout_email ON account_lockouts(email)`);
  db.exec(`CREATE INDEX IF NOT EXISTS idx_lockout_until ON account_lockouts(locked_until)`);

  // Security logs table
  db.exec(`
    CREATE TABLE IF NOT EXISTS security_logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      event_type TEXT NOT NULL,
      severity TEXT NOT NULL CHECK(severity IN ('low', 'medium', 'high', 'critical')),
      email TEXT,
      ip_address TEXT NOT NULL,
      user_agent TEXT,
      details TEXT,
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);
  
  db.exec(`CREATE INDEX IF NOT EXISTS idx_log_event ON security_logs(event_type)`);
  db.exec(`CREATE INDEX IF NOT EXISTS idx_log_severity ON security_logs(severity)`);
  db.exec(`CREATE INDEX IF NOT EXISTS idx_log_email ON security_logs(email)`);
  db.exec(`CREATE INDEX IF NOT EXISTS idx_log_time ON security_logs(timestamp)`);
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

  // Ensure unique index on auth_users.email (defensive, in case schema changed)
  db.exec(`CREATE UNIQUE INDEX IF NOT EXISTS uniq_auth_users_email ON auth_users(email)`);

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

  // Enforce uniqueness at DB level as extra safety
  db.exec(`CREATE UNIQUE INDEX IF NOT EXISTS uniq_pending_registrations_email ON pending_registrations(email)`);

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

  // Security tables
  db.exec(`
    CREATE TABLE IF NOT EXISTS failed_attempts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT NOT NULL,
      ip_address TEXT NOT NULL,
      user_agent TEXT,
      attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      reason TEXT
    )
  `);

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_failed_attempts_email ON failed_attempts(email)
  `);

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_failed_attempts_ip ON failed_attempts(ip_address)
  `);

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_failed_attempts_time ON failed_attempts(attempt_time)
  `);

  db.exec(`
    CREATE TABLE IF NOT EXISTS account_lockouts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT NOT NULL UNIQUE,
      locked_until TIMESTAMP NOT NULL,
      locked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      reason TEXT
    )
  `);

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_lockouts_email ON account_lockouts(email)
  `);

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_lockouts_until ON account_lockouts(locked_until)
  `);

  db.exec(`
    CREATE TABLE IF NOT EXISTS security_logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      event_type TEXT NOT NULL,
      severity TEXT NOT NULL CHECK(severity IN ('low', 'medium', 'high', 'critical')),
      email TEXT,
      ip_address TEXT NOT NULL,
      user_agent TEXT,
      details TEXT,
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_security_logs_type ON security_logs(event_type)
  `);

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_security_logs_severity ON security_logs(severity)
  `);

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_security_logs_email ON security_logs(email)
  `);

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_security_logs_timestamp ON security_logs(timestamp)
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
    // Prevent duplicate pending registrations or existing users with same email
    const existingUser = db.prepare('SELECT id FROM auth_users WHERE email = ?').get(email);
    if (existingUser) {
      throw new Error('EMAIL_EXISTS');
    }

    const existingPending = db.prepare('SELECT id FROM pending_registrations WHERE email = ? AND status = ?').get(email, 'pending');
    if (existingPending) {
      throw new Error('PENDING_EXISTS');
    }
    console.log('[AUTH-DB] Inserindo registro pendente:', { name, email });
    let result;
    try {
      result = db
        .prepare(
          'INSERT INTO pending_registrations (name, email, password, ip_address, user_agent) VALUES (?, ?, ?, ?, ?)'
        )
        .run(name, email, hashedPassword, ipAddress, userAgent);
    } catch (err) {
      // Handle unique constraint errors that may happen in race conditions
      const msg = err instanceof Error ? err.message : String(err);
      if (msg.includes('SQLITE_CONSTRAINT') || msg.includes('constraint')) {
        // Determine whether an auth user exists or a pending exists now
        const nowUser = db.prepare('SELECT id FROM auth_users WHERE email = ?').get(email);
        if (nowUser) throw new Error('EMAIL_EXISTS');
        const nowPending = db.prepare('SELECT id FROM pending_registrations WHERE email = ? AND status = ?').get(email, 'pending');
        if (nowPending) throw new Error('PENDING_EXISTS');
        // fallback
        throw new Error('DB_CONSTRAINT');
      }
      throw err;
    }

    console.log('[AUTH-DB] Registro inserido com ID:', result.lastInsertRowid);
    return result.lastInsertRowid as number;
  } catch (error) {
    console.error('[AUTH-DB] Erro ao criar registro pendente:', error);
    throw error;
  }
}

export function getPendingRegistrationByEmail(email: string) {
  const db = getAuthDatabase();
  return db.prepare('SELECT * FROM pending_registrations WHERE email = ? AND status = ?').get(email, 'pending');
}

export function getPendingRegistrations(): PendingRegistration[] {
  const db = getAuthDatabase();
  return db
    .prepare('SELECT * FROM pending_registrations WHERE status = ? ORDER BY requested_at DESC')
    .all('pending') as PendingRegistration[];
}

export function approvePendingRegistration(id: number): { name: string; email: string } | null {
  const db = getAuthDatabase();
  
  return db.transaction(() => {
    // Get pending registration
    const pending = db
      .prepare('SELECT * FROM pending_registrations WHERE id = ?')
      .get(id) as PendingRegistration | undefined;
    
    if (!pending || pending.status !== 'pending') {
      return null;
    }

    // Create auth user
    try {
      db.prepare(
        'INSERT INTO auth_users (name, email, password, role, approved) VALUES (?, ?, ?, ?, ?)'
      ).run(pending.name, pending.email, pending.password, 'user', 1);
    } catch (err) {
      // Handle unique constraint: another user may have been created concurrently
      const msg = err instanceof Error ? err.message : String(err);
      if (msg.includes('SQLITE_CONSTRAINT') || msg.includes('constraint')) {
        console.warn('[AUTH-DB] Approve failed: email already exists, rejecting pending registration', pending.email);
        // Mark pending as rejected to avoid retry loops
        db.prepare('UPDATE pending_registrations SET status = ? WHERE id = ?').run('rejected', id);
        return null;
      }
      throw err;
    }

    // Update pending status
    db.prepare('UPDATE pending_registrations SET status = ? WHERE id = ?').run('approved', id);

    return { name: pending.name, email: pending.email };
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
