const Database = require('better-sqlite3');
const path = require('path');

const DB_PATH = path.join(__dirname, '..', 'data', 'macacolandia.db');

console.log('🔍 Verificando banco de dados...');
console.log('📁 Caminho:', DB_PATH);
console.log('');

try {
  const db = new Database(DB_PATH, { readonly: true });

  console.log('═══════════════════════════════════════════════════════════');
  console.log('📋 SOLICITAÇÕES PENDENTES (Aguardando Aprovação)');
  console.log('═══════════════════════════════════════════════════════════\n');

  const pending = db.prepare(`
    SELECT id, name, email, requested_at, status, ip_address
    FROM pending_registrations 
    WHERE status = 'pending'
    ORDER BY requested_at DESC
  `).all();

  if (pending.length === 0) {
    console.log('✅ Nenhuma solicitação pendente!\n');
  } else {
    pending.forEach((reg, index) => {
      console.log(`┌─ Solicitação #${index + 1} (ID: ${reg.id})`);
      console.log(`│ 👤 Nome: ${reg.name}`);
      console.log(`│ 📧 Email: ${reg.email}`);
      console.log(`│ 🌐 IP: ${reg.ip_address || 'N/A'}`);
      console.log(`│ 📅 Data: ${new Date(reg.requested_at).toLocaleString('pt-BR')}`);
      console.log(`└─────────────────────────────────────────────────────────\n`);
    });
    console.log(`⚠️  Total: ${pending.length} solicitação(ões) aguardando aprovação\n`);
  }

  console.log('═══════════════════════════════════════════════════════════');
  console.log('👥 USUÁRIOS APROVADOS (Podem fazer login)');
  console.log('═══════════════════════════════════════════════════════════\n');

  const users = db.prepare(`
    SELECT id, name, email, role, approved, blocked, created_at 
    FROM auth_users 
    WHERE approved = 1
    ORDER BY created_at DESC
  `).all();

  if (users.length === 0) {
    console.log('❌ Nenhum usuário aprovado ainda!\n');
  } else {
    users.forEach((user, index) => {
      const roleIcon = user.role === 'admin' ? '👑' : '👤';
      const statusIcon = user.blocked ? '🚫' : '✅';
      
      console.log(`┌─ Usuário #${index + 1} (ID: ${user.id})`);
      console.log(`│ ${roleIcon} Nome: ${user.name}`);
      console.log(`│ 📧 Email: ${user.email}`);
      console.log(`│ 🎭 Role: ${user.role}`);
      console.log(`│ ${statusIcon} Status: ${user.blocked ? 'BLOQUEADO' : 'ATIVO'}`);
      console.log(`│ 📅 Criado em: ${new Date(user.created_at).toLocaleString('pt-BR')}`);
      console.log(`└─────────────────────────────────────────────────────────\n`);
    });
    console.log(`✅ Total: ${users.length} usuário(s) ativo(s)\n`);
  }

  console.log('═══════════════════════════════════════════════════════════');
  console.log('📊 ESTATÍSTICAS GERAIS');
  console.log('═══════════════════════════════════════════════════════════\n');

  const stats = {
    totalPending: db.prepare('SELECT COUNT(*) as count FROM pending_registrations WHERE status = "pending"').get(),
    totalApproved: db.prepare('SELECT COUNT(*) as count FROM pending_registrations WHERE status = "approved"').get(),
    totalRejected: db.prepare('SELECT COUNT(*) as count FROM pending_registrations WHERE status = "rejected"').get(),
    totalUsers: db.prepare('SELECT COUNT(*) as count FROM auth_users').get(),
    totalAdmins: db.prepare('SELECT COUNT(*) as count FROM auth_users WHERE role = "admin"').get(),
    totalBlocked: db.prepare('SELECT COUNT(*) as count FROM auth_users WHERE blocked = 1').get(),
  };

  console.log(`📝 Solicitações Pendentes: ${stats.totalPending.count}`);
  console.log(`✅ Solicitações Aprovadas: ${stats.totalApproved.count}`);
  console.log(`❌ Solicitações Rejeitadas: ${stats.totalRejected.count}`);
  console.log(`👥 Total de Usuários: ${stats.totalUsers.count}`);
  console.log(`👑 Administradores: ${stats.totalAdmins.count}`);
  console.log(`🚫 Usuários Bloqueados: ${stats.totalBlocked.count}`);
  console.log('');

  console.log('═══════════════════════════════════════════════════════════');
  console.log('💡 COMO APROVAR SOLICITAÇÕES');
  console.log('═══════════════════════════════════════════════════════════\n');
  
  console.log('1️⃣  Rode o webapp:');
  console.log('   cd webapp');
  console.log('   npm run dev\n');
  
  console.log('2️⃣  Faça login como admin:');
  console.log('   http://localhost:3000/auth/login\n');
  
  console.log('3️⃣  Acesse a página de registros:');
  console.log('   http://localhost:3000/admin/registrations\n');
  
  console.log('4️⃣  Aprove ou rejeite os usuários!\n');

  db.close();
  console.log('✅ Verificação concluída!\n');
  
} catch (error) {
  console.error('❌ Erro ao acessar banco de dados:', error.message);
  console.error('');
  console.error('💡 Dicas:');
  console.error('   - Verifique se a pasta "data" existe');
  console.error('   - Verifique se o arquivo "macacolandia.db" existe');
  console.error('   - Rode o webapp primeiro para criar o banco');
  console.error('');
  process.exit(1);
}
