# 📧 Como Ver as Solicitações de Registro

## ✅ **Resposta Rápida**

Você **NÃO PRECISA** de email configurado! 🎉

**As solicitações aparecem aqui:**
```
http://localhost:3000/admin/registrations
```

---

## 🚀 Como Funciona

### 1️⃣ **Usuário se registra em** `/auth/register`

- Nome, email e senha são salvos no banco de dados
- Status: `pending` (pendente)
- **Você recebe status 200** ✅

### 2️⃣ **Admin aprova em** `/admin/registrations`

- Veja todas as solicitações pendentes
- Informações mostradas:
  - 👤 Nome
  - 📧 Email
  - 🌐 IP do usuário
  - 💻 Navegador usado
  - 📅 Data/hora do pedido
  
### 3️⃣ **Aprovar ou Rejeitar**

- **✅ Aprovar**: Usuário pode fazer login
- **❌ Rejeitar**: Registro é descartado

---

## 🚀 Como Acessar

### **Primeiro: Configurar Senha do Admin**

```powershell
cd webapp
node set-admin-password.js "sua-senha-aqui"
```

Isso vai criar/atualizar o admin com:
- 📧 Email: `admin@macacolandia.com`
- 🔑 Senha: A que você definir no comando

### **Depois: Acessar o Painel**

```powershell
cd webapp
npm run dev
```

Depois acesse:
1. `http://localhost:3000/auth/login` - Faça login como admin
2. `http://localhost:3000/admin/registrations` - Veja solicitações

### **Em Produção (Dokploy):**

```
https://seu-dominio.com/admin/registrations
```

---

## 🎯 Você Não Precisa de Email!

O sistema de email é **OPCIONAL** e só serve para:
- Receber notificação no email quando alguém se registra
- Enviar email de aprovação para o usuário

**Mas tudo funciona sem email:**
- Registros são salvos no banco ✅
- Você vê no painel admin ✅
- Pode aprovar/rejeitar ✅
- Usuários podem fazer login após aprovação ✅

---

## 📊 Verificar Registros Manualmente no Banco

Se quiser ver direto no banco de dados SQLite:

### **Script de Verificação:**

Crie `webapp/check-registrations.js`:

```javascript
const Database = require('better-sqlite3');
const path = require('path');

const DB_PATH = path.join(__dirname, '..', 'data', 'macacolandia.db');
const db = new Database(DB_PATH, { readonly: true });

console.log('📋 SOLICITAÇÕES PENDENTES:\n');

const pending = db.prepare(`
  SELECT id, name, email, requested_at, status 
  FROM pending_registrations 
  WHERE status = 'pending'
  ORDER BY requested_at DESC
`).all();

if (pending.length === 0) {
  console.log('✅ Nenhuma solicitação pendente!\n');
} else {
  pending.forEach(reg => {
    console.log(`ID: ${reg.id}`);
    console.log(`Nome: ${reg.name}`);
    console.log(`Email: ${reg.email}`);
    console.log(`Data: ${new Date(reg.requested_at).toLocaleString('pt-BR')}`);
    console.log('---\n');
  });
}

console.log('\n👥 USUÁRIOS APROVADOS:\n');

const users = db.prepare(`
  SELECT id, name, email, role, created_at 
  FROM auth_users 
  WHERE approved = 1
  ORDER BY created_at DESC
`).all();

if (users.length === 0) {
  console.log('❌ Nenhum usuário aprovado ainda!\n');
} else {
  users.forEach(user => {
    console.log(`ID: ${user.id}`);
    console.log(`Nome: ${user.name}`);
    console.log(`Email: ${user.email}`);
    console.log(`Role: ${user.role}`);
    console.log(`Criado em: ${new Date(user.created_at).toLocaleString('pt-BR')}`);
    console.log('---\n');
  });
}

db.close();
```

**Rodar:**
```powershell
cd webapp
node check-registrations.js
```

---

## 🐛 Se Não Aparecer Nada na Página Admin

### **1. Verificar se o registro foi salvo:**

```powershell
cd webapp
node check-registrations.js
```

### **2. Verificar logs do terminal:**

Quando o usuário se registra, você deve ver:

```
[REGISTER] Nova solicitação de registro: { name: '...', email: '...' }
[REGISTER] Verificando se email já existe...
[REGISTER] Gerando hash da senha...
[REGISTER] Criando registro pendente...
[AUTH-DB] Inserindo registro pendente: { name: '...', email: '...' }
[AUTH-DB] Registro inserido com ID: 1
[REGISTER] Enviando notificação por email...
[REGISTER] Email enviado: false  <-- Normal se email não configurado
[REGISTER] Registro concluído com sucesso!
```

### **3. Status 200 = Sucesso!**

Se você está recebendo **200**, o registro foi salvo com sucesso! ✅

O problema era que você estava procurando no email, mas não precisa!

---

## ✅ Resumo

| ❌ Não Funciona | ✅ Como Funciona |
|-----------------|------------------|
| Procurar no email | Acessar `/admin/registrations` |
| Esperar notificação | Ver diretamente no painel |
| Configurar SMTP | Sistema funciona sem email |

---

## 🎉 Próximos Passos

1. **Rodar o webapp:**
   ```powershell
   cd webapp
   npm run dev
   ```

2. **Fazer login como admin:**
   ```
   http://localhost:3000/auth/login
   ```

3. **Ver solicitações:**
   ```
   http://localhost:3000/admin/registrations
   ```

4. **Aprovar usuários!** 🎯

---

## 💡 Configurar Email (Opcional)

Se quiser receber emails, edite `.env.local`:

```env
ADMIN_EMAIL=seu-email@gmail.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu-email@gmail.com
EMAIL_PASS=senha-de-app-do-gmail
```

**Como gerar senha de app do Gmail:**
1. https://myaccount.google.com/security
2. Ative "Verificação em duas etapas"
3. https://myaccount.google.com/apppasswords
4. Crie uma senha para "Outro"
5. Use essa senha no `EMAIL_PASS`

Mas isso é **completamente opcional**! 🎈
