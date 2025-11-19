# 🔐 Configuração de Segurança - Dokploy

## Variáveis de Ambiente Obrigatórias

Para garantir a segurança do admin, configure estas variáveis no Dokploy:

### 1. No Painel do Dokploy

1. Acesse seu projeto no Dokploy
2. Vá em **Settings** → **Environment Variables**
3. Adicione as seguintes variáveis:

```env
# Credenciais do Admin (OBRIGATÓRIO)
ADMIN_EMAIL=admin@macacolandia.com
ADMIN_PASSWORD=SuaSenhaForteAqui123!

# NextAuth (OBRIGATÓRIO)
NEXTAUTH_URL=https://seu-dominio.com
NEXTAUTH_SECRET=gere-um-secret-com-openssl-rand-base64-32

# reCAPTCHA (Opcional)
NEXT_PUBLIC_RECAPTCHA_SITE_KEY=sua-site-key
RECAPTCHA_SECRET_KEY=sua-secret-key
```

### 2. Gerar NEXTAUTH_SECRET

No terminal local:
```bash
openssl rand -base64 32
```

Copie o resultado e cole na variável `NEXTAUTH_SECRET` no Dokploy.

### 3. Após Configurar as Variáveis

1. Recomendação de produção: não deixe `ADMIN_PASSWORD` como variável contínua no serviço.
	 - Em vez disso, execute o script `ensure-admin` manualmente (job one-off) para criar/atualizar a conta admin, e então remova `ADMIN_PASSWORD` do ambiente do serviço.

2. Como executar o `ensure-admin` manualmente:

- Pelo console/one-off do Dokploy (recomendado):
	- Abra o recurso de executar comandos/one-off container no painel do Dokploy
	- Defina temporariamente `ADMIN_EMAIL` e `ADMIN_PASSWORD` nas variáveis de ambiente do comando
	- Execute:
		```sh
		node scripts/ensure-admin.js
		```

- Ou via Docker local (exemplo):
	```powershell
	docker run --rm -e ADMIN_EMAIL=admin@macacolandia.com -e ADMIN_PASSWORD="SuaSenhaForteAqui" -e NEXTAUTH_SECRET="seu-secret" -v C:\path\to\data:/app/data macacolandia-webapp node scripts/ensure-admin.js
	```

3. Depois de executar com sucesso, verifique a saída do comando. Em seguida remova `ADMIN_PASSWORD` do ambiente do serviço e faça um deploy normal sem essa variável.

## 🚨 IMPORTANTE

- **NUNCA** commite arquivos `.env` ou `.env.local` no Git
- **SEMPRE** use variáveis de ambiente no Dokploy para produção
- Altere a senha padrão para algo forte e único
- Use um gerenciador de senhas para armazenar a senha do admin

## 🔄 Para Desenvolvimento Local

1. Copie o arquivo `.env.example` para `.env.local`:
```bash
cp .env.example .env.local
```

2. Edite `.env.local` e configure suas variáveis
3. Nunca commite o arquivo `.env.local`

## 📝 Scripts Disponíveis

```bash
# Garantir que o admin existe com as credenciais corretas
npm run ensure-admin

# Desenvolvimento
npm run dev

# Build para produção
npm run build

# Rodar em produção
npm start
```

## 🛡️ Recursos de Segurança Implementados

- ✅ Senhas criptografadas com bcrypt (12 rounds)
- ✅ Rate limiting (5 tentativas / 5 minutos)
- ✅ Bloqueio temporário após 5 tentativas falhas (15 minutos)
- ✅ Logs de segurança para auditoria
- ✅ Proteção contra CSRF e XSS
- ✅ Headers de segurança configurados
- ✅ Cookies HttpOnly e Secure em produção
