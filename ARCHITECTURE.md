# Arquitetura do Projeto

Este documento descreve a arquitetura e organização do código do Macacolândia Bot após a refatoração.

## 📁 Estrutura de Diretórios

```
macacolandia-bot/
├── src/                    # Código fonte principal
│   ├── __init__.py        # Inicializador do pacote
│   ├── bot.py             # Ponto de entrada do bot
│   ├── config.py          # Configurações e variáveis de ambiente
│   ├── music/             # Módulo de música
│   │   ├── __init__.py
│   │   ├── source.py      # Classe YTDLSource (streaming de áudio)
│   │   └── queue.py       # Classe MusicQueue (gerenciamento de fila)
│   └── cogs/              # Comandos organizados em cogs
│       ├── __init__.py
│       ├── general.py     # Comandos gerais (help, etc)
│       └── music.py       # Comandos de música
├── run.py                 # Script principal para iniciar o bot
├── bot.py                 # Wrapper para compatibilidade retroativa
└── bot_legacy.py          # Código original (antes da refatoração)
```

## 🏗️ Arquitetura

### Módulos Principais

#### `src/config.py`
Centraliza todas as configurações do bot:
- Carrega variáveis de ambiente (.env)
- Define opções do YouTube-DL
- Define opções do FFmpeg
- Exporta TOKEN e PREFIX

#### `src/music/`
Pacote responsável pela funcionalidade de música:

**`source.py`** - Classe `YTDLSource`
- Herda de `discord.PCMVolumeTransformer`
- Gerencia streaming de áudio do YouTube
- Extrai informações de vídeos (título, duração, thumbnail)
- Implementa timeout de 60 segundos para buscas

**`queue.py`** - Classe `MusicQueue`
- Gerencia fila de músicas por servidor (guild)
- Métodos: add, get_next, clear, shuffle
- Mantém controle de volume
- Rastreia música atual

#### `src/cogs/`
Comandos organizados usando o padrão Cogs do discord.py:

**`general.py`** - Cog `General`
- Comando `help`: exibe todos os comandos disponíveis
- Comandos utilitários gerais

**`music.py`** - Cog `Music`
- Comandos de reprodução: play, pause, resume, stop, skip
- Comandos de volume: volume, volumeup, volumedown
- Comandos de fila: queue, nowplaying, clear, shuffle
- Comando de voz: leave

#### `src/bot.py`
Ponto de entrada principal do bot:
- Configura intents do Discord
- Cria instância do bot
- Registra event handlers (on_ready, on_command_error)
- Carrega todos os cogs
- Inicia o bot

## 🔄 Fluxo de Execução

1. **Inicialização**
   ```
   run.py → src.bot.main() → Bot instance creation → Load cogs → bot.start(TOKEN)
   ```

2. **Comando de Música**
   ```
   User: !play música
   → Discord event
   → Bot command parser
   → Music cog
   → YTDLSource.from_url()
   → MusicQueue.add() or immediate play
   → FFmpeg audio streaming
   ```

3. **Sistema de Fila**
   ```
   Música termina
   → after_playing callback
   → play_next()
   → MusicQueue.get_next()
   → Toca próxima música ou notifica fim da fila
   ```

## 🎯 Benefícios da Refatoração

### Antes (bot.py monolítico - 500 linhas)
- ❌ Todo código em um único arquivo
- ❌ Difícil de navegar e manter
- ❌ Sem separação de responsabilidades
- ❌ Difícil de testar componentes individuais
- ❌ Mudanças arriscadas devido ao acoplamento

### Depois (arquitetura modular)
- ✅ Código organizado por responsabilidade
- ✅ Módulos independentes e reutilizáveis
- ✅ Fácil de localizar e modificar funcionalidades
- ✅ Melhor testabilidade de componentes
- ✅ Segue boas práticas do discord.py (Cogs)
- ✅ Escalável para novos recursos
- ✅ Compatibilidade retroativa mantida

## 📝 Padrões de Código

### Cogs (discord.py)
Os cogs são a forma recomendada de organizar comandos no discord.py:
- Agrupa comandos relacionados
- Facilita carregar/descarregar funcionalidades
- Permite reutilização entre projetos
- Melhora organização do código

### Separação de Preocupações
Cada módulo tem uma responsabilidade clara:
- **Config**: Gerencia configuração
- **Music/Source**: Gerencia streaming de áudio
- **Music/Queue**: Gerencia fila de reprodução
- **Cogs**: Implementam comandos do Discord

## 🚀 Como Adicionar Novos Recursos

### Adicionar um novo comando de música:
1. Abra `src/cogs/music.py`
2. Adicione método com decorator `@commands.command()`
3. O comando estará disponível automaticamente

### Adicionar um novo tipo de comando:
1. Crie novo arquivo em `src/cogs/`, ex: `src/cogs/admin.py`
2. Defina classe que herda de `commands.Cog`
3. Adicione função `async def setup(bot)` no final
4. Carregue o cog em `src/bot.py` com `await bot.load_extension()`

### Adicionar nova funcionalidade de música:
1. Para gerenciamento de fila: modifique `src/music/queue.py`
2. Para streaming de áudio: modifique `src/music/source.py`

## 🧪 Testabilidade

A nova estrutura permite testes unitários fáceis:

```python
# Testar MusicQueue
from src.music.queue import MusicQueue

def test_queue():
    queue = MusicQueue()
    queue.add("song1")
    assert queue.size() == 1
    assert queue.get_next() == "song1"
    assert queue.is_empty()
```

## 📚 Referências

- [discord.py Documentation](https://discordpy.readthedocs.io/)
- [discord.py Cogs Guide](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html)
- [Python Package Structure](https://docs.python.org/3/tutorial/modules.html#packages)
