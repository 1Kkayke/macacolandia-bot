/**
 * Módulo de segurança centralizado
 * Implementa rate limiting, bloqueio de tentativas, logs e proteções
 */

import { getAuthDatabase } from './auth-db';

// ===== RATE LIMITING =====
interface RateLimitEntry {
  count: number;
  resetTime: number;
}

interface RateLimitStore {
  login: Map<string, RateLimitEntry>;
  register: Map<string, RateLimitEntry>;
}

const rateLimitStore: RateLimitStore = {
  login: new Map(),
  register: new Map(),
};

// Configurações de rate limit
const RATE_LIMITS = {
  login: {
    maxAttempts: 5,
    windowMs: 5 * 60 * 1000, // 5 minutos
  },
  register: {
    maxAttempts: 10,
    windowMs: 60 * 60 * 1000, // 1 hora
  },
};

export interface RateLimitResult {
  allowed: boolean;
  remaining?: number;
  resetTime?: number;
  message?: string;
}

/**
 * Verifica rate limit para um IP específico
 */
export function checkRateLimit(
  ip: string,
  type: 'login' | 'register'
): RateLimitResult {
  const store = rateLimitStore[type];
  const config = RATE_LIMITS[type];
  const now = Date.now();

  const entry = store.get(ip);

  // Se não existe ou expirou, criar nova entrada
  if (!entry || now > entry.resetTime) {
    store.set(ip, {
      count: 1,
      resetTime: now + config.windowMs,
    });
    return {
      allowed: true,
      remaining: config.maxAttempts - 1,
      resetTime: now + config.windowMs,
    };
  }

  // Se atingiu o limite
  if (entry.count >= config.maxAttempts) {
    const minutesRemaining = Math.ceil((entry.resetTime - now) / 60000);
    return {
      allowed: false,
      resetTime: entry.resetTime,
      message: `Muitas tentativas. Tente novamente em ${minutesRemaining} minuto(s).`,
    };
  }

  // Incrementar contador
  entry.count++;
  return {
    allowed: true,
    remaining: config.maxAttempts - entry.count,
    resetTime: entry.resetTime,
  };
}

/**
 * Limpa rate limit para um IP (usado após sucesso)
 */
export function clearRateLimit(ip: string, type: 'login' | 'register'): void {
  rateLimitStore[type].delete(ip);
}

/**
 * Limpeza periódica de entradas expiradas (chamada a cada hora)
 */
export function cleanupExpiredRateLimits(): void {
  const now = Date.now();
  
  for (const [type, store] of Object.entries(rateLimitStore)) {
    for (const [ip, entry] of store.entries()) {
      if (now > entry.resetTime) {
        store.delete(ip);
      }
    }
  }
}

// Executar limpeza a cada hora
setInterval(cleanupExpiredRateLimits, 60 * 60 * 1000);

// ===== BLOQUEIO DE TENTATIVAS FALHAS =====
/**
 * Inicializa tabela de tentativas falhas no banco
 */
export function initFailedAttemptsTable(): void {
  const db = getAuthDatabase();
  
  db.exec(`
    CREATE TABLE IF NOT EXISTS failed_attempts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT NOT NULL,
      ip_address TEXT NOT NULL,
      user_agent TEXT,
      attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      reason TEXT,
      INDEX idx_email (email),
      INDEX idx_ip (ip_address),
      INDEX idx_time (attempt_time)
    )
  `);

  db.exec(`
    CREATE TABLE IF NOT EXISTS account_lockouts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT NOT NULL UNIQUE,
      locked_until TIMESTAMP NOT NULL,
      locked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      reason TEXT,
      INDEX idx_email (email),
      INDEX idx_locked_until (locked_until)
    )
  `);
}

/**
 * Registra uma tentativa de login falha
 */
export function recordFailedAttempt(
  email: string,
  ip: string,
  userAgent: string | null,
  reason: string
): void {
  const db = getAuthDatabase();
  
  db.prepare(`
    INSERT INTO failed_attempts (email, ip_address, user_agent, reason)
    VALUES (?, ?, ?, ?)
  `).run(email, ip, userAgent, reason);
}

/**
 * Verifica se uma conta deve ser bloqueada após tentativas falhas
 */
export function checkAndLockAccount(email: string): {
  shouldLock: boolean;
  attempts: number;
} {
  const db = getAuthDatabase();
  const LOCKOUT_THRESHOLD = 5;
  const TIME_WINDOW = 15 * 60 * 1000; // 15 minutos

  // Contar tentativas recentes
  const result = db.prepare(`
    SELECT COUNT(*) as count
    FROM failed_attempts
    WHERE email = ?
    AND attempt_time > datetime('now', '-15 minutes')
  `).get(email) as { count: number };

  const attempts = result.count;

  if (attempts >= LOCKOUT_THRESHOLD) {
    // Bloquear conta por 15 minutos
    const lockedUntil = new Date(Date.now() + TIME_WINDOW);
    
    db.prepare(`
      INSERT OR REPLACE INTO account_lockouts (email, locked_until, reason)
      VALUES (?, ?, ?)
    `).run(
      email,
      lockedUntil.toISOString(),
      `Bloqueado após ${attempts} tentativas falhas`
    );

    return { shouldLock: true, attempts };
  }

  return { shouldLock: false, attempts };
}

/**
 * Verifica se uma conta está bloqueada
 */
export function isAccountLocked(email: string): {
  locked: boolean;
  lockedUntil?: Date;
  message?: string;
} {
  const db = getAuthDatabase();

  const lockout = db.prepare(`
    SELECT * FROM account_lockouts
    WHERE email = ?
    AND locked_until > datetime('now')
  `).get(email) as { locked_until: string; reason: string } | undefined;

  if (lockout) {
    const lockedUntil = new Date(lockout.locked_until);
    const minutesRemaining = Math.ceil((lockedUntil.getTime() - Date.now()) / 60000);
    
    return {
      locked: true,
      lockedUntil,
      message: `Conta bloqueada. Tente novamente em ${minutesRemaining} minuto(s).`,
    };
  }

  return { locked: false };
}

/**
 * Limpa tentativas falhas após login bem-sucedido
 */
export function clearFailedAttempts(email: string): void {
  const db = getAuthDatabase();
  
  // Remover tentativas falhas
  db.prepare('DELETE FROM failed_attempts WHERE email = ?').run(email);
  
  // Remover bloqueio se existir
  db.prepare('DELETE FROM account_lockouts WHERE email = ?').run(email);
}

/**
 * Limpa bloqueios e tentativas expiradas (manutenção)
 */
export function cleanupExpiredLockouts(): void {
  const db = getAuthDatabase();
  
  // Remover bloqueios expirados
  db.prepare(`
    DELETE FROM account_lockouts
    WHERE locked_until < datetime('now')
  `).run();

  // Remover tentativas antigas (mais de 24 horas)
  db.prepare(`
    DELETE FROM failed_attempts
    WHERE attempt_time < datetime('now', '-24 hours')
  `).run();
}

// Limpeza a cada hora
setInterval(cleanupExpiredLockouts, 60 * 60 * 1000);

// ===== LOGS DE SEGURANÇA =====
export interface SecurityLogEntry {
  event_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  email?: string;
  ip_address: string;
  user_agent?: string | null;
  details: string;
  timestamp: string;
}

/**
 * Inicializa tabela de logs de segurança
 */
export function initSecurityLogsTable(): void {
  const db = getAuthDatabase();
  
  db.exec(`
    CREATE TABLE IF NOT EXISTS security_logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      event_type TEXT NOT NULL,
      severity TEXT NOT NULL CHECK(severity IN ('low', 'medium', 'high', 'critical')),
      email TEXT,
      ip_address TEXT NOT NULL,
      user_agent TEXT,
      details TEXT,
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      INDEX idx_event_type (event_type),
      INDEX idx_severity (severity),
      INDEX idx_email (email),
      INDEX idx_timestamp (timestamp)
    )
  `);
}

/**
 * Registra um evento de segurança
 */
export function logSecurityEvent(entry: Omit<SecurityLogEntry, 'timestamp'>): void {
  const db = getAuthDatabase();
  
  db.prepare(`
    INSERT INTO security_logs (event_type, severity, email, ip_address, user_agent, details)
    VALUES (?, ?, ?, ?, ?, ?)
  `).run(
    entry.event_type,
    entry.severity,
    entry.email || null,
    entry.ip_address,
    entry.user_agent || null,
    entry.details
  );

  // Log crítico também no console
  if (entry.severity === 'critical' || entry.severity === 'high') {
    console.warn(`[SECURITY ${entry.severity.toUpperCase()}]`, {
      type: entry.event_type,
      email: entry.email,
      ip: entry.ip_address,
      details: entry.details,
    });
  }
}

/**
 * Obtém logs de segurança recentes
 */
export function getSecurityLogs(options: {
  limit?: number;
  severity?: SecurityLogEntry['severity'];
  eventType?: string;
  email?: string;
} = {}) {
  const db = getAuthDatabase();
  const { limit = 100, severity, eventType, email } = options;

  let query = 'SELECT * FROM security_logs WHERE 1=1';
  const params: any[] = [];

  if (severity) {
    query += ' AND severity = ?';
    params.push(severity);
  }

  if (eventType) {
    query += ' AND event_type = ?';
    params.push(eventType);
  }

  if (email) {
    query += ' AND email = ?';
    params.push(email);
  }

  query += ' ORDER BY timestamp DESC LIMIT ?';
  params.push(limit);

  return db.prepare(query).all(...params);
}

// ===== RECAPTCHA VERIFICATION =====
/**
 * Verifica token do reCAPTCHA com Google
 */
export async function verifyRecaptcha(token: string, remoteIp?: string): Promise<{
  success: boolean;
  score?: number;
  error?: string;
}> {
  const secretKey = process.env.RECAPTCHA_SECRET_KEY;

  if (!secretKey) {
    console.warn('[SECURITY] RECAPTCHA_SECRET_KEY não configurada');
    // Em desenvolvimento, permitir sem captcha
    if (process.env.NODE_ENV === 'development') {
      return { success: true };
    }
    return { success: false, error: 'Captcha não configurado' };
  }

  try {
    const response = await fetch('https://www.google.com/recaptcha/api/siteverify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        secret: secretKey,
        response: token,
        ...(remoteIp && { remoteip: remoteIp }),
      }),
    });

    const data = await response.json();

    if (!data.success) {
      return {
        success: false,
        error: data['error-codes']?.join(', ') || 'Falha na verificação do captcha',
      };
    }

    return {
      success: true,
      score: data.score,
    };
  } catch (error) {
    console.error('[SECURITY] Erro ao verificar captcha:', error);
    return {
      success: false,
      error: 'Erro ao verificar captcha',
    };
  }
}

// ===== EXTRAÇÃO DE IP DO REQUEST =====
/**
 * Extrai o IP real do cliente considerando proxies e load balancers
 */
export function getClientIp(request: Request): string {
  // Tentar headers de proxy primeiro
  const forwardedFor = request.headers.get('x-forwarded-for');
  if (forwardedFor) {
    return forwardedFor.split(',')[0].trim();
  }

  const realIp = request.headers.get('x-real-ip');
  if (realIp) {
    return realIp;
  }

  const cfConnectingIp = request.headers.get('cf-connecting-ip');
  if (cfConnectingIp) {
    return cfConnectingIp;
  }

  // Fallback
  return 'unknown';
}

/**
 * Extrai User Agent do request
 */
export function getUserAgent(request: Request): string | null {
  return request.headers.get('user-agent');
}

// ===== INICIALIZAÇÃO =====
/**
 * Inicializa todas as tabelas de segurança
 */
export function initSecurityTables(): void {
  try {
    initFailedAttemptsTable();
    initSecurityLogsTable();
    console.log('[SECURITY] Tabelas de segurança inicializadas');
  } catch (error) {
    console.error('[SECURITY] Erro ao inicializar tabelas:', error);
  }
}
