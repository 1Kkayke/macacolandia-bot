# ✅ CHECKLIST DE PRODUÇÃO - Macacolândia Bot Webapp

Use este checklist antes de fazer deploy em produção.

## 🔐 Segurança Básica

- [ ] **NEXTAUTH_SECRET** configurado (32+ caracteres, gerado com `openssl rand -base64 32`)
- [ ] **NEXTAUTH_URL** aponta para domínio de produção (https://seu-dominio.com)
- [ ] **NODE_ENV=production** configurado
- [ ] Senha do admin **NÃO é a padrão** (mudou de "Lucas8556!")
- [ ] Senha do admin é **forte** (12+ caracteres, maiúsculas, minúsculas, números, símbolos)
- [ ] Arquivo `.env.local` **NÃO está** no repositório Git

## 🤖 reCAPTCHA (Recomendado)

- [ ] Chaves do Google reCAPTCHA obtidas em https://www.google.com/recaptcha/admin
- [ ] `NEXT_PUBLIC_RECAPTCHA_SITE_KEY` configurada
- [ ] `RECAPTCHA_SECRET_KEY` configurada
- [ ] Domínio de produção adicionado na lista de domínios autorizados
- [ ] Testado que captcha aparece nos formulários

## 🌐 HTTPS e Domínio

- [ ] Certificado SSL válido instalado
- [ ] HTTPS funciona sem erros/avisos
- [ ] Redirecionamento HTTP → HTTPS configurado
- [ ] Domínio apontando corretamente para o servidor
- [ ] Headers HSTS configurados (se aplicável)

## 📧 Email (Opcional mas Recomendado)

- [ ] `ADMIN_EMAIL` configurado (para receber notificações)
- [ ] `EMAIL_USER` e `EMAIL_PASS` configurados
- [ ] Se Gmail, usa "Senha de App" (https://myaccount.google.com/apppasswords)
- [ ] Email de teste enviado com sucesso
- [ ] Emails de notificação chegando na caixa de entrada (não spam)

## 🗄️ Banco de Dados

- [ ] Pasta `data/` existe com permissões corretas
- [ ] Arquivo `macacolandia.db` criado
- [ ] Backup do banco de dados configurado (automático ou manual)
- [ ] Tabelas de segurança inicializadas (`security_logs`, `failed_attempts`, `account_lockouts`)
- [ ] Admin criado e testado (login funciona)

## 🧪 Testes Funcionais

### Autenticação
- [ ] Login com credenciais corretas funciona
- [ ] Login com senha errada é rejeitado
- [ ] 5 tentativas falhas bloqueiam por 15 minutos
- [ ] Após bloqueio, mensagem clara é exibida
- [ ] Login bem-sucedido remove bloqueio
- [ ] Sessão persiste após refresh da página
- [ ] Logout funciona corretamente

### Registro
- [ ] Formulário de registro aceita dados válidos
- [ ] Email inválido é rejeitado (ex: "oi@oi@oi.com")
- [ ] Username com espaços é rejeitado
- [ ] Username com mais de 15 caracteres é rejeitado
- [ ] Senha fraca é rejeitada (sem maiúscula/número)
- [ ] reCAPTCHA (se configurado) bloqueia sem token
- [ ] Registro duplicado é rejeitado
- [ ] Admin recebe notificação de novo registro

### Admin Panel
- [ ] `/admin/registrations` exibe registros pendentes
- [ ] Aprovar registro funciona
- [ ] Rejeitar registro funciona
- [ ] Usuário aprovado consegue fazer login
- [ ] Usuário rejeitado não consegue fazer login

### Rate Limiting
- [ ] 10 registros rápidos/1h são bloqueados
- [ ] 5 logins errados/5min são bloqueados
- [ ] Mensagem amigável é exibida ao atingir limite
- [ ] Limite reseta após o tempo especificado

## 🛡️ Testes de Segurança

### SQL Injection
- [ ] Input com `' OR '1'='1` é rejeitado
- [ ] Input com `SELECT * FROM` é rejeitado
- [ ] Input com `--` (comentário SQL) é rejeitado

### XSS
- [ ] Input com `<script>alert('xss')</script>` é sanitizado
- [ ] Input com `javascript:` é removido
- [ ] Input com `onerror=` é removido

### Headers HTTP
- [ ] `X-Frame-Options: DENY` presente (F12 → Network → Headers)
- [ ] `X-Content-Type-Options: nosniff` presente
- [ ] `X-XSS-Protection: 1; mode=block` presente
- [ ] `Referrer-Policy` configurado
- [ ] `Content-Security-Policy` presente (se aplicável)

### Cookies
- [ ] Cookie de sessão tem flag `HttpOnly`
- [ ] Cookie de sessão tem flag `Secure` (em produção)
- [ ] Cookie de sessão tem `SameSite=Lax`

## 📊 Monitoramento

- [ ] Script `view-security-logs.js` funciona
- [ ] Logs de segurança sendo gerados
- [ ] Eventos críticos são visíveis
- [ ] IPs suspeitos são identificáveis
- [ ] Plano de monitoramento definido (ex: verificar logs 1x/dia)

## 🔧 Performance

- [ ] Build de produção (`npm run build`) sem erros
- [ ] Tamanho do bundle está otimizado
- [ ] Imagens otimizadas (se houver)
- [ ] Lazy loading configurado (se aplicável)
- [ ] Cache do navegador configurado

## 📱 Compatibilidade

- [ ] Testado no Chrome/Edge
- [ ] Testado no Firefox
- [ ] Testado no Safari (se possível)
- [ ] Testado em mobile (Chrome Mobile)
- [ ] Layout responsivo funciona

## 🚨 Contingência

- [ ] Plano de rollback definido
- [ ] Backup do banco antes do deploy
- [ ] Logs de deploy salvos
- [ ] Senha de admin anotada em lugar seguro
- [ ] Contato técnico disponível em caso de problema

## 📝 Documentação

- [ ] README atualizado com instruções de deploy
- [ ] Variáveis de ambiente documentadas
- [ ] Procedimentos de backup documentados
- [ ] Troubleshooting básico documentado
- [ ] Contatos de emergência anotados

## 🎯 Deploy Final

- [ ] Build de produção executado
- [ ] Variáveis de ambiente configuradas no servidor
- [ ] Aplicação deployada
- [ ] Healthcheck passa (aplicação responde)
- [ ] Login de admin testado em produção
- [ ] Registro de novo usuário testado em produção
- [ ] Logs de segurança verificados

## 🔄 Pós-Deploy

- [ ] Monitorar logs nas primeiras 24h
- [ ] Verificar se emails estão chegando
- [ ] Verificar se não há erros 500
- [ ] Verificar uso de CPU/memória do servidor
- [ ] Testar de diferentes IPs/locais
- [ ] Verificar se rate limiting está funcionando
- [ ] Criar primeiro backup do banco pós-deploy

---

## 📞 Em Caso de Problemas

### Senha não funciona
```bash
ssh usuario@servidor
cd /caminho/do/webapp
node set-admin-password.js "NovaSenh@Forte123"
```

### Ver logs de erro
```bash
# Logs do sistema
pm2 logs webapp

# Logs de segurança
node view-security-logs.js
```

### Desbloquear conta
```javascript
const db = require('better-sqlite3')('data/macacolandia.db');
db.prepare('DELETE FROM account_lockouts WHERE email = ?').run('email@user.com');
db.prepare('DELETE FROM failed_attempts WHERE email = ?').run('email@user.com');
db.close();
```

### Rollback
```bash
# Se usou Git
git revert HEAD
git push

# Se usou backup
cp backup/macacolandia.db.backup data/macacolandia.db
pm2 restart webapp
```

---

## ✅ ASSINATURA

**Data do Deploy:** ___/___/______

**Responsável:** _____________________

**Checklist Completo:** [ ] SIM  [ ] NÃO

**Observações:**
_____________________________________________
_____________________________________________
_____________________________________________

---

**🎉 Deploy aprovado e pronto para produção!**
