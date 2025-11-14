# 🚂 Como fazer Deploy no Railway.app

## 📋 Pré-requisitos

1. Conta no GitHub (seu repositório já está lá!)
2. Conta no Railway.app (gratuita)

## 🚀 Passo a Passo

### 1. Criar conta no Railway

1. Acesse: https://railway.app/
2. Clique em **"Start a New Project"** ou **"Login with GitHub"**
3. Faça login com sua conta do GitHub

### 2. Fazer Push do código para GitHub

Se ainda não fez push das alterações:

```bash
git add .
git commit -m "Configuração para Railway"
git push origin main
```

### 3. Criar novo projeto no Railway

1. No Railway, clique em **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Escolha o repositório **`1Kkayke/macacolandia-bot`**
4. Railway vai detectar automaticamente o Dockerfile

### 4. Configurar Variáveis de Ambiente

1. No projeto criado, clique em **"Variables"**
2. Adicione as seguintes variáveis:
   - `DISCORD_TOKEN` = `seu_token_do_discord_aqui`
   - `PREFIX` = `/`

**IMPORTANTE:** Use o token que você tem no arquivo `.env` local!

### 5. Deploy

- Railway vai fazer o deploy automaticamente!
- Aguarde alguns minutos
- O bot ficará online 24/7

## 📊 Monitoramento

- Veja logs em tempo real no dashboard do Railway
- O bot reinicia automaticamente se cair
- Plano gratuito: $5 de crédito por mês (suficiente para um bot pequeno)

## 🔄 Atualizações Futuras

Sempre que você fizer push no GitHub, o Railway atualiza automaticamente:

```bash
git add .
git commit -m "Atualização do bot"
git push origin main
```

## ⚠️ Importante

- Nunca commite o arquivo `.env` (já está no `.gitignore`)
- Use as variáveis de ambiente do Railway para configurações sensíveis
- O plano gratuito tem limitações de uso mensal

## 💡 Dicas

- **Monitorar uso**: Verifique o consumo no dashboard
- **Logs**: Use o terminal do Railway para ver logs em tempo real
- **Reiniciar**: Pode reiniciar o serviço manualmente se necessário
