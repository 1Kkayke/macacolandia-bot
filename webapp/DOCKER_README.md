# 🐳 Dockerfile do WebApp - Macacolândia Bot

Este documento explica o Dockerfile do painel administrativo web do Bot Macacolândia.

## 📦 Visão Geral

O `Dockerfile` nesta pasta é específico para o **painel web Next.js** e é diferente do Dockerfile do bot Discord (que está na raiz do projeto).

### Por que um Dockerfile separado?

- **Bot Discord**: Aplicação Python que requer FFmpeg e bibliotecas Python
- **WebApp**: Aplicação Next.js que requer Node.js e build do frontend
- **Diferentes requisitos**: Cada aplicação tem dependências e processos de build únicos

## 🏗️ Estrutura do Dockerfile

O Dockerfile usa **multi-stage build** para otimizar o tamanho da imagem final:

### Stage 1: Dependencies
```dockerfile
FROM node:18-alpine AS deps
```
- Instala apenas as dependências do projeto
- Usa cache do Docker para acelerar builds subsequentes

### Stage 2: Builder
```dockerfile
FROM node:18-alpine AS builder
```
- Copia as dependências do stage anterior
- Executa `npm run build` para criar o build de produção
- Usa Next.js standalone output para imagem menor

### Stage 3: Runner
```dockerfile
FROM node:18-alpine AS runner
```
- Imagem final mínima apenas com arquivos necessários
- Executa como usuário não-root (`nextjs`) para segurança
- Expõe porta 3000

## 🚀 Como Usar

### Build Local

```bash
# Na pasta webapp
docker build -t macacolandia-webapp .

# Ou da raiz do projeto
docker build -t macacolandia-webapp -f webapp/Dockerfile webapp/
```

### Executar Container

```bash
docker run -d \
  --name webapp \
  -p 3000:3000 \
  -v ./data:/app/data \
  -e NEXTAUTH_URL=http://localhost:3000 \
  -e NEXTAUTH_SECRET=seu-secret-aqui \
  -e DATABASE_PATH=../data/macacolandia.db \
  macacolandia-webapp
```

### Com Docker Compose

Use o arquivo `docker-compose.full.yml` na raiz do projeto:

```bash
docker-compose -f docker-compose.full.yml up -d
```

## 🔧 Variáveis de Ambiente Necessárias

Configure estas variáveis no Dokploy ou em arquivo `.env`:

```env
# Autenticação
NEXTAUTH_URL=https://seu-dominio.com
NEXTAUTH_SECRET=gere-com-openssl-rand-base64-32

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_SECURE=false
EMAIL_USER=seu-email@gmail.com
EMAIL_PASS=sua-senha-de-app
ADMIN_EMAIL=admin@example.com

# Banco de Dados
DATABASE_PATH=../data/macacolandia.db
```

## 📁 Volumes Importantes

### `/app/data`
- **Propósito**: Compartilhar banco de dados SQLite entre bot e webapp
- **Configuração**: Mesmo volume usado pelo bot
- **Exemplo**: `-v ./data:/app/data`

## 🔒 Segurança

### Usuário Não-Root
O container executa como usuário `nextjs` (UID 1001) por segurança.

### Imagem Mínima
Usa `alpine` para reduzir superfície de ataque e tamanho da imagem.

### Standalone Output
Next.js standalone output reduz dependências e tamanho final.

## 📊 Otimizações

1. **Multi-stage Build**: Reduz tamanho final da imagem (~500MB → ~150MB)
2. **Layer Caching**: `package.json` copiado antes do código para cache eficiente
3. **Standalone Output**: Apenas arquivos necessários na imagem final
4. **Alpine Linux**: Base mínima e segura

## 🐛 Troubleshooting

### Build Falha em "npm ci"
**Solução**: O Dockerfile tem fallback para `npm install`:
```dockerfile
RUN npm ci || npm install
```

### Container não inicia
**Verifique**:
1. Variáveis de ambiente configuradas
2. Volume do banco de dados montado corretamente
3. Porta 3000 não está em uso

### Erro de permissão no banco de dados
**Solução**: Certifique-se que o usuário `nextjs` tem acesso ao volume:
```bash
# No host
chmod 755 ./data
chmod 644 ./data/macacolandia.db
```

## 📝 Deploy no Dokploy

Ao configurar no Dokploy:

1. **Build Type**: Dockerfile
2. **Dockerfile Path**: `Dockerfile`
3. **Build Context**: `webapp` (pasta raiz do webapp)
4. **Port**: `3000`

Veja o arquivo `DOKPLOY_DEPLOY.md` na raiz do projeto para instruções completas.

## 🔗 Arquivos Relacionados

- **`Dockerfile`**: Este arquivo
- **`.dockerignore`**: Arquivos excluídos do build
- **`next.config.ts`**: Configuração do Next.js (standalone output)
- **`docker-compose.full.yml`**: Compose com bot + webapp
- **`DOKPLOY_DEPLOY.md`**: Guia completo de deploy

## 💡 Dicas

1. **Desenvolvimento Local**: Use `npm run dev` ao invés do Docker
2. **Teste Build**: Execute `npm run build` localmente antes de fazer build Docker
3. **Logs**: Use `docker logs macacolandia-webapp` para debug
4. **Health Check**: Acesse `http://localhost:3000` para verificar status

---

<p align="center">
  <strong>🐳 Docker Build Otimizado para Produção</strong>
</p>
