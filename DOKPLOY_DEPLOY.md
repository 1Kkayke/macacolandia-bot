# 🚀 Guia de Deploy no Dokploy - Macacolândia Bot Web App

Este guia detalha como fazer o deploy do painel administrativo web do Bot Macacolândia no Dokploy, no mesmo projeto do bot já ativo.

## ❓ Preciso de um Dockerfile separado para o WebApp?

**SIM!** O repositório agora inclui dois Dockerfiles diferentes:

1. **`Dockerfile`** (na raiz do projeto) - Para o bot Discord (Python)
   - Usa Python 3.11
   - Instala FFmpeg para música
   - Executa `run.py`

2. **`webapp/Dockerfile`** (dentro da pasta webapp) - Para o painel web (Next.js)
   - Usa Node.js 18
   - Build otimizado com standalone output
   - Multi-stage build para imagem menor
   - Executa servidor Next.js

Ambos compartilham o mesmo banco de dados SQLite através de volumes compartilhados, mas são aplicações completamente diferentes que precisam de Dockerfiles específicos.

## 📋 Pré-requisitos

- Dokploy instalado e configurado
- Bot Macacolândia já rodando no Dokploy
- Acesso ao painel Dokploy
- Conta de email configurada (Gmail recomendado)

---

## 🗂️ Estrutura do Projeto

O projeto consiste em dois componentes principais:
1. **Bot Discord** (Python) - Já ativo no Dokploy
2. **Web App** (Next.js) - Novo componente a ser adicionado

Ambos compartilham o mesmo banco de dados SQLite (`data/macacolandia.db`).

---

## ⚙️ Passo 1: Configurar Email para Notificações

### Opção A: Gmail (Recomendado)

1. **Ativar Verificação em 2 Etapas**:
   - Acesse: https://myaccount.google.com/security
   - Ative a verificação em 2 etapas

2. **Gerar Senha de App**:
   - Acesse: https://myaccount.google.com/apppasswords
   - Nome: "Macacolandia Bot"
   - Copie a senha gerada (16 caracteres)

3. **Configurações de Email**:
   ```env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_SECURE=false
   EMAIL_USER=seu-email@gmail.com
   EMAIL_PASS=senha-de-app-aqui
   ADMIN_EMAIL=kayke.contato21@gmail.com
   ```

### Opção B: Outros Provedores

**Outlook/Hotmail**:
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_SECURE=false
```

**Yahoo**:
```env
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_SECURE=false
```

---

## 🔐 Passo 2: Configurar Variáveis de Ambiente

No painel do Dokploy, adicione as seguintes variáveis de ambiente:

### Variáveis Obrigatórias:

```env
# NextAuth (Autenticação)
NEXTAUTH_URL=https://seu-dominio.com
NEXTAUTH_SECRET=gere-um-secret-forte-aqui

# Email (Notificações de Registro)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_SECURE=false
EMAIL_USER=seu-email@gmail.com
EMAIL_PASS=sua-senha-de-app
ADMIN_EMAIL=kayke.contato21@gmail.com

# Banco de Dados
DATABASE_PATH=../data/macacolandia.db
```

### Como Gerar NEXTAUTH_SECRET:

**No Linux/Mac**:
```bash
openssl rand -base64 32
```

**No Windows (PowerShell)**:
```powershell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

**Online** (alternativa):
- Acesse: https://generate-secret.vercel.app/32

---

## 🏗️ Passo 3: Deploy no Dokploy

### 3.1 Acessar o Projeto Existente

1. Entre no painel Dokploy
2. Acesse o projeto do **Macacolândia Bot**
3. Clique em **"Add Service"** ou **"New Application"**

### 3.2 Configurar Aplicação Next.js

**Configurações Básicas**:
- **Nome**: `macacolandia-webapp`
- **Tipo**: Docker / Dockerfile
- **Branch**: `main` (ou sua branch)
- **Root Directory**: `webapp`
- **Dockerfile Path**: `Dockerfile` (está dentro da pasta webapp)

**Build Settings**:
- **Build Type**: Dockerfile
- **Dockerfile**: `Dockerfile`
- **Build Context**: `webapp`
- **Port**: `3000`

**Nota Importante**: O repositório agora inclui um `Dockerfile` específico para o webapp dentro da pasta `webapp/`. Este Dockerfile é otimizado para produção com Next.js standalone output e é diferente do Dockerfile do bot Python.

**Environment Variables**: (copie do passo 2)

### 3.3 Configurar Volume Compartilhado

Para compartilhar o banco de dados entre o bot e o webapp:

1. No Dokploy, vá em **Volumes**
2. Se já existe um volume para o bot (`/app/data`), use o mesmo
3. Adicione o volume ao webapp:
   - **Host Path**: `/caminho/para/data` (mesmo do bot)
   - **Container Path**: `/app/data`

### 3.4 Configurar Domínio

1. Vá em **Domains**
2. Adicione seu domínio: `admin.seubot.com`
3. Configure certificado SSL (Let's Encrypt)

### 3.5 Deploy

1. Clique em **"Deploy"**
2. Aguarde o build (2-5 minutos)
3. Verifique os logs para erros

---

## 👤 Passo 4: Criar Primeiro Usuário Admin

### 4.1 Registrar via Interface

1. Acesse: `https://seu-dominio.com/auth/register`
2. Preencha o formulário com seus dados
3. Aguarde email de confirmação

### 4.2 Aprovar Manualmente (Primeiro Usuário)

Como o primeiro usuário, você precisa aprovar a si mesmo diretamente no banco de dados:

**Opção A: Via Dokploy Terminal**

1. Acesse o terminal do container webapp no Dokploy
2. Execute:

```bash
# Acessar o diretório do banco
cd /app

# Instalar sqlite3 (se necessário)
apk add sqlite

# Acessar o banco
sqlite3 data/macacolandia.db

# Aprovar sua solicitação
UPDATE pending_registrations SET status = 'approved' WHERE email = 'seu-email@gmail.com';

# Criar usuário admin
INSERT INTO auth_users (name, email, password, role, approved) 
SELECT name, email, password, 'admin', 1 
FROM pending_registrations 
WHERE email = 'seu-email@gmail.com' AND status = 'approved';

# Sair
.exit
```

**Opção B: Via SSH no Servidor**

```bash
# Conectar ao servidor
ssh user@seu-servidor

# Localizar container
docker ps | grep webapp

# Acessar container
docker exec -it <container-id> sh

# Seguir comandos da Opção A
```

### 4.3 Fazer Login

1. Acesse: `https://seu-dominio.com/auth/login`
2. Entre com suas credenciais
3. Você terá acesso ao painel admin

---

## 🛠️ Passo 5: Configuração Pós-Deploy

### 5.1 Testar Email

1. Crie um usuário de teste em `/auth/register`
2. Verifique se o email chegou em `kayke.contato21@gmail.com`
3. Aprove o usuário em `/admin/registrations`

### 5.2 Configurar Backup Automático

No Dokploy, configure backup do volume de dados:

1. **Frequência**: Diária
2. **Retenção**: 7 dias
3. **Inclui**: Volume `/app/data`

### 5.3 Monitoramento

Configure alertas no Dokploy para:
- Uso de CPU > 80%
- Uso de memória > 80%
- Container offline

---

## 🔒 Passo 6: Segurança

### 6.1 Firewall

Certifique-se de que apenas as portas necessárias estão expostas:
- `443` (HTTPS) - Público
- `80` (HTTP - redireciona para HTTPS) - Público
- Outras portas - Bloqueadas

### 6.2 SSL/TLS

O Dokploy deve configurar automaticamente:
- Certificado Let's Encrypt
- Redirecionamento HTTP → HTTPS
- HSTS headers

### 6.3 Rate Limiting

Considere adicionar rate limiting no Dokploy ou Nginx:

```nginx
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

location /api/auth {
    limit_req zone=login burst=5;
}
```

---

## 📊 Passo 7: Gerenciar Usuários

### 7.1 Aprovar Novos Usuários

1. Acesse `/admin/registrations`
2. Veja solicitações pendentes
3. Clique em **"Aprovar"** ou **"Rejeitar"**

### 7.2 Gerenciar Usuários Existentes

Em `/admin/users`, você pode:
- ✅ **Aprovar** usuários
- 🔒 **Bloquear** acesso
- 🔓 **Desbloquear** usuários
- 👑 **Promover** para admin
- 🗑️ **Remover** usuários

### 7.3 Visualizar Logs

Em `/admin/logs`, você pode:
- Ver todas as ações dos usuários
- Filtrar por data
- Exportar logs (futuro)

---

## 🎮 Passo 8: Gerenciar Bot

### 8.1 Acessar Dashboard Principal

Em `/` (página principal):
- Selecione o servidor Discord
- Visualize estatísticas
- Gerencie moedas dos jogadores

### 8.2 Adicionar/Remover Moedas

1. Selecione um servidor
2. Clique no usuário
3. Digite quantidade
4. Adicione descrição (opcional)
5. Clique em **"Adicionar"** ou **"Remover"**

### 8.3 Visualizar Estatísticas

Dashboard mostra:
- Total de usuários
- Moedas em circulação
- Jogos realizados
- Win rates por jogo

---

## 🐛 Troubleshooting

### Problema: Email Não Está Sendo Enviado

**Solução 1: Verificar Credenciais**
```bash
# No terminal do container
node -e "const nodemailer = require('nodemailer'); const t = nodemailer.createTransport({host:'smtp.gmail.com',port:587,auth:{user:'seu-email',pass:'sua-senha'}}); t.verify().then(console.log).catch(console.error);"
```

**Solução 2: Verificar Firewall**
- Certifique-se de que a porta 587 está aberta
- Teste: `telnet smtp.gmail.com 587`

**Solução 3: Logs**
```bash
# Ver logs do webapp
docker logs <container-id> | grep -i email
```

### Problema: Banco de Dados Não Encontrado

**Verificar Volume**:
```bash
# No container
ls -la /app/data/
ls -la ../data/

# Deve mostrar: macacolandia.db
```

**Corrigir Path**:
- Verifique variável `DATABASE_PATH` no Dokploy
- Deve ser: `../data/macacolandia.db` ou `/app/data/macacolandia.db`

### Problema: Autenticação Não Funciona

**Verificar NEXTAUTH_SECRET**:
```bash
# No terminal do container
echo $NEXTAUTH_SECRET

# Deve mostrar uma string longa (44+ caracteres)
```

**Regenerar Secret**:
1. Gere novo secret
2. Atualize variável no Dokploy
3. Redeploy a aplicação

### Problema: Middleware Loop

Se você cair em loop de redirecionamento:

1. Verifique variável `NEXTAUTH_URL`
2. Deve ser: `https://seu-dominio.com` (sem barra final)
3. Limpe cookies do navegador
4. Tente novamente

---

## 📝 Checklist de Deploy

Use este checklist para garantir que tudo está configurado:

### Pré-Deploy
- [ ] Dokploy instalado e acessível
- [ ] Bot Discord rodando no Dokploy
- [ ] Domínio configurado e apontando para servidor
- [ ] Email de administrador configurado
- [ ] Senha de app do Gmail gerada

### Configuração
- [ ] Variáveis de ambiente adicionadas no Dokploy
- [ ] NEXTAUTH_SECRET gerado (32+ caracteres)
- [ ] NEXTAUTH_URL configurado com domínio correto
- [ ] EMAIL_USER e EMAIL_PASS configurados
- [ ] ADMIN_EMAIL configurado
- [ ] Volume compartilhado configurado

### Deploy
- [ ] Aplicação Next.js adicionada no Dokploy
- [ ] Build executado sem erros
- [ ] Container iniciado com sucesso
- [ ] Logs não mostram erros críticos

### Pós-Deploy
- [ ] Domínio acessível via HTTPS
- [ ] Página de registro carrega
- [ ] Email de registro é enviado
- [ ] Primeiro admin criado e pode fazer login
- [ ] Dashboard principal carrega
- [ ] Dados do bot aparecem corretamente

### Segurança
- [ ] SSL/TLS ativo (certificado válido)
- [ ] HTTP redireciona para HTTPS
- [ ] Apenas portas 80/443 expostas
- [ ] Firewall configurado
- [ ] Backup automático ativo

---

## 🎯 Próximos Passos

Após o deploy bem-sucedido:

1. **Convidar Equipe**:
   - Envie link de registro para administradores
   - Aprove contas conforme necessário

2. **Documentar Processos**:
   - Como adicionar moedas
   - Como gerenciar eventos
   - Políticas de moderação

3. **Monitorar Sistema**:
   - Configure alertas
   - Revise logs semanalmente
   - Acompanhe uso de recursos

4. **Backup e Recuperação**:
   - Teste processo de restauração
   - Documente procedimentos
   - Mantenha backups off-site

---

## 📞 Suporte

### Documentação Adicional
- **Webapp Setup**: `WEBAPP_SETUP.md`
- **Features**: `WEBAPP_FEATURES.md`
- **Main README**: `README.md`

### Logs Úteis
```bash
# Logs do webapp
docker logs macacolandia-webapp

# Logs do bot
docker logs macacolandia-bot

# Logs do Dokploy
journalctl -u dokploy
```

### Comandos Úteis
```bash
# Reiniciar webapp
docker restart macacolandia-webapp

# Ver status
docker ps | grep macacolandia

# Acessar terminal
docker exec -it macacolandia-webapp sh

# Ver uso de recursos
docker stats macacolandia-webapp
```

---

## ✅ Conclusão

Seguindo este guia, você terá:
- ✅ Web app funcionando no Dokploy
- ✅ Sistema de autenticação seguro
- ✅ Notificações por email configuradas
- ✅ Painel admin completo
- ✅ Gerenciamento de usuários
- ✅ Integração com bot Discord

O sistema está pronto para produção e pode ser usado imediatamente pela equipe!

---

<p align="center">
  <strong>🎮 Macacolândia Bot - Dokploy Deployment Guide 🚀</strong><br>
  <em>Deploy profissional e seguro</em>
</p>
