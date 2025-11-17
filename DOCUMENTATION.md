# 📚 Documentação Técnica - Bot Macacolândia

## Índice
1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Módulos](#módulos)
4. [Banco de Dados](#banco-de-dados)
5. [Sistema de Economia](#sistema-de-economia)
6. [Jogos](#jogos)
7. [Conquistas](#conquistas)
8. [Extensibilidade](#extensibilidade)

## Visão Geral

O Bot Macacolândia é um bot Discord completo desenvolvido em Python que combina funcionalidades de música, jogos de cassino, sistema de economia e comandos interativos. O projeto foi estruturado seguindo princípios de clean code, modularidade e escalabilidade.

### Tecnologias Principais
- **Python 3.8+**
- **discord.py 2.3.2**: Framework para bots Discord
- **SQLite3**: Banco de dados relacional embutido
- **yt-dlp**: Download e streaming de áudio do YouTube
- **FFmpeg**: Processamento de áudio

## Arquitetura

### Padrão de Design
O bot utiliza o padrão **Cog** do discord.py para organizar comandos em módulos separados, facilitando a manutenção e expansão.

### Estrutura de Diretórios

```
src/
├── core/              # Funcionalidades centrais
├── database/          # Camada de persistência
├── economy/           # Lógica de economia
├── games/             # Implementações de jogos
├── fun/               # Comandos interativos
├── music/             # Sistema de música
├── cogs/              # Comandos Discord (interface)
├── bot.py             # Entry point
└── config.py          # Configurações
```

### Fluxo de Dados

```
Discord → Cog (Interface) → Manager (Lógica) → Database (Persistência)
                                ↓
                            Game Logic
```

## Módulos

### 1. Core (`src/core/`)

#### achievements.py
**Propósito**: Gerencia o sistema de conquistas do bot.

**Classes Principais**:
- `Achievement`: Define uma conquista
  - `name`: Identificador único
  - `title`: Título exibido
  - `description`: Descrição da conquista
  - `emoji`: Emoji representativo
  - `condition`: Função lambda para verificar desbloqueio
  - `reward`: Moedas de recompensa

- `AchievementManager`: Gerencia conquistas
  - `check_achievements(user_id, username)`: Verifica e desbloqueia conquistas
  - `get_achievement(name)`: Obtém conquista por nome
  - `get_all_achievements()`: Lista todas as conquistas

**Conquistas Disponíveis**:
1. **first_game**: Primeira aposta (100 moedas)
2. **high_roller**: 10.000+ moedas (500 moedas)
3. **veteran**: 100 jogos jogados (1.000 moedas)
4. **lucky_streak**: 7 dias de streak (500 moedas)
5. **big_winner**: 5.000 moedas ganhas (250 moedas)
6. **millionaire**: 50.000+ moedas (5.000 moedas)

#### checks.py
**Propósito**: Verificações e controle de estado de jogos.

**Funcionalidades**:
- `is_user_playing(user_id)`: Verifica se usuário está jogando
- `start_game(user_id, game_type)`: Marca início de jogo
- `end_game(user_id)`: Marca fim de jogo
- `ensure_not_playing(ctx)`: Previne jogos concorrentes

### 2. Database (`src/database/`)

#### db_manager.py
**Propósito**: Camada de abstração para operações de banco de dados.

**Classe Principal**: `DatabaseManager`

**Tabelas**:
1. **users**: Dados dos usuários
   - user_id (PK)
   - username
   - coins (moedas atuais)
   - total_won (total ganho)
   - total_lost (total perdido)
   - games_played
   - created_at
   - last_daily (última recompensa diária)
   - streak (dias consecutivos)

2. **transactions**: Histórico de transações
   - id (PK)
   - user_id (FK)
   - amount
   - transaction_type
   - description
   - timestamp

3. **game_history**: Histórico de jogos
   - id (PK)
   - user_id (FK)
   - game_type
   - bet_amount
   - result
   - winnings
   - timestamp

4. **achievements**: Conquistas desbloqueadas
   - id (PK)
   - user_id (FK)
   - achievement_name
   - unlocked_at

**Métodos Principais**:
- `get_user(user_id, username)`: Obtém ou cria usuário
- `update_coins(user_id, amount)`: Atualiza saldo
- `transfer_coins(from_user, to_user, amount)`: Transfere moedas
- `record_game(...)`: Registra resultado de jogo
- `claim_daily_reward(user_id)`: Reivindica recompensa diária
- `get_leaderboard(limit)`: Obtém ranking

#### models.py
**Propósito**: Define modelos de dados usando dataclasses.

### 3. Economy (`src/economy/`)

#### economy_manager.py
**Propósito**: Gerencia operações econômicas de alto nível.

**Classe Principal**: `EconomyManager`

**Métodos**:
- `get_balance(user_id, username)`: Consulta saldo
- `add_coins(user_id, amount, reason)`: Adiciona moedas
- `remove_coins(user_id, amount, reason)`: Remove moedas
- `transfer_coins(from_user, to_user, amount)`: Transferência
- `can_afford(user_id, username, amount)`: Verifica saldo
- `process_bet(...)`: Processa resultado de aposta

**Fluxo de Aposta**:
```
1. Verifica saldo (can_afford)
2. Remove aposta (remove_coins)
3. Determina resultado (game logic)
4. Se ganhou: adiciona prêmio (add_coins)
5. Registra no histórico (record_game)
```

### 4. Games (`src/games/`)

#### roulette.py
**Jogo**: Roleta Europeia (0-36)

**Implementação**:
- Números vermelhos e pretos definidos
- Tipos de aposta: número, cor, paridade, altura
- Multiplicadores: 35x (número), 2x (outros)

**Métodos**:
- `spin()`: Gira a roleta (0-36)
- `get_color(number)`: Retorna cor do número
- `check_bet(number, bet_type, bet_value)`: Verifica se ganhou

#### slots.py
**Jogo**: Caça-níqueis de 3 rolos

**Símbolos e Multiplicadores**:
```python
🍒: 2x   (mais comum)
🍋: 3x
🍊: 4x
🍇: 5x
🍉: 7x
⭐: 10x
💎: 20x
🎰: 50x  (jackpot)
```

**Mecânica**:
- 3 símbolos iguais: multiplicador cheio
- 2 símbolos iguais: metade do multiplicador
- Sistema de pesos para raridade

**Métodos**:
- `spin()`: Gira os rolos
- `calculate_win(reels)`: Calcula ganhos

#### dice.py
**Jogo**: Dados com múltiplos modos

**Modos de Jogo**:
1. **Over/Under** (2 dados):
   - Acima de 7: 2x
   - Abaixo de 7: 2x
   - Exatamente 7: 5x

2. **High/Low** (1 dado):
   - Alto (4-6): 2x
   - Baixo (1-3): 2x

3. **Número Específico**:
   - Acertar número: 6x

**Métodos**:
- `roll_dice(num_dice)`: Rola dados
- `play_over_under(bet_type, threshold)`: Joga over/under
- `play_high_low(prediction)`: Joga high/low
- `play_specific_number(bet_number)`: Aposta em número

#### blackjack.py
**Jogo**: Blackjack/21 clássico

**Classes**:
- `Card`: Representa uma carta (rank, suit)
- `Hand`: Gerencia mão de cartas
- `BlackjackGame`: Lógica do jogo

**Regras**:
- Dealer para em 17
- Ás conta como 11 ou 1
- Blackjack (21 com 2 cartas) paga 2.5x
- Vitória normal paga 2x
- Empate devolve aposta

**Fluxo de Jogo**:
```
1. Deal inicial (2 cartas cada)
2. Jogador: Hit ou Stand
3. Dealer joga (se jogador não estourar)
4. Comparar mãos
5. Determinar vencedor
```

### 5. Fun (`src/fun/`)

#### jokes.py
**Funcionalidade**: Sistema de piadas

- 20+ piadas de programação e gerais
- Seleção aleatória
- Expansível (adicionar novas piadas no array)

#### trivia.py
**Funcionalidade**: Sistema de quiz/trivia

**Estrutura**:
- `Question`: pergunta, opções, resposta correta, categoria
- `TriviaManager`: gerencia banco de perguntas

**Categorias**:
- Programação
- Tecnologia
- Computação
- Hardware
- Ciência
- Geografia
- História
- Arte

**Recompensa**: 50 moedas por resposta correta

#### poll.py
**Funcionalidade**: Sistema de enquetes com votação

**Classes**:
- `Poll`: representa uma enquete
  - Pergunta
  - Opções (máximo 10)
  - Votos dos usuários
  - Duração/expiração

- `PollManager`: gerencia enquetes ativas

**Características**:
- Votação única por usuário
- Duração configurável (1-60 minutos)
- Resultados com gráficos de barras
- Auto-expiração

### 6. Music (`src/music/`)

Sistema existente mantido e integrado.

#### source.py
- `YTDLSource`: Streaming de áudio do YouTube

#### queue.py
- `MusicQueue`: Gerencia fila de músicas

### 7. Cogs (`src/cogs/`)

#### general.py
**Comandos**: help, ajuda

Interface principal de ajuda com todos os comandos categorizados.

#### economy.py
**Comandos**:
- `saldo`: Exibe saldo e estatísticas
- `transferir`: Transfere moedas entre usuários
- `diario`: Recompensa diária com streak
- `historico`: Histórico de transações
- `ranking`: Top 10 jogadores
- `conquistas`: Lista conquistas do usuário

#### games.py
**Comandos**:
- `roleta`: Joga roleta
- `slots`: Joga caça-níqueis
- `dados`: Joga dados
- `blackjack`: Joga blackjack
- `jogos`: Lista todos os jogos

**Características**:
- Verificação de saldo antes de apostar
- Prevenção de jogos concorrentes
- Processamento automático de apostas
- Verificação de conquistas após cada jogo
- Embeds informativos com resultados

#### fun.py
**Comandos**:
- `piada`: Piada aleatória
- `trivia`: Quiz interativo
- `enquete`: Cria enquete
- `coinflip`: Cara ou coroa
- `8ball`: Bola mágica 8

#### music.py
Comandos de música (sistema existente).

## Sistema de Economia

### Fluxo de Moedas

```
Entrada de Moedas:
├── Recompensa diária (100 + streak bonus)
├── Conquistas desbloqueadas
├── Vitórias em jogos
├── Transferências recebidas
└── Trivia correta (50)

Saída de Moedas:
├── Apostas em jogos
├── Transferências enviadas
└── (Futuro: compras, itens, etc.)
```

### Economia Balanceada

**Valores Iniciais**:
- Saldo inicial: 1.000 moedas
- Recompensa diária base: 100 moedas
- Aposta mínima: 10 moedas

**Multiplicadores**:
- Seguros (2x): Cor, paridade, high/low
- Médios (5-6x): Seven, número específico
- Altos (35x+): Número na roleta, jackpot slots

**Recompensas**:
- Conquistas: 100 - 5.000 moedas
- Trivia: 50 moedas
- Streak diário: até +200 moedas

## Conquistas

### Sistema de Auto-Unlock

```python
1. Usuário completa ação (jogo, login diário, etc.)
2. AchievementManager.check_achievements() é chamado
3. Para cada conquista:
   a. Verifica condição
   b. Se atendida e não desbloqueada:
      - Desbloqueia conquista
      - Adiciona recompensa
      - Registra transação
      - Retorna conquista
4. Exibe conquistas desbloqueadas ao usuário
```

### Adicionando Novas Conquistas

```python
# Em src/core/achievements.py
achievements['nova_conquista'] = Achievement(
    'nova_conquista',                    # nome único
    'Título da Conquista',               # título exibido
    'Descrição da conquista',            # descrição
    '🎯',                                 # emoji
    lambda stats: stats['condicao'],     # condição
    500                                   # recompensa em moedas
)
```

## Extensibilidade

### Adicionando Novo Jogo

1. **Criar arquivo do jogo** em `src/games/`:
```python
# src/games/novo_jogo.py
class NovoJogo:
    @staticmethod
    def jogar(params):
        # Lógica do jogo
        return ganhou, multiplicador
```

2. **Adicionar ao __init__.py**:
```python
# src/games/__init__.py
from .novo_jogo import NovoJogo
__all__ = [..., 'NovoJogo']
```

3. **Criar comando no cog**:
```python
# src/cogs/games.py
@commands.command(name='novogame')
async def novo_game(self, ctx, bet_amount: int):
    # Verificações padrão
    # Jogar jogo
    # Processar aposta
    # Exibir resultado
```

### Adicionando Nova Categoria de Comando

1. **Criar novo cog** em `src/cogs/`:
```python
# src/cogs/novo_cog.py
from discord.ext import commands

class NovoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='comando')
    async def comando(self, ctx):
        pass

async def setup(bot):
    await bot.add_cog(NovoCog(bot))
```

2. **Registrar no bot**:
```python
# src/bot.py
await bot.load_extension('src.cogs.novo_cog')
```

### Modificando Banco de Dados

Para adicionar novas tabelas ou campos:

1. **Atualizar schema** em `db_manager.py`:
```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS nova_tabela (
        id INTEGER PRIMARY KEY,
        campo TEXT
    )
''')
```

2. **Adicionar métodos** para manipular novos dados
3. **Atualizar modelos** em `models.py` se necessário

## Boas Práticas

### Segurança
- ✅ Nunca expor tokens ou senhas no código
- ✅ Usar variáveis de ambiente (.env)
- ✅ Validar entradas do usuário
- ✅ Prevenir SQL injection (parametrização)

### Performance
- ✅ Usar conexões de banco eficientemente
- ✅ Limitar queries pesadas
- ✅ Usar índices em campos frequentemente consultados
- ✅ Cache de dados quando apropriado

### Manutenibilidade
- ✅ Separação de responsabilidades (SoC)
- ✅ Código documentado
- ✅ Nomes descritivos de variáveis e funções
- ✅ DRY (Don't Repeat Yourself)
- ✅ Tratamento de erros adequado

## Testes

### Testando Comandos Localmente

```python
# Exemplo de teste manual
python bot.py

# No Discord:
/saldo              # Verifica economia
/diario             # Testa recompensa
/slots 100          # Testa jogo
/conquistas         # Verifica achievements
```

### Áreas de Teste Críticas

1. **Economia**:
   - Transferências
   - Saldo negativo (prevenir)
   - Apostas maiores que saldo

2. **Jogos**:
   - Cálculo correto de multiplicadores
   - Pagamentos corretos
   - Prevenção de jogo concorrente

3. **Banco de Dados**:
   - Criação automática de tabelas
   - Transações atômicas
   - Integridade referencial

## Conclusão

O Bot Macacolândia foi estruturado com foco em:
- **Modularidade**: Fácil adicionar novos recursos
- **Escalabilidade**: Suporta crescimento de usuários e funcionalidades
- **Manutenibilidade**: Código limpo e bem organizado
- **Experiência do Usuário**: Interface intuitiva em português
- **Gamificação**: Sistema de recompensas e conquistas engajante

A arquitetura permite expansão fácil com novos jogos, comandos e funcionalidades sem afetar código existente.
