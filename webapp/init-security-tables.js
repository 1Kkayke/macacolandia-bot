const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

// Caminho do banco de dados
const dataDir = path.join(__dirname, '..', 'data');
const dbPath = path.join(dataDir, 'macacolandia.db');

if (!fs.existsSync(dbPath)) {
  console.log('❌ Banco de dados não encontrado em:', dbPath);
  process.exit(1);
}

const db = new Database(dbPath);

try {
  console.log('Criando tabelas de segurança...\n');

  // Tabela de rate limiting
  db.exec(`
    CREATE TABLE IF NOT EXISTS rate_limits (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ip TEXT NOT NULL,
      action TEXT NOT NULL,
      timestamp INTEGER NOT NULL,
      UNIQUE(ip, action, timestamp)
    )
  `);
  console.log('✅ Tabela rate_limits criada');

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_rate_limits_ip_action 
    ON rate_limits(ip, action, timestamp)
  `);
  console.log('✅ Índice idx_rate_limits_ip_action criado');

  // Tabela de tentativas de login falhas
  db.exec(`
    CREATE TABLE IF NOT EXISTS failed_attempts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT NOT NULL,
      ip TEXT NOT NULL,
      timestamp INTEGER NOT NULL,
      user_agent TEXT
    )
  `);
  console.log('✅ Tabela failed_attempts criada');

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_failed_attempts_email 
    ON failed_attempts(email, timestamp)
  `);
  console.log('✅ Índice idx_failed_attempts_email criado');

  // Tabela de bloqueios de conta
  db.exec(`
    CREATE TABLE IF NOT EXISTS account_lockouts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT NOT NULL UNIQUE,
      locked_until INTEGER NOT NULL,
      reason TEXT,
      created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
    )
  `);
  console.log('✅ Tabela account_lockouts criada');

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_account_lockouts_email 
    ON account_lockouts(email, locked_until)
  `);
  console.log('✅ Índice idx_account_lockouts_email criado');

  // Tabela de logs de segurança
  db.exec(`
    CREATE TABLE IF NOT EXISTS security_logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
      severity TEXT NOT NULL,
      event_type TEXT NOT NULL,
      ip TEXT,
      user_agent TEXT,
      email TEXT,
      details TEXT,
      metadata TEXT
    )
  `);
  console.log('✅ Tabela security_logs criada');

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_security_logs_timestamp 
    ON security_logs(timestamp DESC)
  `);
  console.log('✅ Índice idx_security_logs_timestamp criado');

  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_security_logs_severity 
    ON security_logs(severity, timestamp DESC)
  `);
  console.log('✅ Índice idx_security_logs_severity criado');

  console.log('\n✅ Todas as tabelas de segurança foram criadas com sucesso!');

  // Mostrar tabelas existentes
  const tables = db.prepare(`
    SELECT name FROM sqlite_master 
    WHERE type='table' AND name NOT LIKE 'sqlite_%'
    ORDER BY name
  `).all();

  console.log('\nTabelas no banco de dados:');
  tables.forEach(table => {
    console.log(`  - ${table.name}`);
  });

} catch (error) {
  console.error('❌ Erro ao criar tabelas:', error.message);
} finally {
  db.close();
}
