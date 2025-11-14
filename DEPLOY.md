# Deploy no Dokploy

## Pré-requisitos
- Servidor/VPS (DigitalOcean, Linode, Vultr, etc.)
- Dokploy instalado no servidor

## 1. Instalar Dokploy

SSH no servidor:
```bash
ssh root@seu-servidor-ip
```

Instalar Dokploy:
```bash
curl -sSL https://dokploy.com/install.sh | sh
```

Aguarde 2-3 minutos. Depois acesse: `http://seu-servidor-ip:3000`

## 2. Criar Projeto

1. Abra `http://seu-servidor-ip:3000`
2. Faça login (primeiro acesso cria conta admin)
3. Clique em **"Create Project"**
4. Nome: `macacolandia-bot`

## 3. Adicionar Aplicação

1. Dentro do projeto, clique **"Add Application"**
2. Nome: `bot`
3. Source: **GitHub**
4. Repository: `1Kkayke/macacolandia-bot`
5. Branch: `main`

## 4. Configurar Build

- Build Type: **Dockerfile**
- Dockerfile Path: `Dockerfile`
- Build Context: `/`

## 5. Variáveis de Ambiente

Na aba **Environment**, adicione:

```
DISCORD_TOKEN=seu_token_aqui
PREFIX=/
```

## 6. Recursos (Opcional)

Na aba **Advanced**:
- Memory: 512MB-1GB
- Restart Policy: Always

## 7. Deploy

1. Clique **"Deploy"**
2. Acompanhe logs de build (2-3 min)
3. Verifique logs: deve aparecer `🤖 Bot conectado como MacacolandiaBot`

## Pronto!

Bot online 24/7. Todo push no GitHub atualiza automaticamente.

## Comandos do Bot

Use `/help` no Discord para ver todos os comandos.
