# 🔐 Documentação de Segurança - Macacolândia Bot Webapp

## ✅ Medidas de Segurança Implementadas

### 1. **Autenticação Robusta**

#### NextAuth v5 com JWT
- ✅ Sessões baseadas em JWT (stateless)
- ✅ Cookies HttpOnly (não acessíveis via JavaScript)
- ✅ Cookies Secure em produção (apenas HTTPS)
- ✅ SameSite: Lax (proteção CSRF)
- ✅ Expiração: 30 dias

#### Bcrypt para Hashing
- ✅ 12 rounds de hashing (muito seguro)
- ✅ Salt automático
- ✅ Comparação resistente a timing attacks

**Senha Padrão do Admin:**
- Email: `admin@macacolandia.com`
- Senha: `Lucas8556!`
- Para resetar: `node set-admin-password.js "nova-senha"`

---

### 2. **Validações de Entrada**

#### Username (arquivo: `lib/validation.ts`)
- ❌ Sem espaços
- ✅ 3-15 caracteres
- ✅ Apenas letras, números e underscore (`[a-zA-Z0-9_]`)

#### Email (RFC 5322 Completo)
- ✅ Validação regex RFC 5322
- ✅ Máximo 254 caracteres
- ✅ Conversão automática para lowercase
- ✅ Trim automático
- ❌ Rejeita múltiplos `@` (ex: `oi@oi@oi.com`)
- ❌ Rejeita domínios inválidos

#### Senha Forte
- ✅ Mínimo 8 caracteres
- ✅ Pelo menos 1 maiúscula
- ✅ Pelo menos 1 minúscula
- ✅ Pelo menos 1 número
- ❌ Sem espaços

#### Exemplo de Validação:
```typescript
import { validateEmail, validatePassword } from '@/lib/validation';

const emailResult = validateEmail('user@example.com');
if (!emailResult.valid) {
  console.error(emailResult.error);
}

const passwordResult = validatePassword('MyPass123');
if (!passwordResult.valid) {
  console.error(passwordResult.error);
}
```

---

### 3. **Proteção contra SQL Injection**

#### Better-SQLite3 com Prepared Statements
- ✅ Todas as queries usam prepared statements
- ✅ Parâmetros escapados automaticamente
- ✅ Validação extra contra padrões SQL suspeitos

#### Padrões Detectados:
```javascript
- SELECT, INSERT, UPDATE, DELETE, DROP
- -- (comentários SQL)
- ' OR '1'='1 (bypass comum)
- ; (múltiplas queries)
```

**Exemplo de Query Segura:**
```typescript
// ❌ NUNCA faça isso:
db.exec(`SELECT * FROM users WHERE email = '${email}'`);

// ✅ SEMPRE use prepared statements:
db.prepare('SELECT * FROM users WHERE email = ?').get(email);
```

---

### 4. **Rate Limiting**

#### Limites por IP (arquivo: `lib/security.ts`)

| Ação | Limite | Janela | Mensagem após Limite |
|------|--------|--------|----------------------|
| **Login** | 5 tentativas | 5 minutos | "Muitas tentativas. Tente novamente em X minuto(s)." |
| **Registro** | 10 tentativas | 1 hora | "Muitas tentativas. Tente novamente em X minuto(s)." |

#### Funcionalidade:
```typescript
import { checkRateLimit, clearRateLimit } from '@/lib/security';

const rateLimit = checkRateLimit(ipAddress, 'login');
if (!rateLimit.allowed) {
  return res.status(429).json({ error: rateLimit.message });
}

// Após sucesso:
clearRateLimit(ipAddress, 'login');
```

---

### 5. **Bloqueio de Conta Temporário**

#### Sistema de Tentativas Falhas
- ✅ Registra cada tentativa de login falha
- ✅ Bloqueia conta após **5 tentativas falhas**
- ✅ Bloqueio de **15 minutos**
- ✅ Limpa tentativas após login bem-sucedido
- ✅ Limpeza automática de registros antigos (24h)

#### Tabelas do Banco:
- `failed_attempts`: Histórico de tentativas
- `account_lockouts`: Bloqueios ativos

#### Exemplo de Uso:
```typescript
import { isAccountLocked, recordFailedAttempt, clearFailedAttempts } from '@/lib/security';

const lockStatus = isAccountLocked(email);
if (lockStatus.locked) {
  return res.status(403).json({ error: lockStatus.message });
}

// Se senha errada:
recordFailedAttempt(email, ip, userAgent, 'Senha incorreta');

// Se login OK:
clearFailedAttempts(email);
```

---

### 6. **Logs de Segurança**

#### Sistema de Logging Centralizado
- ✅ Todos os eventos de segurança são registrados
- ✅ Severidades: `low`, `medium`, `high`, `critical`
- ✅ Inclui: IP, User Agent, Email, Detalhes
- ✅ Logs críticos também vão para console

#### Eventos Registrados:

| Evento | Severidade | Descrição |
|--------|-----------|-----------|
| `login_success` | low | Login bem-sucedido |
| `login_failed_wrong_password` | medium | Senha incorreta |
| `login_attempt_locked_account` | medium | Tentativa em conta bloqueada |
| `login_attempt_unapproved` | low | Conta não aprovada |
| `register_success` | low | Registro criado |
| `register_invalid_email` | low | Email inválido |
| `register_duplicate_email` | low | Email já existe |
| `register_sql_injection_attempt` | **critical** | Tentativa de SQL injection |
| `register_rate_limit_exceeded` | medium | Rate limit excedido |

#### Consultar Logs:
```typescript
import { getSecurityLogs } from '@/lib/security';

// Últimos 100 logs
const logs = getSecurityLogs({ limit: 100 });

// Apenas eventos críticos
const critical = getSecurityLogs({ severity: 'critical' });

// Por email específico
const userLogs = getSecurityLogs({ email: 'user@example.com' });
```

---

### 7. **reCAPTCHA v2**

#### Configuração
- ✅ Obrigatório em produção
- ✅ Opcional em desenvolvimento
- ✅ Validação server-side (Google API)
- ✅ Score tracking (se usar v3)

#### Variáveis de Ambiente:
```env
RECAPTCHA_SITE_KEY=sua-chave-publica
RECAPTCHA_SECRET_KEY=sua-chave-secreta
```

#### Como Obter Chaves:
1. Acesse: https://www.google.com/recaptcha/admin
2. Registre um novo site
3. Escolha reCAPTCHA v2 (checkbox)
4. Adicione domínios: `localhost`, `seu-dominio.com`
5. Copie as chaves para `.env.local`

#### Implementação no Frontend:
```tsx
import ReCAPTCHA from 'react-google-recaptcha';

<ReCAPTCHA
  sitekey={process.env.NEXT_PUBLIC_RECAPTCHA_SITE_KEY!}
  onChange={(token) => setRecaptchaToken(token)}
/>
```

#### Validação no Backend:
```typescript
import { verifyRecaptcha } from '@/lib/security';

const captchaResult = await verifyRecaptcha(token, ip);
if (!captchaResult.success) {
  return res.status(400).json({ error: 'Captcha inválido' });
}
```

---

### 8. **Headers de Segurança**

#### Implementado via Next.js Config
Arquivo: `next.config.js`

```javascript
module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY', // Previne clickjacking
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff', // Previne MIME sniffing
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block', // XSS protection
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.google.com https://www.gstatic.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://www.google.com;",
          },
        ],
      },
    ];
  },
};
```

---

### 9. **Proteção CSRF**

#### NextAuth CSRF Token
- ✅ Token CSRF automático em todos os forms
- ✅ Validado em cada requisição POST
- ✅ Renovado a cada sessão

---

### 10. **Sanitização de Entrada**

#### XSS Protection
```typescript
import { sanitizeInput } from '@/lib/validation';

const cleanInput = sanitizeInput(userInput);
// Remove: <, >, javascript:, on*= (event handlers)
```

---

## 📊 Estrutura do Banco de Dados

### Tabelas de Segurança:

#### `failed_attempts`
```sql
CREATE TABLE failed_attempts (
  id INTEGER PRIMARY KEY,
  email TEXT NOT NULL,
  ip_address TEXT NOT NULL,
  user_agent TEXT,
  attempt_time TIMESTAMP,
  reason TEXT
);
```

#### `account_lockouts`
```sql
CREATE TABLE account_lockouts (
  id INTEGER PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  locked_until TIMESTAMP NOT NULL,
  locked_at TIMESTAMP,
  reason TEXT
);
```

#### `security_logs`
```sql
CREATE TABLE security_logs (
  id INTEGER PRIMARY KEY,
  event_type TEXT NOT NULL,
  severity TEXT NOT NULL,
  email TEXT,
  ip_address TEXT NOT NULL,
  user_agent TEXT,
  details TEXT,
  timestamp TIMESTAMP
);
```

---

## 🚀 Configuração para Produção

### 1. Variáveis de Ambiente (`.env.production`)

```env
# NextAuth
NEXTAUTH_URL=https://seu-dominio.com
NEXTAUTH_SECRET=gere-uma-chave-forte-aqui

# reCAPTCHA
RECAPTCHA_SITE_KEY=sua-chave-publica
RECAPTCHA_SECRET_KEY=sua-chave-secreta

# Email (Opcional)
ADMIN_EMAIL=admin@seu-dominio.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu-email@gmail.com
EMAIL_PASS=senha-de-app

# Node
NODE_ENV=production
```

### 2. Gerar NEXTAUTH_SECRET

```bash
openssl rand -base64 32
```

Ou use: https://generate-secret.vercel.app/32

### 3. Resetar Senha do Admin

```bash
cd webapp
node set-admin-password.js "SuaSenhaForte123!"
```

### 4. Verificar Logs de Segurança

Crie `webapp/view-security-logs.js`:

```javascript
const Database = require('better-sqlite3');
const path = require('path');

const DB_PATH = path.join(__dirname, '..', 'data', 'macacolandia.db');
const db = new Database(DB_PATH, { readonly: true });

const logs = db.prepare(`
  SELECT * FROM security_logs 
  WHERE severity IN ('high', 'critical')
  ORDER BY timestamp DESC 
  LIMIT 50
`).all();

console.log('🚨 LOGS CRÍTICOS/ALTOS:\n');
logs.forEach(log => {
  console.log(`[${log.severity.toUpperCase()}] ${log.event_type}`);
  console.log(`Email: ${log.email || 'N/A'}`);
  console.log(`IP: ${log.ip_address}`);
  console.log(`Detalhes: ${log.details}`);
  console.log(`Quando: ${new Date(log.timestamp).toLocaleString('pt-BR')}`);
  console.log('---\n');
});

db.close();
```

---

## 🛡️ Checklist de Segurança

### Antes do Deploy:
- [ ] `NEXTAUTH_SECRET` configurado e forte (32+ chars)
- [ ] `NEXTAUTH_URL` aponta para domínio de produção
- [ ] reCAPTCHA configurado com chaves de produção
- [ ] Senha do admin resetada (não use padrão em produção!)
- [ ] `NODE_ENV=production`
- [ ] HTTPS ativo (certificado SSL válido)
- [ ] Headers de segurança configurados
- [ ] Logs de segurança sendo monitorados

### Após Deploy:
- [ ] Testar login com senha correta
- [ ] Testar bloqueio após 5 tentativas falhas
- [ ] Testar rate limiting (muitas tentativas)
- [ ] Verificar captcha funcionando
- [ ] Verificar logs de segurança
- [ ] Testar registro de novo usuário
- [ ] Verificar emails sendo enviados (se configurado)

---

## 🔍 Monitoramento

### Scripts Úteis:

#### Verificar Tentativas Falhas:
```javascript
db.prepare(`
  SELECT email, COUNT(*) as count 
  FROM failed_attempts 
  WHERE attempt_time > datetime('now', '-1 hour')
  GROUP BY email 
  ORDER BY count DESC
`).all();
```

#### Verificar Contas Bloqueadas:
```javascript
db.prepare(`
  SELECT * FROM account_lockouts 
  WHERE locked_until > datetime('now')
`).all();
```

#### Top IPs com Mais Tentativas:
```javascript
db.prepare(`
  SELECT ip_address, COUNT(*) as count 
  FROM security_logs 
  WHERE event_type LIKE '%failed%'
  AND timestamp > datetime('now', '-24 hours')
  GROUP BY ip_address 
  ORDER BY count DESC 
  LIMIT 10
`).all();
```

---

## 🆘 Troubleshooting

### Problema: Senha não funciona após deploy

**Solução:**
```bash
cd webapp
node set-admin-password.js "Lucas8556!"
```

Verifique que o teste de hash passa (✅ PASSOU).

### Problema: reCAPTCHA não valida

**Causas Comuns:**
1. `RECAPTCHA_SECRET_KEY` não configurada
2. Domínio não autorizado no Google reCAPTCHA
3. Token expirado (válido por 2 minutos)

**Solução:**
- Em desenvolvimento, captcha é opcional
- Em produção, configure as variáveis de ambiente
- Adicione `localhost` e seu domínio na lista de domínios autorizados

### Problema: Rate limit bloqueando muito rápido

**Ajustar limites em** `lib/security.ts`:
```typescript
const RATE_LIMITS = {
  login: {
    maxAttempts: 10, // Era 5
    windowMs: 5 * 60 * 1000,
  },
};
```

### Problema: Conta bloqueada permanentemente

**Desbloquear manualmente:**
```javascript
const db = require('better-sqlite3')('data/macacolandia.db');
db.prepare('DELETE FROM account_lockouts WHERE email = ?').run('email@example.com');
db.prepare('DELETE FROM failed_attempts WHERE email = ?').run('email@example.com');
db.close();
```

---

## 📚 Referências

- [NextAuth.js Documentation](https://next-auth.js.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [RFC 5322 (Email Format)](https://datatracker.ietf.org/doc/html/rfc5322)
- [Google reCAPTCHA](https://www.google.com/recaptcha)
- [bcrypt Security](https://github.com/kelektiv/node.bcrypt.js#security-issues-and-concerns)

---

## ✅ Resumo

Este webapp implementa **10 camadas de segurança**:

1. ✅ Autenticação robusta (NextAuth + bcrypt 12 rounds)
2. ✅ Validações completas (RFC 5322, senha forte)
3. ✅ Proteção SQL Injection (prepared statements)
4. ✅ Rate limiting (5 login/5min, 10 registro/1h)
5. ✅ Bloqueio temporário (5 tentativas = 15min)
6. ✅ Logs de segurança (4 níveis de severidade)
7. ✅ reCAPTCHA (anti-bot)
8. ✅ Headers seguros (XSS, CSRF, Clickjacking)
9. ✅ Sanitização XSS (entrada limpa)
10. ✅ Cookies seguros (HttpOnly, Secure, SameSite)

**Status:** ✅ Pronto para produção!
