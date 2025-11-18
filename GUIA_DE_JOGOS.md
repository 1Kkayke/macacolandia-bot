# 🎮 Guia Completo dos Jogos - Bot Macacolândia

Este guia contém todas as informações sobre como jogar e aproveitar os jogos do bot!

---

## 💰 Sistema de Economia

### `/saldo` ou `/balance`
**Mostra seu saldo, estatísticas e ranking**

```
/saldo
```

**O que você verá:**
- 💰 Moedas disponíveis
- 🎮 Total de jogos jogados
- ✅ Jogos ganhos
- ❌ Jogos perdidos
- 📊 Taxa de vitória (%)
- 🏆 Seu ranking no servidor

---

### `/diario` ou `/daily`
**Recompensa diária - quanto mais dias seguidos, maior o bônus!**

```
/diario
```

**Recompensas:**
- Base: 100 moedas
- Bônus de sequência: +10 moedas por dia consecutivo
- Máximo: 200 moedas/dia (após 10 dias seguidos)

**Exemplo:**
- Dia 1: 100 moedas
- Dia 2: 110 moedas
- Dia 3: 120 moedas
- Dia 10+: 200 moedas

⏰ **Cooldown:** 24 horas

---

### `/transferir` ou `/give`
**Transfere moedas para outro jogador**

```
/transferir @usuario 500
/give @usuario 500
```

**Parâmetros:**
- `@usuario`: Mencione o usuário (@nome)
- `valor`: Quantidade de moedas (mínimo 1)

**Requisitos:**
- Você precisa ter saldo suficiente
- Não pode transferir para si mesmo
- Não pode transferir para bots

---

### `/ranking` ou `/leaderboard`
**Top 10 jogadores mais ricos do servidor**

```
/ranking
```

Mostra:
- 🥇 Top 3 com emojis especiais
- Nome dos jogadores
- Saldo de cada um

---

### `/historico` ou `/history`
**Últimas 10 transações da sua conta**

```
/historico
```

Mostra para cada transação:
- Tipo (ganho/perda/transferência)
- Valor
- Data e hora
- Descrição

---

### `/conquistas` ou `/achievements`
**Veja suas conquistas desbloqueadas**

```
/conquistas
```

**Exemplos de conquistas:**
- 🎮 Primeira Aposta - Jogue seu primeiro jogo
- 💎 Apostador de Elite - Tenha 10.000+ moedas
- 🎖️ Veterano - Jogue 100 jogos
- 🍀 Sortudo - 7 dias de sequência diária
- 🏆 Grande Vencedor - Ganhe 5.000 moedas no total
- 💰 Milionário - Acumule 50.000 moedas

Cada conquista dá recompensa em moedas! 🎁

---

## 🎰 Jogos de Cassino

### 🐅 Tigrinho (Fortune Tiger)
**Slot machine 3x3 com múltiplas linhas de pagamento**

```
/tigrinho 100
```

**Parâmetros:**
- `valor`: Aposta (mínimo 10 moedas)

**Como funciona:**
- Grade 3x3 com 9 posições
- 8 linhas de pagamento (3 horizontais, 3 verticais, 2 diagonais)
- Combine 3 símbolos iguais em qualquer linha

**Símbolos e Multiplicadores:**
| Símbolo | Nome | Multiplicador |
|---------|------|---------------|
| 🪙 | Moeda | 2x |
| 🎋 | Bambu | 3x |
| 🏮 | Lanterna | 5x |
| 💰 | Ouro | 8x |
| 🐉 | Dragão | 12x |
| 🎴 | Carta | 20x |
| 🐅 | Tigre | 50x |
| 💎 | Diamante | 100x |

**Exemplo de vitória:**
```
Aposta: 100 moedas
Resultado:
🐅 🐅 🐅
💰 🐉 🎋
🏮 🪙 🎴

Linha horizontal superior: 🐅 🐅 🐅 = 50x
Ganho: 100 × 50 = 5.000 moedas! 🎉
```

**Dicas:**
- ✨ Múltiplas linhas vencedoras acumulam!
- 💎 Diamante é o jackpot (100x)
- 🐅 Tigre dá 50x (muito raro!)

---

### 🚀 Crash
**Multiplicador que cresce até crashar - saque antes!**

```
/crash 100 2.5
```

**Parâmetros:**
- `valor`: Aposta (mínimo 10 moedas)
- `multiplicador_alvo`: Onde você quer sacar (ex: 1.5, 2.0, 5.0)

**Como funciona:**
1. Você define seu multiplicador alvo ANTES
2. O jogo calcula um ponto de crash aleatório
3. Se o crash for DEPOIS do seu alvo = VOCÊ GANHA! 🎉
4. Se crashar ANTES do seu alvo = VOCÊ PERDE! 💥

**Exemplos:**

**Vitória:**
```
Aposta: 100 moedas
Alvo: 2.0x
Crash: 3.47x ✅

Você ganha: 100 × 2.0 = 200 moedas
```

**Derrota:**
```
Aposta: 100 moedas
Alvo: 5.0x
Crash: 2.18x 💥

Você perde: 100 moedas
```

**Níveis de Risco:**
- 🟢 **Baixo Risco** (< 1.5x): ~67% chance, ganho pequeno
- 🟡 **Risco Moderado** (1.5x - 2.0x): ~50% chance, ganho médio
- 🟠 **Alto Risco** (2.0x - 5.0x): ~20-40% chance, ganho alto
- 🔴 **Risco Extremo** (> 5.0x): < 20% chance, ganho massivo

**Dicas:**
- 💡 Multiplicadores baixos são mais seguros
- 🎲 Crashes altos (>10x) são muito raros
- 📊 A média de crash é ~2.0x

---

### 🎡 Double
**Roleta de cores - Vermelho, Preto ou Branco**

```
/double 100 vermelho
/double 100 preto
/double 100 branco
```

**Parâmetros:**
- `valor`: Aposta (mínimo 10 moedas)
- `cor`: vermelho, preto ou branco

**Probabilidades e Pagamentos:**

| Cor | Probabilidade | Pagamento | Descrição |
|-----|---------------|-----------|-----------|
| 🔴 Vermelho | 46.7% (7/15) | 2x | Quase metade |
| ⚫ Preto | 46.7% (7/15) | 2x | Quase metade |
| ⚪ Branco | 6.7% (1/15) | 14x | Raro! |

**Exemplos:**

**Vermelho/Preto:**
```
Aposta: 100 em vermelho
Resultado: 🔴 Vermelho
Ganho: 100 × 2 = 200 moedas
```

**Branco (Jackpot):**
```
Aposta: 100 em branco
Resultado: ⚪ Branco!
Ganho: 100 × 14 = 1.400 moedas! 🎉
```

**Recursos:**
- 📊 Vê os últimos 10 resultados
- 🎭 Animação da roleta girando
- 💰 Branco é difícil mas paga muito!

**Dicas:**
- 🎯 Vermelho/Preto = Jogo seguro (quase 50/50)
- 💎 Branco = Alto risco, alta recompensa
- 📈 Use os resultados anteriores (mas lembre: cada giro é independente!)

---

### 💣 Mines
**Campo minado - revele tiles e aumente o multiplicador**

```
/mines 100
/mines 100 medio
/mines 100 dificil
/mines 100 extremo
```

**Parâmetros:**
- `valor`: Aposta (mínimo 10 moedas)
- `dificuldade`: facil, medio, dificil, extremo (opcional, padrão: medio)

**Dificuldades:**

| Nível | Minas | Tiles Seguros | Dificuldade |
|-------|-------|---------------|-------------|
| 🟢 Fácil | 3 | 22 | Iniciante |
| 🟡 Médio | 5 | 20 | Balanceado |
| 🟠 Difícil | 8 | 17 | Arriscado |
| 🔴 Extremo | 10 | 15 | Muito difícil |

**Como jogar:**

1. **Revelar tiles:**
```
revelar 0 0    (revela linha 0, coluna 0)
revelar 2 3    (revela linha 2, coluna 3)
```

2. **Sacar a qualquer momento:**
```
sair
```

**Grade 5x5:**
```
    0   1   2   3   4
0 [ ] [ ] [ ] [ ] [ ]
1 [ ] [ ] [ ] [ ] [ ]
2 [ ] [ ] [ ] [ ] [ ]
3 [ ] [ ] [ ] [ ] [ ]
4 [ ] [ ] [ ] [ ] [ ]
```

**Sistema de Multiplicador:**
- Cada tile seguro revelado aumenta o multiplicador
- Crescimento exponencial!
- Exemplo (Médio - 5 minas):
  - 1º tile: 1.25x
  - 2º tile: 1.56x
  - 3º tile: 1.95x
  - 5º tile: 3.05x
  - 10º tile: 9.31x
  - 15º tile: 28.4x
  - 20º tile: 86.7x (todos seguros!)

**Estratégias:**

**🛡️ Conservadora:**
```
1. Revele 2-3 tiles
2. Saia com multiplicador baixo (~1.5-2x)
3. Ganho pequeno mas seguro
```

**⚡ Moderada:**
```
1. Revele 5-7 tiles
2. Multiplicador médio (~3-5x)
3. Risco/recompensa balanceado
```

**💎 Agressiva:**
```
1. Revele 10+ tiles
2. Multiplicador alto (>10x)
3. Alto risco, recompensa massiva
```

**Exemplo de jogo:**
```
Aposta: 100 moedas (Médio)

Jogada 1: revelar 2 2
✅ Seguro! Multiplicador: 1.25x

Jogada 2: revelar 0 4
✅ Seguro! Multiplicador: 1.56x

Jogada 3: revelar 3 1
✅ Seguro! Multiplicador: 1.95x

Jogada 4: revelar 4 4
✅ Seguro! Multiplicador: 2.44x

Você digita: sair
💰 Ganho: 100 × 2.44 = 244 moedas!
```

**Dicas:**
- ⚠️ Uma mina = perde tudo
- 📊 Mais difícil = multiplicador cresce mais rápido
- 🎯 Saque cedo se estiver nervoso
- 💪 Continue para multiplicadores massivos

---

### 🎰 Slots (Caça-Níqueis)
**Slot machine clássico 3x1**

```
/slots 100
```

**Parâmetros:**
- `valor`: Aposta (mínimo 10 moedas)

**Símbolos e Multiplicadores:**

| Símbolo | Nome | 3 Iguais | 2 Iguais |
|---------|------|----------|----------|
| 🍒 | Cereja | 2x | 1x |
| 🍋 | Limão | 3x | 1.5x |
| 🍊 | Laranja | 5x | 2.5x |
| 🍇 | Uva | 8x | 4x |
| 🍉 | Melancia | 10x | 5x |
| ⭐ | Estrela | 20x | 10x |
| 💎 | Diamante | 30x | 15x |
| 🎰 | Jackpot | 50x | 25x |

**Exemplos:**

**3 Símbolos Iguais:**
```
Aposta: 100 moedas
Resultado: 💎 💎 💎
Ganho: 100 × 30 = 3.000 moedas! 🎉
```

**2 Símbolos Iguais:**
```
Aposta: 100 moedas
Resultado: 🍉 🍉 🍊
Ganho: 100 × 5 = 500 moedas
```

**Sem combinação:**
```
Aposta: 100 moedas
Resultado: 🍒 🍋 ⭐
Perda: 100 moedas 😢
```

**Dicas:**
- 🎰 Jackpot (3x 🎰) = 50x sua aposta!
- 💎 Diamantes são raros mas valem muito
- 🍒 Cerejas são comuns mas pagam pouco

---

### 🎲 Roleta Europeia
**Roleta clássica com múltiplos tipos de aposta**

```
/roleta 100 numero 17
/roleta 100 cor vermelho
/roleta 100 paridade par
/roleta 100 altura baixo
```

**Parâmetros:**
- `valor`: Aposta (mínimo 10 moedas)
- `tipo`: numero, cor, paridade, altura
- `aposta`: Depende do tipo (veja abaixo)

**Tipos de Aposta:**

#### 1️⃣ Número Específico
```
/roleta 100 numero 17
```
- Escolha: 0 a 36
- Pagamento: 35x
- Probabilidade: 2.7% (1/37)
- **Maior pagamento!**

#### 🔴 Cor
```
/roleta 100 cor vermelho
/roleta 100 cor preto
```
- Escolha: vermelho ou preto
- Pagamento: 2x
- Probabilidade: 48.6% (18/37)
- **Quase 50/50**

**Números Vermelhos:** 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36

**Números Pretos:** 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35

#### ⚖️ Paridade
```
/roleta 100 paridade par
/roleta 100 paridade impar
```
- Escolha: par ou impar
- Pagamento: 2x
- Probabilidade: 48.6% (18/37)
- **Quase 50/50** (0 não conta)

#### 📊 Altura
```
/roleta 100 altura baixo
/roleta 100 altura alto
```
- **Baixo:** 1-18
- **Alto:** 19-36
- Pagamento: 2x
- Probabilidade: 48.6% (18/37)

**Exemplos:**

**Número Específico (Jackpot):**
```
Aposta: 100 em número 17
Resultado: 🎰 17 🔴
Ganho: 100 × 35 = 3.500 moedas! 🎉
```

**Cor:**
```
Aposta: 100 em vermelho
Resultado: 🎰 23 🔴
Ganho: 100 × 2 = 200 moedas
```

**Dicas:**
- 🎯 Número = Alto risco, pagamento massivo
- 🎲 Cor/Paridade/Altura = Mais seguro, pagamento 2x
- 🟢 Zero (0) = Casa ganha em cor/paridade/altura

---

### 🎲 Dados
**Jogue dados com diferentes modos de aposta**

```
/dados 100 acima
/dados 100 abaixo
/dados 100 sete
/dados 100 alto
/dados 100 baixo
/dados 100 6
```

**Parâmetros:**
- `valor`: Aposta (mínimo 10 moedas)
- `tipo`: acima, abaixo, sete, alto, baixo, ou número (1-6)

**Modos de Jogo:**

#### 📈 Acima/Abaixo (2 dados)
```
/dados 100 acima    (soma > 7)
/dados 100 abaixo   (soma < 7)
```
- Pagamento: 2x
- Probabilidade: ~42% cada

**Possibilidades:**
- Acima (8-12): 15 combinações de 36
- Sete (7): 6 combinações de 36
- Abaixo (2-6): 15 combinações de 36

#### 🎯 Sete (2 dados)
```
/dados 100 sete     (soma = 7)
```
- Pagamento: 5x
- Probabilidade: 16.7% (6/36)
- **Alto risco, alta recompensa!**

#### ⬆️ Alto/Baixo (1 dado)
```
/dados 100 alto     (4, 5 ou 6)
/dados 100 baixo    (1, 2 ou 3)
```
- Pagamento: 2x
- Probabilidade: 50% (3/6)

#### 🔢 Número Específico (1 dado)
```
/dados 100 1
/dados 100 6
```
- Escolha: 1, 2, 3, 4, 5 ou 6
- Pagamento: 6x
- Probabilidade: 16.7% (1/6)

**Exemplos:**

**Acima:**
```
Aposta: 100 em acima
Dados: 🎲 4 + 🎲 6 = 10
Ganho: 100 × 2 = 200 moedas ✅
```

**Sete:**
```
Aposta: 100 em sete
Dados: 🎲 3 + 🎲 4 = 7
Ganho: 100 × 5 = 500 moedas! 🎉
```

**Número Específico:**
```
Aposta: 100 em 6
Dado: 🎲 6
Ganho: 100 × 6 = 600 moedas! 🎲
```

**Dicas:**
- 🎯 Alto/Baixo = Mais seguro (50/50)
- 🎲 Acima/Abaixo = Levemente menos que 50/50
- 💎 Sete = Difícil mas paga 5x
- ⭐ Número específico = Muito difícil, paga 6x

---

### 🃏 Blackjack (21)
**Jogo de cartas clássico contra o dealer**

```
/blackjack 100
```

**Parâmetros:**
- `valor`: Aposta (mínimo 10 moedas)

**Como jogar:**

1. Você e o dealer recebem 2 cartas
2. Você vê suas 2 cartas e 1 carta do dealer
3. Use as reações para decidir:
   - ⬇️ **HIT** - Pedir mais uma carta
   - 🛑 **STAND** - Parar e manter suas cartas

**Valores das Cartas:**
- Números (2-10): Valor nominal
- Valete (J), Dama (Q), Rei (K): 10 pontos
- Ás (A): 1 ou 11 (o que for melhor)

**Objetivo:**
- Chegar mais perto de 21 que o dealer
- Não ultrapassar 21 (bust = perda automática)

**Regras do Dealer:**
- Para em 17 ou mais
- Continua pedindo em 16 ou menos

**Resultados:**

| Resultado | Pagamento | Descrição |
|-----------|-----------|-----------|
| 🎉 Blackjack Natural | 2.5x | A + 10/J/Q/K (primeiras 2 cartas) |
| ✅ Vitória | 2x | Maior que dealer sem bust |
| 🤝 Empate | 1x | Mesma pontuação (devolve aposta) |
| 💥 Bust | 0x | Ultrapassou 21 |
| ❌ Derrota | 0x | Dealer ganhou |

**Exemplos:**

**Blackjack Natural:**
```
Aposta: 100 moedas
Suas cartas: A♠️ K♥️ (21!)
Ganho: 100 × 2.5 = 250 moedas! 🎉
```

**Vitória Normal:**
```
Aposta: 100 moedas
Você: 19 pontos
Dealer: 17 pontos
Ganho: 100 × 2 = 200 moedas ✅
```

**Bust:**
```
Aposta: 100 moedas
Suas cartas: K♠️ 7♥️ 8♣️ = 25 (Bust!)
Perda: 100 moedas 💥
```

**Estratégia Básica:**

**Quando pedir carta (HIT):**
- Você tem 11 ou menos (impossível bust)
- Você tem 12-16 e dealer mostra 7-Ás
- Você tem Ás suave (Ás contado como 11)

**Quando parar (STAND):**
- Você tem 17 ou mais
- Você tem 13-16 e dealer mostra 2-6
- Você está satisfeito com sua mão

**Dicas:**
- 🎯 Dealer para em 17
- 💡 Ás é flexível (1 ou 11)
- ⚠️ Mais de 21 = Bust automático
- 🃏 Blackjack natural paga 2.5x!

---

## 🎉 Comandos Divertidos

### 😂 Piada
**Conta uma piada aleatória**

```
/piada
/joke
```

- 30+ piadas de programação e tecnologia
- Piadas brasileiras com humor local
- Sempre uma surpresa diferente!

---

### 🧠 Trivia / Quiz
**Responda perguntas e ganhe moedas!**

```
/trivia
/quiz
```

**Como funciona:**
1. O bot faz uma pergunta
2. Você tem 4 opções (A, B, C, D)
3. Clique na reação correta
4. Resposta certa = +50 moedas! 🪙

**Temas:**
- Geografia
- História
- Ciência
- Tecnologia
- Cultura Geral
- Curiosidades

**Recompensa:**
- ✅ Acertou: +50 moedas
- ❌ Errou: Nada (mas aprende algo novo!)

**Dicas:**
- 📚 Mais de 100 perguntas diferentes
- 🔄 Nunca repete até esgotar todas
- 🎓 Aprenda enquanto ganha moedas!

---

### 🔮 Bola Mágica 8
**Pergunte qualquer coisa e receba uma resposta mística**

```
/8ball Vou ganhar no crash hoje?
/8ball Devo apostar tudo?
```

**Parâmetros:**
- `pergunta`: Qualquer pergunta (sim/não funciona melhor)

**Tipos de Resposta:**
- ✅ Positivas (certeza absoluta, com certeza, sim)
- ⚠️ Neutras (talvez, não posso prever, pergunte depois)
- ❌ Negativas (definitivamente não, não conte com isso)

**Exemplos:**
```
Você: /8ball Vou ganhar no tigrinho?
Bot: 🔮 Com certeza!

Você: /8ball Devo fazer all-in?
Bot: 🔮 Melhor não contar com isso...
```

---

### 📊 Enquete
**Cria votação com tempo limitado**

```
/enquete 5 "Melhor jogo?" "Tigrinho" "Crash" "Mines"
```

**Parâmetros:**
- `minutos`: Duração (1-60 minutos)
- `pergunta`: Sua pergunta (entre aspas)
- `opcoes`: 2 ou mais opções (cada uma entre aspas)

**Exemplo completo:**
```
/enquete 10 "Qual jogo paga mais?" "Tigrinho 🐅" "Crash 🚀" "Mines 💣" "Blackjack 🃏"
```

**O bot mostra:**
- ⏰ Tempo restante
- 📊 Contagem em tempo real
- 🎯 Total de votos

**Após o tempo:**
- 🏆 Mostra resultado final
- 👑 Destaca a opção vencedora
- 📈 Porcentagem de cada opção

---

## 📋 Comandos Úteis

### `/ajuda` ou `/help`
Mostra lista completa de comandos

### `/jogos`
Lista todos os jogos disponíveis com descrições

---

## 💡 Dicas Gerais

### 🎯 Gestão de Banca
- Nunca aposte mais de 10% do seu saldo
- Use `/saldo` para acompanhar seu progresso
- Pegue o `/diario` todos os dias

### 🎲 Estratégias
- **Conservador**: Apostas baixas, jogos seguros (Double vermelho/preto)
- **Moderado**: Apostas médias, risco equilibrado (Crash 2x, Slots)
- **Agressivo**: Apostas altas, risco extremo (Tigrinho, Mines difícil)

### 🏆 Conquistas
- Jogue diferentes jogos para desbloquear conquistas
- Conquistas dão bônus de moedas
- Use `/conquistas` para ver seu progresso

### 💰 Como Ganhar Moedas
1. **Diário**: 100-200 moedas/dia (GRÁTIS!)
2. **Jogos**: Apostando e ganhando
3. **Conquistas**: Recompensas por milestones
4. **Trivia**: 50 moedas por resposta certa

### ⚠️ Jogo Responsável
- É apenas diversão! Não aposte moedas que você não pode perder
- Se estiver em sequência de derrotas, faça uma pausa
- Use `/historico` para acompanhar ganhos/perdas

---

## 🆘 Precisa de Ajuda?

**Comandos não funcionando?**
- Verifique se está usando o prefixo correto (`/`)
- Veja se tem saldo suficiente (`/saldo`)
- Use `/ajuda` para ver sintaxe correta

**Dúvidas sobre probabilidades?**
- Cada jogo tem sua matemática
- Jogos mais difíceis pagam mais
- "A casa sempre tem vantagem" (como cassinos reais)

**Quer sugerir novos jogos?**
- Fale com os administradores do servidor!

---

## 🎊 Boa Sorte!

**Lembre-se:**
- 🍀 Sorte ajuda, mas gestão de banca é chave
- 🎯 Jogue por diversão, não por necessidade
- 🏆 Conquistas valem a pena!
- 💰 Colete seu diário TODOS OS DIAS!

**Divirta-se jogando! 🎮🎰🎲**

---

<p align="center">
  <b>Bot Macacolândia</b> - Onde a diversão nunca para! 🐒
</p>
