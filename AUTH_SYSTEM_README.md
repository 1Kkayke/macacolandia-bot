# 🔐 Sistema de Autenticação - Macacolândia Bot Admin

Este documento descreve o sistema de autenticação implementado no painel web do Bot Macacolândia.

## 📋 Visão Geral

Sistema completo de autenticação com aprovação manual de usuários, painel administrativo e notificações por email.

---

## ✨ Funcionalidades

### 🔑 Para Usuários

#### Registro
1. Acesse `/auth/register`
2. Preencha:
   - Nome completo
   - Email
   - Senha (mínimo 6 caracteres)
   - Confirmação de senha
3. Aguarde email de aprovação

#### Login
1. Acesse `/auth/login`
2. Entre com email e senha
3. Acesso ao dashboard principal

### 👑 Para Administradores

#### Gerenciar Solicitações (`/admin/registrations`)
- Ver todas as solicitações pendentes
- Informações incluem:
  - Nome e email do usuário
  - Endereço IP
  - Navegador/User Agent
  - Data e hora da solicitação
- Aprovar ou rejeitar com um clique

#### Gerenciar Usuários (`/admin/users`)
- Listar todos os usuários do sistema
- Ações disponíveis:
  - ✅ Aprovar usuário
  - 🔒 Bloquear acesso
  - 🔓 Desbloquear usuário
  - 👑 Promover para admin
  - 🗑️ Remover do sistema

#### Visualizar Logs (`/admin/logs`)
- Todas as ações administrativas
- Detalhes: usuário, ação, data, IP
- Histórico completo de atividades

---

## 📧 Sistema de Email

### Notificações de Registro

Quando um usuário se registra, um email é enviado automaticamente para o administrador:

**Para**: kayke.contato21@gmail.com (configurável via `.env`)

**Conteúdo**:
- Nome do usuário
- Email
- Endereço IP
- Navegador
- Data e hora
- ID da solicitação
- Botões de ação (Aprovar/Rejeitar)

### Email de Aprovação

Quando um admin aprova um usuário, este recebe um email:

**Para**: Email do usuário

**Conteúdo**:
- Confirmação de aprovação
- Link para login
- Mensagem de boas-vindas

---

## 🛠️ Configuração

### Variáveis de Ambiente

Crie arquivo `.env.local` na pasta `webapp/`:

```env
# NextAuth
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=gere-um-secret-aqui

# Email (Gmail recomendado)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_SECURE=false
EMAIL_USER=seu-email@gmail.com
EMAIL_PASS=sua-senha-de-app

# Admin
ADMIN_EMAIL=kayke.contato21@gmail.com

# Database
DATABASE_PATH=../data/macacolandia.db
```

### Gerar NEXTAUTH_SECRET

**Linux/Mac**:
```bash
openssl rand -base64 32
```

**Windows PowerShell**:
```powershell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

### Configurar Email Gmail

1. Ativar verificação em 2 etapas
2. Ir em: https://myaccount.google.com/apppasswords
3. Criar senha de app
4. Usar essa senha no `EMAIL_PASS`

---

## 🗄️ Estrutura do Banco de Dados

### Tabelas Criadas

#### `auth_users`
Usuários do sistema de autenticação:
```sql
CREATE TABLE auth_users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT DEFAULT 'user',
  approved BOOLEAN DEFAULT 0,
  blocked BOOLEAN DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### `pending_registrations`
Solicitações de registro:
```sql
CREATE TABLE pending_registrations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL,
  ip_address TEXT,
  user_agent TEXT,
  requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status TEXT DEFAULT 'pending'
)
```

#### `activity_logs`
Logs de atividades:
```sql
CREATE TABLE activity_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  action TEXT NOT NULL,
  details TEXT,
  ip_address TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES auth_users(id)
)
```

---

## 🔐 Segurança

### Implementado

✅ **Hashing de Senha**: bcryptjs com 10 rounds
✅ **Sessões JWT**: NextAuth.js com tokens seguros
✅ **Prepared Statements**: Proteção contra SQL injection
✅ **Rate Limiting**: Configurável no proxy
✅ **Email Oculto**: Não aparece no código fonte
✅ **Role-Based Access**: Admin vs User
✅ **Aprovação Manual**: Usuários não podem auto-aprovar
✅ **Activity Logging**: Todas as ações registradas

### Para Produção

⚠️ **HTTPS Obrigatório**: Configure certificado SSL
⚠️ **Firewall**: Bloqueie portas desnecessárias
⚠️ **Backup**: Configure backup automático do banco
⚠️ **Monitoramento**: Configure alertas de falhas
⚠️ **Rate Limiting**: Limite tentativas de login

---

## 📁 Arquitetura

### Estrutura de Arquivos

```
webapp/
├── app/
│   ├── auth/
│   │   ├── login/page.tsx         # Página de login
│   │   ├── register/page.tsx      # Página de registro
│   │   └── error/page.tsx         # Página de erro
│   ├── admin/
│   │   ├── page.tsx               # Dashboard admin
│   │   ├── registrations/page.tsx # Gerenciar solicitações
│   │   ├── users/page.tsx         # Gerenciar usuários
│   │   ├── logs/page.tsx          # Visualizar logs
│   │   └── layout.tsx             # Layout admin
│   └── api/
│       ├── auth/
│       │   ├── [...nextauth]/route.ts  # NextAuth handler
│       │   └── register/route.ts       # API registro
│       └── admin/
│           ├── registrations/route.ts  # API solicitações
│           ├── users/route.ts          # API usuários
│           └── logs/route.ts           # API logs
├── lib/
│   ├── auth.ts           # Configuração NextAuth
│   ├── auth-db.ts        # Operações banco de dados
│   ├── email.ts          # Sistema de email
│   └── auth-guard.tsx    # Proteção de rotas
└── components/
    └── nav-bar.tsx       # Navegação com logout
```

### Fluxo de Autenticação

```
1. Usuário preenche registro
         ↓
2. POST /api/auth/register
         ↓
3. Senha hasheada (bcryptjs)
         ↓
4. Salvo em pending_registrations
         ↓
5. Email enviado ao admin
         ↓
6. Admin aprova em /admin/registrations
         ↓
7. POST /api/admin/registrations
         ↓
8. Usuário criado em auth_users
         ↓
9. Email de aprovação enviado
         ↓
10. Usuário pode fazer login
```

---

## 🎯 Casos de Uso

### Caso 1: Novo Membro da Equipe

```
Cenário: Adicionar novo administrador

1. Novo membro acessa /auth/register
2. Preenche dados e envia
3. Admin recebe email
4. Admin acessa /admin/registrations
5. Aprova a solicitação
6. Admin acessa /admin/users
7. Promove usuário para "admin"
8. Novo admin tem acesso total
```

### Caso 2: Usuário Problemático

```
Cenário: Bloquear acesso de usuário

1. Admin identifica problema
2. Admin acessa /admin/users
3. Encontra usuário na lista
4. Clica em "Bloquear"
5. Usuário não pode mais fazer login
6. Ação registrada em logs
```

### Caso 3: Auditoria de Segurança

```
Cenário: Investigar atividade suspeita

1. Admin acessa /admin/logs
2. Filtra por data/usuário
3. Revisa ações realizadas
4. Identifica padrões
5. Toma ações necessárias
```

---

## 🐛 Troubleshooting

### Problema: Email não está sendo enviado

**Diagnóstico**:
1. Verificar variáveis de ambiente
2. Testar credenciais SMTP
3. Verificar logs do servidor

**Solução**:
```bash
# Verificar logs
docker logs macacolandia-webapp | grep -i email

# Testar SMTP
telnet smtp.gmail.com 587
```

### Problema: Não consigo fazer login

**Possíveis Causas**:
- Conta não aprovada
- Conta bloqueada
- Senha incorreta
- NEXTAUTH_SECRET incorreto

**Solução**:
1. Verificar status em `/admin/users`
2. Verificar variáveis de ambiente
3. Limpar cache do navegador
4. Verificar logs

### Problema: Admin não recebe emails

**Verificações**:
1. `ADMIN_EMAIL` está correto no `.env`?
2. `EMAIL_USER` e `EMAIL_PASS` corretos?
3. Firewall bloqueia porta 587?
4. Logs mostram erro?

---

## 📊 Estatísticas

### Tabela de Endpoints

| Endpoint | Método | Autenticação | Admin Only |
|----------|--------|--------------|------------|
| `/auth/login` | GET/POST | Não | Não |
| `/auth/register` | GET/POST | Não | Não |
| `/api/auth/register` | POST | Não | Não |
| `/api/auth/[...nextauth]` | GET/POST | Não | Não |
| `/admin` | GET | Sim | Sim |
| `/admin/registrations` | GET | Sim | Sim |
| `/admin/users` | GET | Sim | Sim |
| `/admin/logs` | GET | Sim | Sim |
| `/api/admin/registrations` | GET/POST | Sim | Sim |
| `/api/admin/users` | GET/POST | Sim | Sim |
| `/api/admin/logs` | GET | Sim | Sim |

### Funções do Banco de Dados

| Função | Descrição | Retorno |
|--------|-----------|---------|
| `createPendingRegistration()` | Criar solicitação | ID |
| `getPendingRegistrations()` | Listar pendentes | Array |
| `approvePendingRegistration()` | Aprovar e criar usuário | Boolean |
| `rejectPendingRegistration()` | Rejeitar solicitação | Boolean |
| `getUserByEmail()` | Buscar por email | User \| undefined |
| `getUserById()` | Buscar por ID | User \| undefined |
| `getAllAuthUsers()` | Listar todos | Array |
| `updateUserApproval()` | Aprovar/desaprovar | Boolean |
| `updateUserBlocked()` | Bloquear/desbloquear | Boolean |
| `updateUserRole()` | Mudar role | Boolean |
| `deleteAuthUser()` | Remover usuário | Boolean |
| `logActivity()` | Registrar ação | Void |
| `getActivityLogs()` | Buscar logs | Array |

---

## 🎓 Melhores Práticas

### Para Administradores

✅ **Revisar Solicitações**: Analise cuidadosamente cada registro
✅ **Verificar Identidade**: Confirme identidade por outro canal
✅ **Documentar Ações**: Adicione descrições claras
✅ **Revisar Logs**: Monitore atividades regularmente
✅ **Backup Regular**: Mantenha backups do banco
✅ **Senhas Fortes**: Use senhas complexas
✅ **2FA Recomendado**: Ative quando disponível

### Para Desenvolvedores

✅ **Variáveis de Ambiente**: Nunca commitar `.env`
✅ **Secrets Seguros**: Use secrets fortes (32+ caracteres)
✅ **HTTPS**: Sempre em produção
✅ **Validação**: Valide inputs server-side
✅ **Logging**: Registre ações importantes
✅ **Testes**: Teste fluxos críticos
✅ **Documentação**: Mantenha docs atualizados

---

## 📞 Suporte

### Documentação Relacionada

- **DOKPLOY_DEPLOY.md**: Guia completo de deploy
- **WEBAPP_SETUP.md**: Configuração geral do webapp
- **WEBAPP_FEATURES.md**: Todas as funcionalidades
- **README.md**: Documentação principal

### Logs Importantes

```bash
# Ver logs de autenticação
docker logs webapp | grep -i auth

# Ver tentativas de login
docker logs webapp | grep -i "credentials"

# Ver emails enviados
docker logs webapp | grep -i email

# Ver erros
docker logs webapp | grep -i error
```

### Contato

Para suporte técnico ou dúvidas:
- Consulte esta documentação
- Revise os logs do sistema
- Abra uma issue no GitHub

---

## ✅ Checklist de Implementação

Use para garantir que tudo está configurado:

### Configuração Inicial
- [ ] Variáveis de ambiente configuradas
- [ ] NEXTAUTH_SECRET gerado (32+ caracteres)
- [ ] Email Gmail configurado (senha de app)
- [ ] ADMIN_EMAIL configurado
- [ ] Banco de dados acessível

### Primeiro Admin
- [ ] Registrado via /auth/register
- [ ] Aprovado manualmente no banco
- [ ] Role alterado para 'admin'
- [ ] Login funciona
- [ ] Acesso ao /admin

### Funcionalidades
- [ ] Registro de novos usuários funciona
- [ ] Email é enviado ao admin
- [ ] Login funciona após aprovação
- [ ] Painel admin acessível
- [ ] Aprovação de registros funciona
- [ ] Gerenciamento de usuários funciona
- [ ] Logs são registrados

### Segurança
- [ ] HTTPS ativo em produção
- [ ] Firewall configurado
- [ ] Backup automático ativo
- [ ] Senhas fortes em uso
- [ ] Logs de acesso monitorados

---

## 🎉 Conclusão

O sistema de autenticação está completo e pronto para produção. Ele fornece:

- ✅ Registro seguro com aprovação manual
- ✅ Login com sessões JWT
- ✅ Painel administrativo completo
- ✅ Sistema de notificações por email
- ✅ Logging de atividades
- ✅ Proteção de rotas
- ✅ Interface moderna e responsiva

Siga o guia **DOKPLOY_DEPLOY.md** para fazer o deploy no Dokploy!

---

<p align="center">
  <strong>🔐 Sistema de Autenticação Macacolândia Bot</strong><br>
  <em>Seguro, Moderno, Completo</em>
</p>
