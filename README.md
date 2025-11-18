# 🎮 Bot Macacolândia - Música, Cassino & Diversão

<p align="center">
  <img src="bot_avatar.svg" alt="Bot Avatar" width="200"/>
</p>

Um bot completo para Discord feito em Python com música, jogos de cassino, sistema de economia e comandos interativos!

## 🌐 Novo: Painel de Administração Web!

Agora o Bot Macacolândia inclui um **painel web completo** para administração! Gerencie usuários, moedas e visualize estatísticas através de uma interface moderna e responsiva.

**[📖 Ver Guia de Configuração do Web App →](WEBAPP_SETUP.md)**
**[🐳 Ver Guia de Docker do Web App →](webapp/DOCKER_README.md)** ⭐ NOVO!

### Principais Funcionalidades do Painel Web:
- 💰 Adicionar/remover moedas de jogadores
- 📊 Dashboard com estatísticas em tempo real
- 👥 Gerenciar usuários por servidor
- 📈 Visualizar histórico de jogos e transações
- 🏆 Ver conquistas desbloqueadas
- 📱 Interface responsiva e moderna

### 🐳 Deploy com Docker
O projeto agora inclui **Dockerfiles separados** para bot e webapp:
- **Bot Discord**: `Dockerfile` (Python)
- **WebApp Admin**: `webapp/Dockerfile` (Next.js)

**[❓ Por que dois Dockerfiles? →](DOCKERFILE_FAQ.md)**

[Acesse a documentação completa do webapp →](webapp/README.md)

## ✨ Características

### 🎵 Sistema de Música
- **Reprodução de Música**: Toca músicas do YouTube via URL ou busca
- **Sistema de Fila**: Gerenciamento completo de fila de músicas
- **Controle de Volume**: Ajuste fino de volume com comandos dedicados
- **Controles de Reprodução**: Play, pause, resume, skip, stop
- **Shuffle**: Embaralhe sua fila de músicas

### 🎰 Cassino & Jogos
- **Tigrinho (Fortune Tiger)**: Slot 3x3 com símbolos temáticos e múltiplas linhas de pagamento
- **Crash**: Multiplier cresce até crashar - saque antes do crash!
- **Double**: Aposta em cores (vermelho/preto 2x, branco 14x)
- **Mines**: Campo minado interativo com múltiplas dificuldades
- **Roleta Europeia**: Apostas em números, cores, paridade e altura
- **Caça-Níqueis (Slots)**: Sistema de símbolos com multiplicadores
- **Dados**: Múltiplos modos de jogo (acima/abaixo, alto/baixo, número específico)
- **Blackjack (21)**: Jogo interativo de cartas contra o dealer

### 💰 Sistema de Economia
- **Moedas Virtuais**: Sistema completo de economia interna
- **Recompensas Diárias**: Ganhe moedas todos os dias com bônus de sequência
- **Transferências**: Transfira moedas entre usuários
- **Histórico de Transações**: Acompanhe todas as suas transações
- **Persistência**: Todos os dados salvos em banco de dados SQLite

### 🏆 Gamificação
- **Conquistas**: Sistema de achievements com recompensas
- **Ranking/Leaderboard**: Veja os jogadores mais ricos do servidor
- **Estatísticas**: Acompanhe jogos jogados, vitórias e derrotas
- **Sequências (Streaks)**: Bônus por login diário consecutivo

### 🎉 Comandos Divertidos
- **Piadas**: 20+ piadas de programação e gerais
- **Trivia/Quiz**: Perguntas com recompensas em moedas
- **Enquetes**: Sistema de votação com tempo limitado
- **Bola Mágica 8**: Pergunte e receba respostas místicas
- **Interface em Português**: Totalmente em português brasileiro

## 🚀 Comandos Disponíveis

### 🎵 Música

#### Reprodução
- `!play <url/busca>` ou `!p <url/busca>` - Toca uma música do YouTube
- `!pause` ou `!pausar` - Pausa a música atual
- `!resume` ou `!retomar` - Retoma a música pausada
- `!stop` ou `!parar` - Para a música e limpa a fila
- `!skip` ou `!pular` ou `!s` - Pula para a próxima música
- `!leave` ou `!sair` - Desconecta o bot do canal de voz

#### Controle de Volume
- `!volume <0-100>` ou `!vol <0-100>` - Define o volume (0-100%)
- `!volumeup` ou `!v+` ou `!aumentar` - Aumenta o volume em 10%
- `!volumedown` ou `!v-` ou `!diminuir` - Diminui o volume em 10%

#### Gerenciamento de Fila
- `!queue` ou `!q` ou `!fila` - Mostra a fila de músicas
- `!nowplaying` ou `!np` ou `!tocando` - Mostra a música atual
- `!clear` ou `!limpar` - Limpa a fila de músicas
- `!shuffle` ou `!embaralhar` - Embaralha a fila

### 💰 Economia

- `!saldo` ou `!balance` - Mostra seu saldo de moedas e estatísticas
- `!diario` ou `!daily` - Reivindica sua recompensa diária (100+ moedas)
- `!transferir <@user> <valor>` ou `!give` - Transfere moedas para outro usuário
- `!historico` ou `!history` - Mostra seu histórico de transações
- `!ranking` ou `!leaderboard` - Top 10 jogadores mais ricos
- `!conquistas` ou `!achievements` - Veja suas conquistas desbloqueadas

### 🎰 Jogos de Cassino

#### Tigrinho (Fortune Tiger) 🐅
```
!tigrinho <valor>
```
Slot 3x3 inspirado no Fortune Tiger com símbolos temáticos orientais. Combine símbolos em linhas (horizontal, vertical ou diagonal) para ganhar!

**Símbolos e Multiplicadores:**
- 🪙 Moeda: 2x
- 🎋 Bambu: 3x
- 🏮 Lanterna: 5x
- 💰 Ouro: 8x
- 🐉 Dragão: 12x
- 🎴 Carta: 20x
- 🐅 Tigre: 50x (raro!)
- 💎 Diamante: 100x (jackpot!)

**Recursos:**
- Múltiplas linhas de pagamento (8 linhas)
- Animação de giro realista
- Multiplicadores acumulam para múltiplas linhas vencedoras

#### Crash 🚀
```
!crash <valor> [multiplicador_alvo]
```
O multiplicador começa em 1.0x e cresce até crashar. Defina seu multiplicador alvo para cash out automático antes do crash!

**Como Jogar:**
- O jogo calcula um ponto de crash aleatório
- Você define um multiplicador alvo (exemplo: 2.0x)
- Se o crash acontecer depois do seu alvo, você ganha!
- Se crashar antes, você perde

**Dicas:**
- 🟢 Baixo Risco: < 1.5x
- 🟡 Risco Moderado: 1.5x - 2.0x
- 🟠 Alto Risco: 2.0x - 5.0x
- 🔴 Risco Extremo: > 5.0x

#### Double 🎡
```
!double <valor> <cor>
```
Apostas em cores com diferentes probabilidades e pagamentos.

**Opções de Aposta:**
- 🔴 **Vermelho**: 2x (46.7% de chance)
- ⚫ **Preto**: 2x (46.7% de chance)
- ⚪ **Branco**: 14x (6.7% de chance - raro!)

**Recursos:**
- Histórico dos últimos 10 resultados
- Animação de roleta girando
- Alta emoção com a opção branco!

#### Mines 💣
```
!mines <valor> [dificuldade]
```
Campo minado interativo! Revele tiles seguros e aumente seu multiplicador. Um único erro e você perde tudo!

**Dificuldades:**
- `facil`: 3 minas (mais fácil, menor multiplicador)
- `medio`: 5 minas (balanceado)
- `dificil`: 8 minas (mais difícil, maior multiplicador)
- `extremo`: 10 minas (muito difícil, multiplicador máximo!)

**Como Jogar:**
1. Use `revelar <linha> <coluna>` para revelar um tile (exemplo: `revelar 0 0`)
2. Cada tile seguro aumenta seu multiplicador
3. Digite `sair` a qualquer momento para sacar com o multiplicador atual
4. Acerte uma mina 💣 e perca tudo!

**Estratégia:**
- Grade 5x5 = 25 tiles
- Multiplicador cresce exponencialmente
- Sacar cedo = menor risco, menor recompensa
- Continuar = maior risco, maior recompensa!

#### Caça-Níqueis
```
!slots <valor>
```
Combine 3 símbolos iguais para ganhar! Multiplicadores de até 50x.

#### Roleta
```
!roleta <valor> <tipo> <aposta>
```
**Tipos de Aposta:**
- `numero <0-36>` - Aposta em número específico (35x)
- `cor <vermelho/preto>` - Aposta na cor (2x)
- `paridade <par/impar>` - Aposta em par ou ímpar (2x)
- `altura <baixo/alto>` - Baixo (1-18) ou Alto (19-36) (2x)

#### Dados
```
!dados <valor> <tipo>
```
**Tipos de Aposta:**
- `acima` - Soma > 7 (2x)
- `abaixo` - Soma < 7 (2x)
- `sete` - Soma = 7 (5x)
- `alto` - Dado 4-6 (2x)
- `baixo` - Dado 1-3 (2x)
- `1-6` - Número específico (6x)

#### Blackjack (21)
```
!blackjack <valor>
```
Jogo interativo de cartas. Use reações para pedir cartas (⬇️) ou parar (🛑).
- Blackjack paga 2.5x
- Vitória normal paga 2x
- Empate devolve a aposta
Apostas simples com 2x de retorno.

### 🎉 Diversão & Interação

- `!piada` ou `!joke` - Conta uma piada aleatória
- `!trivia` ou `!quiz` - Quiz com recompensa de 50 moedas
- `!enquete <min> "pergunta" "op1" "op2"` - Cria uma enquete com votação
- `!8ball <pergunta>` - Pergunta à bola mágica 8
- `!jogos` - Lista todos os jogos disponíveis

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
PREFIX=/
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
🎮 Bot Macacolândia está online!
------
```

### Exemplos de Uso

#### Música
```
!play Never Gonna Give You Up
!play https://www.youtube.com/watch?v=dQw4w9WgXcQ
!volume 50
!queue
!skip
```

#### Economia
```
!saldo                      # Ver seu saldo
!diario                     # Recompensa diária
!transferir @user 100       # Transferir 100 moedas
!ranking                    # Ver top 10
!conquistas                 # Ver achievements
```

#### Jogos de Cassino
```
!tigrinho 100               # Fortune Tiger slot 3x3
!crash 100 2.5              # Crash com alvo 2.5x
!double 100 vermelho        # Apostar 100 em vermelho
!mines 100 medio            # Campo minado médio
!slots 100                  # Caça-níqueis com 100 moedas
!roleta 50 cor vermelho     # Apostar 50 na cor vermelha
!dados 100 acima            # Apostar 100 que soma > 7
!blackjack 200              # Jogar blackjack com 200
```

#### Diversão
```
!piada                      # Piada aleatória
!trivia                     # Quiz com recompensa
!enquete 5 "Melhor linguagem?" "Python" "JavaScript" "Go"
!8ball Vou ganhar hoje?     # Bola mágica
```
   !volumeup
   !volumedown
   ```

## 🛠️ Tecnologias Utilizadas

- **[discord.py](https://github.com/Rapptz/discord.py)**: Biblioteca Python para Discord
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: Extrator de vídeos do YouTube
- **[FFmpeg](https://ffmpeg.org/)**: Processamento de áudio
- **[PyNaCl](https://github.com/pyca/pynacl/)**: Criptografia para voz
- **[python-dotenv](https://github.com/theskumar/python-dotenv)**: Gerenciamento de variáveis de ambiente
- **[SQLite3](https://www.sqlite.org/)**: Banco de dados para economia e estatísticas

## 📁 Estrutura do Projeto

```
macacolandia-bot/
├── src/                       # Código fonte principal
│   ├── __init__.py           # Inicializador do pacote
│   ├── bot.py                # Ponto de entrada do bot
│   ├── config.py             # Configurações e variáveis de ambiente
│   ├── core/                 # Utilitários centrais
│   │   ├── achievements.py   # Sistema de conquistas
│   │   └── checks.py         # Verificações de comandos
│   ├── database/             # Camada de banco de dados
│   │   ├── db_manager.py     # Gerenciador de banco de dados
│   │   └── models.py         # Modelos de dados
│   ├── economy/              # Sistema de economia
│   │   └── economy_manager.py # Gerenciador de economia
│   ├── games/                # Jogos de cassino
│   │   ├── roulette.py       # Roleta
│   │   ├── slots.py          # Caça-níqueis
│   │   ├── dice.py           # Dados
│   │   └── blackjack.py      # Blackjack
│   ├── fun/                  # Comandos divertidos
│   │   ├── jokes.py          # Sistema de piadas
│   │   ├── trivia.py         # Sistema de quiz
│   │   └── poll.py           # Sistema de enquetes
│   ├── music/                # Módulo de música
│   │   ├── source.py         # Streaming de áudio
│   │   └── queue.py          # Gerenciamento de fila
│   └── cogs/                 # Comandos organizados em cogs
│       ├── general.py        # Comandos gerais (help)
│       ├── music.py          # Comandos de música
│       ├── economy.py        # Comandos de economia
│       ├── games.py          # Comandos de jogos
│       └── fun.py            # Comandos divertidos
├── data/                     # Banco de dados (gerado automaticamente)
│   └── macacolandia.db       # SQLite database
├── run.py                    # Script principal para iniciar o bot
├── bot.py                    # Wrapper de compatibilidade
├── requirements.txt          # Dependências do projeto
├── .env.example             # Exemplo de arquivo de configuração
├── .gitignore               # Arquivos ignorados pelo Git
├── bot_avatar.svg           # Avatar do bot
├── start.sh                 # Script de inicialização (Linux/macOS)
├── start.bat                # Script de inicialização (Windows)
├── Dockerfile               # Configuração Docker
├── docker-compose.yml       # Configuração Docker Compose
└── README.md                # Este arquivo
```

## 🎯 Sistema de Conquistas

O bot possui um sistema de conquistas que recompensa os jogadores:

| Conquista | Descrição | Recompensa |
|-----------|-----------|------------|
| 🎮 Primeira Aposta | Jogue seu primeiro jogo | 100 🪙 |
| 💎 Apostador de Elite | Tenha 10.000 moedas ou mais | 500 🪙 |
| 🎖️ Veterano | Jogue 100 jogos | 1.000 🪙 |
| 🍀 Sortudo | 7 dias de sequência de recompensas diárias | 500 🪙 |
| 🏆 Grande Vencedor | Ganhe 5.000 moedas no total | 250 🪙 |
| 💰 Milionário | Acumule 50.000 moedas | 5.000 🪙 |

## 🎲 Mecânicas dos Jogos

### Tigrinho (Fortune Tiger)
- **Grade**: 3x3 com 9 posições
- **Linhas de Pagamento**: 8 linhas (3 horizontais, 3 verticais, 2 diagonais)
- **Símbolos**: 🪙 🎋 🏮 💰 🐉 🎴 🐅 💎
- **Pagamento**: Combinações em linhas acumulam multiplicadores
- **Multiplicadores**: De 2x (Moeda) até 100x (Diamante)
- **Especial**: Múltiplas linhas vencedoras multiplicam os ganhos!

### Crash
- **Mecânica**: Multiplicador cresce de 1.0x até crashar
- **House Edge**: ~1% (crash médio em 1.98x)
- **Range**: 1.0x até 100x
- **Distribuição**: Exponencial - crashes baixos são mais comuns
- **Estratégia**: Defina alvo antes do jogo começar

### Double
- **Cores**: Vermelho, Preto, Branco
- **Probabilidades**:
  - Vermelho: 46.7% (7/15) - Paga 2x
  - Preto: 46.7% (7/15) - Paga 2x
  - Branco: 6.7% (1/15) - Paga 14x
- **Histórico**: Últimos 10 resultados visíveis

### Mines
- **Grade**: 5x5 (25 tiles)
- **Dificuldades**:
  - Fácil: 3 minas (22 seguros)
  - Médio: 5 minas (20 seguros)
  - Difícil: 8 minas (17 seguros)
  - Extremo: 10 minas (15 seguros)
- **Multiplicador**: Cresce exponencialmente com cada tile revelado
- **Pagamento**: Pode sacar a qualquer momento antes de acertar mina
- **Risco vs Recompensa**: Mais tiles = maior multiplicador, maior risco

### Caça-Níqueis (Slots)
- **Símbolos**: 🍒 🍋 🍊 🍇 🍉 ⭐ 💎 🎰
- **Pagamento**: 3 iguais = multiplicador cheio, 2 iguais = metade do multiplicador
- **Multiplicadores**: De 2x (🍒) até 50x (🎰)

### Roleta
- **Números**: 0-36 (Roleta Europeia)
- **Cores**: Vermelho, Preto, Verde (0)
- **Pagamentos**:
  - Número específico: 35x
  - Cor/Paridade/Altura: 2x

### Dados
- **Modos de Jogo**:
  - Over/Under 7: 2x
  - Seven: 5x
  - High/Low (1 dado): 2x
  - Número específico: 6x

### Blackjack
- **Regras**: Padrão de cassino
- **Dealer**: Para em 17
- **Pagamentos**:
  - Blackjack: 2.5x
  - Vitória: 2x
  - Empate: Devolve aposta

## 🐛 Solução de Problemas

### O bot não se conecta
- Verifique se o token está correto no arquivo `.env`
- Certifique-se de que o bot tem permissões no servidor
- Verifique se todas as intents estão habilitadas no Discord Developer Portal

### Erro ao reproduzir música
- Verifique se o FFmpeg está instalado corretamente
- Execute `ffmpeg -version` para confirmar
- No Windows, ajuste o caminho do FFmpeg em `src/config.py` se necessário

### YouTube pede login / Músicas restritas não funcionam

Se você receber erros como "Sign in to confirm you're not a bot" ou músicas que requerem login:

1. **Execute o script de extração de cookies:**
```bash
python extract_cookies.py
```

O script tentará extrair cookies automaticamente dos seguintes navegadores:
- Google Chrome
- Microsoft Edge
- Mozilla Firefox
- Opera
- Brave

2. **Alternativa manual (se o script não funcionar):**
   - Instale a extensão "Get cookies.txt LOCALLY" no seu navegador
   - Acesse [youtube.com](https://youtube.com) e faça login
   - Clique na extensão e baixe o arquivo `cookies.txt`
   - Renomeie para `youtube_cookies.txt` e coloque na pasta raiz do bot

3. **Reinicie o bot**
   - O bot detectará automaticamente os cookies
   - Você verá a mensagem: "✅ Cookies do YouTube carregados!"

**Notas importantes:**
- Os cookies expiram após alguns meses - execute o script novamente se necessário
- Mantenha o arquivo `youtube_cookies.txt` privado (já está no .gitignore)
- Este método permite que o bot acesse vídeos que requerem verificação de idade ou login

### O bot não responde aos comandos
- Verifique se o prefixo está correto (padrão: `/`)
- Certifique-se de que o bot tem permissão para ler mensagens
- Verifique se a intent `message_content` está ativada

### Erro de banco de dados
- O bot cria automaticamente o banco de dados na primeira execução
- Certifique-se de que a pasta `data/` pode ser criada
- Em caso de corrupção, delete o arquivo `data/macacolandia.db` para recriá-lo

### Jogos não funcionam
- Verifique se você tem saldo suficiente (`!saldo`)
- A aposta mínima é 10 moedas
- Use `!diario` para receber sua recompensa diária inicial

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
