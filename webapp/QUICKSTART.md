# 🚀 GUIA RÁPIDO - Deploy com Segurança

## ✅ Pré-requisitos

- [x] Senha do admin configurada
- [x] Node.js instalado
- [x] Variáveis de ambiente configuradas

## 📝 Passo a Passo

### 1. Configure a Senha do Admin

```bash
cd webapp
node set-admin-password.js "Lucas8556!"
```

**Resultado esperado:**
```
✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!
Comparação bcrypt: ✅ PASSOU
```

### 2. Configure Variáveis de Ambiente

Crie `webapp/.env.local`:

```env
# Obrigatório
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=gere-com-openssl-rand-base64-32

# Opcional (recomendado para produção)
NEXT_PUBLIC_RECAPTCHA_SITE_KEY=sua-chave-google
RECAPTCHA_SECRET_KEY=sua-chave-secreta

# Opcional (notificações por email)
ADMIN_EMAIL=seu-email@gmail.com
EMAIL_USER=seu-email@gmail.com
EMAIL_PASS=senha-de-app-do-gmail
```

**Gerar NEXTAUTH_SECRET:**
```bash
openssl rand -base64 32
```

**Obter chaves do reCAPTCHA:**
https://www.google.com/recaptcha/admin

### 3. Instalar Dependências

```bash
cd webapp
npm install
```

### 4. Rodar em Desenvolvimento

```bash
npm run dev
```

Acesse: http://localhost:3000

### 5. Fazer Login

```
Email: admin@macacolandia.com
Senha: Lucas8556!
```

### 6. Verificar Segurança

```bash
# Ver registros pendentes
node check-registrations.js

# Ver logs de segurança
node view-security-logs.js
```

## 🚀 Deploy para Produção

### 1. Configure Variáveis de Ambiente (Dokploy/Vercel/etc)

```env
NODE_ENV=production
NEXTAUTH_URL=https://seu-dominio.com
NEXTAUTH_SECRET=sua-chave-forte-32-chars
NEXT_PUBLIC_RECAPTCHA_SITE_KEY=sua-chave
RECAPTCHA_SECRET_KEY=sua-chave-secreta
```

### 2. Resete a Senha (use senha mais forte em produção)

```bash
node set-admin-password.js "SuaSenhaForteDeProdução123!"
```

### 3. Build e Deploy

```bash
npm run build
npm run start
```

Ou faça deploy direto no Dokploy/Vercel/Netlify.

## 🛡️ Verificações Pós-Deploy

- [ ] Login funciona com a senha configurada
- [ ] HTTPS ativo (certificado SSL)
- [ ] reCAPTCHA aparece nos formulários
- [ ] Rate limiting funciona (tente 6 logins errados)
- [ ] Logs de segurança sendo gerados
- [ ] Headers de segurança ativos (F12 → Network → Headers)

## 🔧 Troubleshooting

### Senha não funciona

```bash
cd webapp
node set-admin-password.js "NovaSenh@123"
```

### Ver logs de erro

```bash
node view-security-logs.js
```

Procure por eventos `critical` ou `high`.

### Desbloquear conta

Se ficou bloqueado por tentativas falhas:

```javascript
const db = require('better-sqlite3')('data/macacolandia.db');
db.prepare('DELETE FROM account_lockouts WHERE email = ?').run('email@aqui.com');
db.close();
```

### Verificar rate limit

Se está sendo bloqueado injustamente, ajuste em `lib/security.ts`:

```typescript
const RATE_LIMITS = {
  login: {
    maxAttempts: 10, // Era 5
    windowMs: 5 * 60 * 1000,
  },
};
```

## 📚 Documentação Completa

- **Segurança:** `SECURITY.md`
- **Implementação:** `IMPLEMENTATION_SUMMARY.md`
- **Como ver registros:** `COMO_VER_REGISTROS.md`
- **Debug:** `DEBUG_GUIDE.md`

## ✅ Checklist Final

- [ ] Senha do admin configurada e testada
- [ ] `.env.local` ou `.env.production` configurado
- [ ] NEXTAUTH_SECRET gerado (32+ caracteres)
- [ ] reCAPTCHA configurado (se for usar)
- [ ] Webapp rodando sem erros
- [ ] Login funciona
- [ ] Registros pendentes aparecem em `/admin/registrations`
- [ ] HTTPS ativo (em produção)
- [ ] Logs de segurança funcionando

## 🎉 Pronto!

Seu webapp está seguro e pronto para produção com:

✅ 10 camadas de segurança implementadas
✅ Senha do admin funcionando
✅ Rate limiting ativo
✅ Bloqueio de tentativas falhas
✅ Logs de segurança
✅ Proteção SQL Injection
✅ Headers seguros
✅ Sanitização XSS
✅ Bearer Token seguro
✅ Proteção CSRF

**Única pendência:** Componente visual do reCAPTCHA (opcional)

---

**Dúvidas?** Leia `SECURITY.md` para detalhes completos.
