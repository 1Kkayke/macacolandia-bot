const bcrypt = require('bcryptjs');
const Database = require('better-sqlite3');
const path = require('path');

const dbPath = path.join(__dirname, '..', '..', 'data', 'macacolandia.db');

async function ensureAdmin() {
  const adminEmail = 'admin@macacolandia.com';
  const adminPassword = 'Lucas8556!';
  
  console.log('🔧 Garantindo admin em produção...');
  console.log(`📁 Banco de dados: ${dbPath}`);
  
  let db;
  try {
    db = new Database(dbPath);
    
    // Hash da senha
    console.log('🔐 Gerando hash da senha...');
    const hashedPassword = await bcrypt.hash(adminPassword, 12);
    
    // Verificar se admin existe
    const existingAdmin = db.prepare('SELECT * FROM auth_users WHERE email = ?').get(adminEmail);
    
    if (existingAdmin) {
      console.log('👤 Admin encontrado, atualizando...');
      
      // Atualizar senha e desbloquear
      db.prepare(`
        UPDATE auth_users 
        SET password = ?, 
            approved = 1,
            blocked = 0,
            role = 'admin',
            updated_at = datetime('now')
        WHERE email = ?
      `).run(hashedPassword, adminEmail);
      
      console.log('✅ Admin atualizado com sucesso!');
    } else {
      console.log('👤 Admin não encontrado, criando...');
      
      // Criar admin
      db.prepare(`
        INSERT INTO auth_users (name, email, password, role, approved, blocked, created_at, updated_at)
        VALUES (?, ?, ?, 'admin', 1, 0, datetime('now'), datetime('now'))
      `).run('Administrador', adminEmail, hashedPassword);
      
      console.log('✅ Admin criado com sucesso!');
    }
    
    // Limpar tentativas falhadas
    db.prepare('DELETE FROM failed_attempts WHERE email = ?').run(adminEmail);
    console.log('🧹 Tentativas falhadas removidas');
    
    // Limpar bloqueios
    db.prepare('DELETE FROM account_lockouts WHERE email = ?').run(adminEmail);
    console.log('🧹 Bloqueios removidos');
    
    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('✅ ADMIN GARANTIDO COM SUCESSO!');
    console.log('═══════════════════════════════════════════════════════════');
    console.log(`📧 Email:  ${adminEmail}`);
    console.log(`🔑 Senha:  ${adminPassword}`);
    console.log('═══════════════════════════════════════════════════════════\n');
    
  } catch (error) {
    console.error('❌ Erro ao garantir admin:', error);
    process.exit(1);
  } finally {
    if (db) {
      db.close();
    }
  }
}

ensureAdmin();
