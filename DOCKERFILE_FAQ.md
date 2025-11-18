# ❓ FAQ: Dockerfiles no Projeto Macacolândia Bot

## Pergunta Principal

> "Eu tenho um Dockerfile para o bot no projeto, mas eu tenho um webapp que eu estou subindo no Dokploy, será que eu preciso criar um outro Dockerfile para subir no Dokploy?"

## ✅ Resposta: SIM, você precisa de dois Dockerfiles separados!

### Por que?

O projeto Macacolândia Bot consiste em **duas aplicações completamente diferentes**:

#### 1. 🤖 Bot Discord (Python)
- **Localização**: Raiz do projeto
- **Dockerfile**: `/Dockerfile`
- **Tecnologia**: Python 3.11
- **Dependências**: FFmpeg, discord.py, yt-dlp, etc.
- **Executa**: `python run.py`
- **Função**: Bot Discord com música e jogos

#### 2. 🌐 Painel Web Admin (Next.js)
- **Localização**: Pasta `webapp/`
- **Dockerfile**: `/webapp/Dockerfile` ⭐ (NOVO)
- **Tecnologia**: Node.js 18 + Next.js
- **Dependências**: React, Next.js, shadcn/ui, etc.
- **Executa**: Servidor Next.js
- **Função**: Interface web administrativa

### 🔑 Diferenças Fundamentais

| Aspecto | Bot Discord | WebApp Admin |
|---------|-------------|--------------|
| **Linguagem** | Python | JavaScript/TypeScript |
| **Framework** | discord.py | Next.js |
| **Base Image** | `python:3.11-slim` | `node:18-alpine` |
| **Sistema Operacional** | Debian | Alpine Linux |
| **Build** | Apenas copia arquivos | Build completo do Next.js |
| **Porta** | Nenhuma (cliente Discord) | 3000 (servidor HTTP) |
| **Tamanho** | ~500MB | ~150MB (otimizado) |

## 📁 Estrutura de Dockerfiles no Projeto

```
macacolandia-bot/
├── Dockerfile                    # ← Para o BOT (Python)
├── docker-compose.yml           # Compose apenas para bot
├── docker-compose.full.yml      # ⭐ Compose com bot + webapp
├── DEPLOY.md                    # Deploy do bot
├── DOKPLOY_DEPLOY.md           # Deploy do webapp no Dokploy
│
└── webapp/
    ├── Dockerfile               # ⭐ Para o WEBAPP (Next.js)
    ├── .dockerignore           # ⭐ Otimização do build
    ├── DOCKER_README.md        # ⭐ Documentação detalhada
    └── ...
```

## 🚀 Como Usar no Dokploy

### Deploy do Bot (já existente)

1. **Projeto**: Macacolândia Bot
2. **Build Type**: Dockerfile
3. **Dockerfile**: `Dockerfile` (raiz)
4. **Build Context**: `/` (raiz)
5. **Variáveis**: `DISCORD_TOKEN`, `PREFIX`

### Deploy do WebApp (novo)

1. **Projeto**: Mesmo projeto do bot
2. **Add Service**: Nova aplicação
3. **Build Type**: Dockerfile
4. **Dockerfile**: `Dockerfile`
5. **Build Context**: `webapp` ⭐
6. **Port**: `3000`
7. **Variáveis**: `NEXTAUTH_URL`, `NEXTAUTH_SECRET`, `EMAIL_*`, etc.

### Volume Compartilhado

Ambas aplicações precisam compartilhar o banco de dados:

```yaml
volumes:
  - ./data:/app/data  # Mesmo volume para bot e webapp
```

## 💡 Por que não um único Dockerfile?

Você **poderia** tecnicamente criar um único Dockerfile que instala Python E Node.js, mas isso seria:

❌ **Ruim**:
- Imagem muito maior (>1GB)
- Mais vulnerabilidades de segurança
- Builds mais lentos
- Dificulta manutenção
- Viola princípios de containers (uma responsabilidade por container)

✅ **Melhor** (atual):
- Imagens otimizadas e pequenas
- Builds independentes e mais rápidos
- Escalabilidade separada
- Facilita debugging
- Segue melhores práticas Docker

## 🔄 Fluxo de Deployment Completo

### No Dokploy:

1. **Bot Discord** (Aplicação 1)
   ```
   Dockerfile: Dockerfile
   Context: /
   Volume: ./data -> /app/data
   ```

2. **WebApp Admin** (Aplicação 2)
   ```
   Dockerfile: Dockerfile
   Context: webapp
   Volume: ./data -> /app/data (mesmo do bot!)
   Port: 3000
   ```

### Compartilhamento de Dados:

```
Bot ─┬─> [SQLite DB] <─┬─ WebApp
     │                  │
     └─> /app/data <────┘
         (volume compartilhado)
```

## 📚 Documentação Relacionada

- **[DOKPLOY_DEPLOY.md](DOKPLOY_DEPLOY.md)**: Guia completo de deploy do webapp
- **[webapp/DOCKER_README.md](webapp/DOCKER_README.md)**: Detalhes técnicos do Dockerfile do webapp
- **[docker-compose.full.yml](docker-compose.full.yml)**: Exemplo de execução local
- **[DEPLOY.md](DEPLOY.md)**: Deploy do bot Discord

## 🎯 Resumo Executivo

**Resposta Curta**: SIM, você precisa de 2 Dockerfiles:
1. `/Dockerfile` - Para o bot Python (já existe)
2. `/webapp/Dockerfile` - Para o webapp Next.js (✅ criado agora)

**Por que**: São aplicações completamente diferentes com requisitos distintos de runtime, build e dependências.

**Benefícios**: Imagens otimizadas, builds mais rápidos, melhor segurança, manutenção mais fácil.

## ✅ Checklist de Deployment

- [x] Dockerfile do bot existe (`/Dockerfile`)
- [x] Dockerfile do webapp criado (`/webapp/Dockerfile`)
- [x] Documentação atualizada
- [x] `.dockerignore` otimizado
- [x] Build local testado
- [x] Docker compose de exemplo criado
- [ ] Deploy no Dokploy (próximo passo)

## 🤝 Próximos Passos

1. Faça push deste branch
2. Siga o guia [DOKPLOY_DEPLOY.md](DOKPLOY_DEPLOY.md)
3. Configure o webapp no Dokploy usando `webapp/Dockerfile`
4. Configure o volume compartilhado
5. Teste o acesso ao painel admin

---

<p align="center">
  <strong>🎮 Dois containers, uma solução completa! 🚀</strong><br>
  <em>Bot Discord + Painel Web Admin</em>
</p>
