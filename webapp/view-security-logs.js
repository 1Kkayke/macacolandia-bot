const Database = require('better-sqlite3');
const path = require('path');

const DB_PATH = path.join(__dirname, '..', 'data', 'macacolandia.db');

console.log('🔍 Analisando Logs de Segurança...\n');
console.log('📁 Banco:', DB_PATH);
console.log('');

try {
  const db = new Database(DB_PATH, { readonly: true });

  // Estatísticas gerais
  console.log('═══════════════════════════════════════════════════════════');
  console.log('📊 ESTATÍSTICAS GERAIS');
  console.log('═══════════════════════════════════════════════════════════\n');

  const stats = {
    total: db.prepare('SELECT COUNT(*) as count FROM security_logs').get(),
    low: db.prepare('SELECT COUNT(*) as count FROM security_logs WHERE severity = "low"').get(),
    medium: db.prepare('SELECT COUNT(*) as count FROM security_logs WHERE severity = "medium"').get(),
    high: db.prepare('SELECT COUNT(*) as count FROM security_logs WHERE severity = "high"').get(),
    critical: db.prepare('SELECT COUNT(*) as count FROM security_logs WHERE severity = "critical"').get(),
  };

  console.log(`Total de eventos: ${stats.total.count}`);
  console.log(`├─ 🟢 Low:      ${stats.low.count}`);
  console.log(`├─ 🟡 Medium:   ${stats.medium.count}`);
  console.log(`├─ 🟠 High:     ${stats.high.count}`);
  console.log(`└─ 🔴 Critical: ${stats.critical.count}`);
  console.log('');

  // Eventos críticos e altos
  console.log('═══════════════════════════════════════════════════════════');
  console.log('🚨 EVENTOS CRÍTICOS E ALTOS (Últimos 20)');
  console.log('═══════════════════════════════════════════════════════════\n');

  const criticalLogs = db.prepare(`
    SELECT * FROM security_logs 
    WHERE severity IN ('high', 'critical')
    ORDER BY timestamp DESC 
    LIMIT 20
  `).all();

  if (criticalLogs.length === 0) {
    console.log('✅ Nenhum evento crítico ou alto registrado!\n');
  } else {
    criticalLogs.forEach((log, index) => {
      const icon = log.severity === 'critical' ? '🔴' : '🟠';
      console.log(`${icon} Evento #${index + 1}`);
      console.log(`├─ Tipo: ${log.event_type}`);
      console.log(`├─ Severidade: ${log.severity.toUpperCase()}`);
      console.log(`├─ Email: ${log.email || 'N/A'}`);
      console.log(`├─ IP: ${log.ip_address}`);
      console.log(`├─ Detalhes: ${log.details}`);
      console.log(`└─ Quando: ${new Date(log.timestamp).toLocaleString('pt-BR')}`);
      console.log('');
    });
  }

  // Tentativas de login falhas
  console.log('═══════════════════════════════════════════════════════════');
  console.log('❌ TENTATIVAS DE LOGIN FALHAS (Últimas 24h)');
  console.log('═══════════════════════════════════════════════════════════\n');

  const failedLogins = db.prepare(`
    SELECT email, COUNT(*) as count 
    FROM security_logs 
    WHERE event_type LIKE '%login_failed%'
    AND timestamp > datetime('now', '-24 hours')
    GROUP BY email 
    ORDER BY count DESC 
    LIMIT 10
  `).all();

  if (failedLogins.length === 0) {
    console.log('✅ Nenhuma tentativa de login falha nas últimas 24 horas!\n');
  } else {
    failedLogins.forEach((item, index) => {
      console.log(`${index + 1}. ${item.email}: ${item.count} tentativas`);
    });
    console.log('');
  }

  // IPs suspeitos
  console.log('═══════════════════════════════════════════════════════════');
  console.log('🌐 TOP 10 IPs COM MAIS EVENTOS (Últimas 24h)');
  console.log('═══════════════════════════════════════════════════════════\n');

  const topIPs = db.prepare(`
    SELECT ip_address, COUNT(*) as count,
           SUM(CASE WHEN severity IN ('high', 'critical') THEN 1 ELSE 0 END) as critical_count
    FROM security_logs 
    WHERE timestamp > datetime('now', '-24 hours')
    GROUP BY ip_address 
    ORDER BY count DESC 
    LIMIT 10
  `).all();

  if (topIPs.length === 0) {
    console.log('ℹ️  Nenhum evento nas últimas 24 horas\n');
  } else {
    topIPs.forEach((item, index) => {
      const warning = item.critical_count > 0 ? '⚠️' : '  ';
      console.log(`${warning} ${index + 1}. ${item.ip_address}`);
      console.log(`   └─ ${item.count} eventos (${item.critical_count} críticos)`);
    });
    console.log('');
  }

  // Contas bloqueadas
  console.log('═══════════════════════════════════════════════════════════');
  console.log('🔒 CONTAS BLOQUEADAS ATUALMENTE');
  console.log('═══════════════════════════════════════════════════════════\n');

  const lockedAccounts = db.prepare(`
    SELECT * FROM account_lockouts 
    WHERE locked_until > datetime('now')
  `).all();

  if (lockedAccounts.length === 0) {
    console.log('✅ Nenhuma conta bloqueada no momento!\n');
  } else {
    lockedAccounts.forEach((lock, index) => {
      const minutesLeft = Math.ceil((new Date(lock.locked_until) - new Date()) / 60000);
      console.log(`${index + 1}. ${lock.email}`);
      console.log(`   ├─ Bloqueado em: ${new Date(lock.locked_at).toLocaleString('pt-BR')}`);
      console.log(`   ├─ Liberado em: ${new Date(lock.locked_until).toLocaleString('pt-BR')}`);
      console.log(`   ├─ Tempo restante: ${minutesLeft} minutos`);
      console.log(`   └─ Motivo: ${lock.reason}`);
      console.log('');
    });
  }

  // Eventos recentes
  console.log('═══════════════════════════════════════════════════════════');
  console.log('📝 ÚLTIMOS 10 EVENTOS');
  console.log('═══════════════════════════════════════════════════════════\n');

  const recentLogs = db.prepare(`
    SELECT * FROM security_logs 
    ORDER BY timestamp DESC 
    LIMIT 10
  `).all();

  if (recentLogs.length === 0) {
    console.log('ℹ️  Nenhum evento registrado ainda\n');
  } else {
    recentLogs.forEach((log, index) => {
      const severityIcon = {
        low: '🟢',
        medium: '🟡',
        high: '🟠',
        critical: '🔴'
      }[log.severity] || '⚪';

      console.log(`${severityIcon} ${index + 1}. ${log.event_type}`);
      console.log(`   ├─ Email: ${log.email || 'N/A'}`);
      console.log(`   ├─ IP: ${log.ip_address}`);
      console.log(`   └─ ${new Date(log.timestamp).toLocaleString('pt-BR')}`);
      console.log('');
    });
  }

  // Recomendações
  console.log('═══════════════════════════════════════════════════════════');
  console.log('💡 RECOMENDAÇÕES');
  console.log('═══════════════════════════════════════════════════════════\n');

  const recommendations = [];

  if (stats.critical.count > 0) {
    recommendations.push('⚠️  Você tem eventos CRÍTICOS! Investigue imediatamente.');
  }

  if (stats.high.count > 5) {
    recommendations.push('⚠️  Muitos eventos HIGH. Revise a segurança.');
  }

  if (lockedAccounts.length > 0) {
    recommendations.push(`🔒 ${lockedAccounts.length} conta(s) bloqueada(s). Verifique se é legítimo.`);
  }

  if (failedLogins.length > 0) {
    const totalFailed = failedLogins.reduce((sum, item) => sum + item.count, 0);
    if (totalFailed > 20) {
      recommendations.push(`❌ ${totalFailed} tentativas de login falhas. Possível ataque de força bruta!`);
    }
  }

  if (recommendations.length === 0) {
    console.log('✅ Tudo parece estar em ordem!');
    console.log('✅ Nenhuma ação recomendada no momento.');
  } else {
    recommendations.forEach(rec => console.log(rec));
  }

  console.log('');
  console.log('═══════════════════════════════════════════════════════════');
  console.log('✅ Análise concluída!');
  console.log('═══════════════════════════════════════════════════════════\n');

  db.close();

} catch (error) {
  console.error('❌ Erro ao acessar banco de dados:', error.message);
  console.error('');
  console.error('💡 Dicas:');
  console.error('   - Execute o webapp primeiro para criar as tabelas');
  console.error('   - Verifique se o caminho do banco está correto');
  console.error('');
  process.exit(1);
}
