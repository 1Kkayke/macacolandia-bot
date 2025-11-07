# 🚀 Guia Rápido de Início

## ⚡ Início em 5 Minutos

### Passo 1: Pré-requisitos
```bash
# Verifique se tem Python 3.8+
python3 --version

# Verifique se tem FFmpeg
ffmpeg -version
```

Se não tiver, instale:
- **Python**: [python.org/downloads](https://www.python.org/downloads/)
- **FFmpeg**: [ffmpeg.org/download.html](https://ffmpeg.org/download.html)

### Passo 2: Clone e Configure
```bash
# Clone o repositório
git clone https://github.com/1Kkayke/macacolandia-bot.git
cd macacolandia-bot

# Instale as dependências
pip install -r requirements.txt

# Configure o token
cp .env.example .env
# Edite .env e adicione seu token do Discord
```

### Passo 3: Crie o Bot no Discord

1. Vá para [discord.com/developers/applications](https://discord.com/developers/applications)
2. Clique em "New Application"
3. Dê um nome (ex: "Macacolândia Music")
4. Vá em "Bot" → "Add Bot"
5. Copie o token e cole no arquivo `.env`
6. Em "Privileged Gateway Intents", ative:
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT (opcional)

### Passo 4: Adicione ao Servidor

Use este link (substitua CLIENT_ID pelo ID da sua aplicação):
```
https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=3165184&scope=bot
```

Para encontrar o CLIENT_ID:
- Vá em "OAuth2" → "General"
- Copie o "CLIENT ID"

### Passo 5: Execute o Bot

**Linux/macOS:**
```bash
./start.sh
```

**Windows:**
```batch
start.bat
```

**Ou diretamente:**
```bash
python bot.py
```

## 🎮 Primeiros Comandos

Depois que o bot estiver online no seu servidor:

1. **Entre em um canal de voz**

2. **Digite no chat:**
   ```
   !play Never Gonna Give You Up
   ```

3. **Teste outros comandos:**
   ```
   !pause
   !resume
   !volume 80
   !queue
   !help
   ```

## 🐳 Alternativa: Docker

Se preferir usar Docker:

```bash
# Configure o .env primeiro
cp .env.example .env
# Edite .env com seu token

# Inicie o bot
docker-compose up -d

# Veja os logs
docker-compose logs -f

# Pare o bot
docker-compose down
```

## ❓ Problemas Comuns

### Bot não conecta
- ✅ Verifique se o token está correto no `.env`
- ✅ Confira se MESSAGE CONTENT INTENT está ativo

### Bot não responde
- ✅ Certifique-se de usar o prefixo correto (padrão: `!`)
- ✅ Verifique se o bot tem permissão de ler/enviar mensagens

### Não toca música
- ✅ Confirme que FFmpeg está instalado: `ffmpeg -version`
- ✅ Certifique-se de estar em um canal de voz
- ✅ Verifique as permissões de voz do bot

### Erro ao instalar dependências
```bash
# Tente atualizar o pip
pip install --upgrade pip

# Instale novamente
pip install -r requirements.txt
```

## 📞 Suporte

- 📖 Leia o [README.md](README.md) completo
- 🎯 Veja os [FEATURES.md](FEATURES.md) para detalhes
- 🐛 Abra uma issue no GitHub para bugs
- 💡 Contribua com pull requests!

## ✅ Checklist de Verificação

Antes de reportar problemas, verifique:

- [ ] Python 3.8+ instalado
- [ ] FFmpeg instalado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Arquivo `.env` criado com token válido
- [ ] Bot adicionado ao servidor com permissões corretas
- [ ] MESSAGE CONTENT INTENT ativado no Discord Developer Portal
- [ ] Você está em um canal de voz ao testar comandos de música

---

🎉 **Pronto! Seu bot de música está funcionando!**

Use `!help` no Discord para ver todos os comandos disponíveis.
