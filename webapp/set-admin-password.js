const Database = require('better-sqlite3');
const bcrypt = require('bcryptjs');
const path = require('path');
const fs = require('fs');

const DB_PATH = path.join(__dirname, '..', 'data', 'macacolandia.db');

// Configurações do admin
const ADMIN_CONFIG = {
  name: 'Admin',
  email: 'admin@macacolandia.com',
  password: process.argv[2] || 'Lucas8556!', // Senha padrão se não fornecida
  role: 'admin'
};

// Garantir que diretório existe
const dataDir = path.dirname(DB_PATH);
if (!fs.existsSync(dataDir)) {
  console.log('📁 Criando diretório de dados:', dataDir);
  fs.mkdirSync(dataDir, { recursive: true });
}

if (!process.argv[2]) {
  console.log('⚠️  AVISO: Usando senha padrão (Lucas8556!)');
  console.log('💡 Para definir outra senha, use: node set-admin-password.js "sua-senha"\n');
}

console.log('🔧 Configurando senha do administrador...\n');
console.log('📁 Banco de dados:', DB_PATH);
console.log('');

try {
  const db = new Database(DB_PATH, { readonly: false });

  // Hash da senha com 12 rounds (mais seguro)
  console.log('🔐 Gerando hash da senha (12 rounds)...');
  const hashedPassword = bcrypt.hashSync(ADMIN_CONFIG.password, 12);
  console.log('✅ Hash gerado com sucesso!');
  console.log('🔍 Hash preview:', hashedPassword.substring(0, 29) + '...\n');

  // Verificar se admin já existe
  const existingAdmin = db.prepare('SELECT * FROM auth_users WHERE email = ?').get(ADMIN_CONFIG.email);

  if (existingAdmin) {
    console.log('👤 Admin encontrado (ID: ' + existingAdmin.id + ')');
    console.log('🔄 Atualizando senha...');
    
    // Atualizar senha e garantir que está aprovado e não bloqueado
    db.prepare(`
      UPDATE auth_users 
      SET password = ?, 
          approved = 1, 
          blocked = 0,
          updated_at = CURRENT_TIMESTAMP 
      WHERE email = ?
    `).run(hashedPassword, ADMIN_CONFIG.email);
    
    console.log('✅ Senha atualizada com sucesso!');
    console.log('✅ Status garantido: approved=1, blocked=0\n');
  } else {
    console.log('➕ Admin não encontrado, criando novo...');
    
    db.prepare(`
      INSERT INTO auth_users (name, email, password, role, approved, blocked)
      VALUES (?, ?, ?, ?, 1, 0)
    `).run(ADMIN_CONFIG.name, ADMIN_CONFIG.email, hashedPassword, ADMIN_CONFIG.role);
    
    console.log('✅ Admin criado com sucesso!\n');
  }

  // Limpar tentativas falhas e bloqueios para este admin
  try {
    db.prepare('DELETE FROM failed_attempts WHERE email = ?').run(ADMIN_CONFIG.email);
    db.prepare('DELETE FROM account_lockouts WHERE email = ?').run(ADMIN_CONFIG.email);
    console.log('🧹 Limpeza: tentativas falhas e bloqueios removidos\n');
  } catch (cleanupError) {
    // Ignorar se tabelas não existirem ainda
    console.log('ℹ️  Nota: tabelas de segurança serão criadas no próximo start\n');
  }

  // TESTE DE VERIFICAÇÃO
  console.log('🧪 TESTE DE VERIFICAÇÃO:');
  console.log('─────────────────────────────────────────────────────────────');
  
  const adminForTest = db.prepare('SELECT * FROM auth_users WHERE email = ?').get(ADMIN_CONFIG.email);
  const testResult = bcrypt.compareSync(ADMIN_CONFIG.password, adminForTest.password);
  
  console.log('Senha fornecida:', ADMIN_CONFIG.password);
  console.log('Hash armazenado:', adminForTest.password.substring(0, 29) + '...');
  console.log('Comparação bcrypt:', testResult ? '✅ PASSOU' : '❌ FALHOU');
  console.log('');

  if (!testResult) {
    console.error('❌ ERRO: A senha não está funcionando!');
    console.error('Isso NÃO deveria acontecer. Verifique o código.\n');
    process.exit(1);
  }

  // Mostrar informações de login
  console.log('═══════════════════════════════════════════════════════════');
  console.log('✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!');
  console.log('═══════════════════════════════════════════════════════════\n');
  console.log('Credenciais de Login:');
  console.log('─────────────────────────────────────────────────────────────');
  console.log('📧 Email:     ', ADMIN_CONFIG.email);
  console.log('🔑 Senha:     ', ADMIN_CONFIG.password);
  console.log('👑 Role:      ', ADMIN_CONFIG.role);
  console.log('✅ Aprovado:   SIM');
  console.log('🔓 Bloqueado:  NÃO');
  console.log('');
  console.log('💡 Faça login em:');
  console.log('   http://localhost:3000/auth/login');
  console.log('');
  console.log('🔐 Configurações de Segurança Ativas:');
  console.log('   • Bcrypt: 12 rounds (muito seguro)');
  console.log('   • Rate limit: 10 tentativas/5min');
  console.log('   • Bloqueio: 5 tentativas falhas = 15min bloqueado');
  console.log('   • Cookies: HttpOnly + Secure (em produção)');
  console.log('');
  
  db.close();
  
} catch (error) {
  console.error('❌ Erro:', error.message);
  console.error('');
  console.error('💡 Dicas:');
  console.error('   - Certifique-se que a pasta "data" existe');
  console.error('   - Rode "npm install" para instalar dependências');
  console.error('   - Execute o webapp primeiro (npm run dev) para criar o banco');
  console.error('');
  process.exit(1);
}
