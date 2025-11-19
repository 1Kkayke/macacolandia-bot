const Database = require('better-sqlite3');
const bcrypt = require('bcryptjs');
const path = require('path');

const DB_PATH = path.join(__dirname, '..', 'data', 'macacolandia.db');

// Configurações do admin
const ADMIN_CONFIG = {
  name: 'Admin',
  email: 'admin@macacolandia.com',
  password: process.argv[2] || 'admin123', // Senha via argumento ou padrão
  role: 'admin'
};

if (!process.argv[2]) {
  console.log('⚠️  AVISO: Nenhuma senha fornecida!');
  console.log('💡 Use: node set-admin-password.js "sua-senha-aqui"\n');
  console.log('🔧 Usando senha padrão temporária...\n');
}

console.log('🔧 Configurando senha do administrador...\n');
console.log('📁 Banco de dados:', DB_PATH);
console.log('');

try {
  const db = new Database(DB_PATH, { readonly: false });

  // Hash da senha
  console.log('🔐 Gerando hash da senha...');
  const hashedPassword = bcrypt.hashSync(ADMIN_CONFIG.password, 10);
  console.log('✅ Hash gerado com sucesso!\n');

  // Verificar se admin já existe
  const existingAdmin = db.prepare('SELECT * FROM auth_users WHERE email = ?').get(ADMIN_CONFIG.email);

  if (existingAdmin) {
    console.log('👤 Admin encontrado (ID: ' + existingAdmin.id + ')');
    console.log('🔄 Atualizando senha...');
    
    db.prepare(`
      UPDATE auth_users 
      SET password = ?, updated_at = CURRENT_TIMESTAMP 
      WHERE email = ?
    `).run(hashedPassword, ADMIN_CONFIG.email);
    
    console.log('✅ Senha atualizada com sucesso!\n');
  } else {
    console.log('➕ Admin não encontrado, criando novo...');
    
    db.prepare(`
      INSERT INTO auth_users (name, email, password, role, approved, blocked)
      VALUES (?, ?, ?, ?, 1, 0)
    `).run(ADMIN_CONFIG.name, ADMIN_CONFIG.email, hashedPassword, ADMIN_CONFIG.role);
    
    console.log('✅ Admin criado com sucesso!\n');
  }

  // Mostrar informações de login
  console.log('═══════════════════════════════════════════════════════════');
  console.log('✅ CONFIGURAÇÃO CONCLUÍDA!');
  console.log('═══════════════════════════════════════════════════════════\n');
  console.log('📧 Email: ' + ADMIN_CONFIG.email);
  console.log('👑 Role: ' + ADMIN_CONFIG.role);
  console.log('🔑 Senha: ****** (configurada com sucesso)');
  console.log('');
  console.log('💡 Faça login em:');
  console.log('   http://localhost:3000/auth/login');
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
