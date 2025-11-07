# 🎵 Bot de Música Macacolândia

<p align="center">
  <img src="bot_avatar.svg" alt="Bot Avatar" width="200"/>
</p>

Um bot completo de música para Discord feito em Python, com suporte a YouTube e comandos avançados de controle!

## 📋 Características

- 🎵 **Reprodução de Música**: Toca músicas do YouTube via URL ou busca
- 📋 **Sistema de Fila**: Gerenciamento completo de fila de músicas
- 🔊 **Controle de Volume**: Ajuste fino de volume com comandos dedicados
- ⏯️ **Controles de Reprodução**: Play, pause, resume, skip, stop
- 🔀 **Shuffle**: Embaralhe sua fila de músicas
- 📊 **Informações Detalhadas**: Exibe informações sobre músicas com thumbnails
- 🌐 **Comandos em Português**: Interface totalmente em português brasileiro

## 🚀 Comandos Disponíveis

### 🎵 Reprodução
- `!play <url/busca>` ou `!p <url/busca>` - Toca uma música do YouTube
- `!pause` ou `!pausar` - Pausa a música atual
- `!resume` ou `!retomar` - Retoma a música pausada
- `!stop` ou `!parar` - Para a música e limpa a fila
- `!skip` ou `!pular` ou `!s` - Pula para a próxima música
- `!leave` ou `!sair` - Desconecta o bot do canal de voz

### 🔊 Controle de Volume
- `!volume <0-100>` ou `!vol <0-100>` - Define o volume (0-100%)
- `!volumeup` ou `!v+` ou `!aumentar` - Aumenta o volume em 10%
- `!volumedown` ou `!v-` ou `!diminuir` - Diminui o volume em 10%

### 📋 Gerenciamento de Fila
- `!queue` ou `!q` ou `!fila` - Mostra a fila de músicas
- `!nowplaying` ou `!np` ou `!tocando` - Mostra a música atual
- `!clear` ou `!limpar` - Limpa a fila de músicas
- `!shuffle` ou `!embaralhar` - Embaralha a fila

### ℹ️ Ajuda
- `!help` ou `!ajuda` - Mostra todos os comandos disponíveis

## 📦 Instalação

### Pré-requisitos

1. **Python 3.8+** instalado
2. **FFmpeg** instalado no sistema
3. Uma conta Discord e um bot criado no [Discord Developer Portal](https://discord.com/developers/applications)

### Instalando FFmpeg

#### Windows
Baixe de [ffmpeg.org](https://ffmpeg.org/download.html) e adicione ao PATH do sistema.

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS
```bash
brew install ffmpeg
```

### Configuração do Bot

1. Clone este repositório:
```bash
git clone https://github.com/1Kkayke/macacolandia-bot.git
cd macacolandia-bot
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
```

4. Edite o arquivo `.env` e adicione seu token do Discord:
```env
DISCORD_TOKEN=seu_token_aqui
PREFIX=!
```

### Como Obter o Token do Bot

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Clique em "New Application" e dê um nome ao seu bot
3. Vá para a seção "Bot" no menu lateral
4. Clique em "Add Bot"
5. Em "TOKEN", clique em "Copy" para copiar seu token
6. Cole o token no arquivo `.env`

### Permissões Necessárias

Ao adicionar o bot ao seu servidor, certifique-se de que ele tem as seguintes permissões:

- ✅ Read Messages/View Channels
- ✅ Send Messages
- ✅ Embed Links
- ✅ Connect (Voice)
- ✅ Speak (Voice)
- ✅ Use Voice Activity

Link de convite sugerido (substitua `CLIENT_ID` pelo ID da sua aplicação):
```
https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=3165184&scope=bot
```

## 🎮 Uso

### Iniciar o Bot

#### Método 1: Script de Inicialização (Recomendado)

**Linux/macOS:**
```bash
./start.sh
```

**Windows:**
```batch
start.bat
```

#### Método 2: Diretamente com Python

```bash
python bot.py
```

#### Método 3: Com Docker

```bash
# Construir e iniciar o bot
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar o bot
docker-compose down
```

Você verá uma mensagem confirmando que o bot está online:
```
🤖 Bot conectado como NomeDoBot
📊 ID: 123456789
🎵 Bot de música Macacolândia está online!
------
```

### Exemplos de Uso

1. **Tocar uma música**:
   ```
   !play Never Gonna Give You Up
   !play https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

2. **Ajustar volume**:
   ```
   !volume 50
   !volumeup
   !volumedown
   ```

3. **Gerenciar fila**:
   ```
   !queue
   !shuffle
   !skip
   ```

## 🛠️ Tecnologias Utilizadas

- **[discord.py](https://github.com/Rapptz/discord.py)**: Biblioteca Python para Discord
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: Extrator de vídeos do YouTube
- **[FFmpeg](https://ffmpeg.org/)**: Processamento de áudio
- **[PyNaCl](https://github.com/pyca/pynacl/)**: Criptografia para voz
- **[python-dotenv](https://github.com/theskumar/python-dotenv)**: Gerenciamento de variáveis de ambiente

## 📁 Estrutura do Projeto

```
macacolandia-bot/
├── bot.py              # Arquivo principal do bot
├── requirements.txt    # Dependências do projeto
├── .env.example       # Exemplo de arquivo de configuração
├── .gitignore         # Arquivos ignorados pelo Git
├── bot_avatar.svg     # Avatar do bot
├── start.sh           # Script de inicialização (Linux/macOS)
├── start.bat          # Script de inicialização (Windows)
├── Dockerfile         # Configuração Docker
├── docker-compose.yml # Configuração Docker Compose
└── README.md          # Este arquivo
```

## 🐛 Solução de Problemas

### O bot não se conecta
- Verifique se o token está correto no arquivo `.env`
- Certifique-se de que o bot tem permissões no servidor

### Erro ao reproduzir música
- Verifique se o FFmpeg está instalado corretamente
- Execute `ffmpeg -version` para confirmar

### O bot não responde aos comandos
- Verifique se o prefixo está correto (padrão: `!`)
- Certifique-se de que o bot tem permissão para ler mensagens

### Qualidade de áudio ruim
- Ajuste o volume com `!volume`
- Verifique sua conexão de internet

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é de código aberto e está disponível para uso pessoal e educacional.

## 👤 Autor

**1Kkayke**

## 🙏 Agradecimentos

- Comunidade discord.py
- Desenvolvedores do yt-dlp
- Todos os contribuidores

---

<p align="center">
  Feito com ❤️ para a comunidade Macacolândia
</p>
