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
  // Limpar todos os rate limits
  const deleteRateLimits = db.prepare('DELETE FROM rate_limits');
  const result = deleteRateLimits.run();
  
  console.log('✅ Rate limits limpos com sucesso!');
  console.log(`   ${result.changes} registros removidos`);
  
  // Mostrar rate limits restantes (deve ser 0)
  const countStmt = db.prepare('SELECT COUNT(*) as count FROM rate_limits');
  const count = countStmt.get();
  console.log(`   Rate limits ativos: ${count.count}`);
  
} catch (error) {
  console.error('❌ Erro ao limpar rate limits:', error.message);
} finally {
  db.close();
}
