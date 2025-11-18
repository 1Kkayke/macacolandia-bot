# 🦹 Sistema de Roubo - Comando /roubar

## 💰 Como Funciona

O comando `/roubar` permite que você tente roubar moedas de outros jogadores, mas eles podem se defender!

### 🎯 Uso Básico

```
/roubar @usuario
/rob @usuario
/steal @usuario
/heist @usuario
```

---

## ⚔️ Mecânica do Jogo

### 1️⃣ **Iniciando o Roubo**

Quando você tenta roubar alguém:
- O bot sorteia **5-15% do saldo da vítima** (mínimo 100 moedas)
- Um **desafio aleatório** é gerado
- A vítima tem **15 segundos** para defender

### 2️⃣ **Tipos de Desafio**

O alvo precisa responder corretamente um dos 4 tipos de desafio:

#### 🧮 Matemática Rápida (Fácil)
```
Exemplo: Quanto é: 23 + 47?
Resposta: 70
```
- Somas, subtrações ou multiplicações simples
- Números de 2 dígitos

#### 🎯 Encontre o Emoji (Médio)
```
Exemplo: Encontre a posição do 🍓:
🍎 🍊 🍋 🍓 🍉 🍇 🥝 🍒 🍑
(Digite 1-9)
Resposta: 4
```
- Encontre o emoji específico na sequência
- Digite a posição (1 a 9)

#### 🔢 Sequência (Médio)
```
Exemplo: Complete a sequência:
5 → 10 → 15 → 20 → ?
Resposta: 25
```
- Progressões aritméticas
- Multiplicações
- Padrões crescentes

#### 📝 Palavra Embaralhada (Difícil)
```
Exemplo: Desembaralhe a palavra 🎰:
CNSISAO
Resposta: CASSINO
```
- Palavras relacionadas ao jogo embaralhadas
- Palavras como: ROUBO, MOEDA, JOGO, CASSINO, etc.

### 3️⃣ **Resultados Possíveis**

#### ✅ DEFESA BEM SUCEDIDA
**Se a vítima responder CORRETAMENTE:**
- ✅ A vítima **protege suas moedas**
- 💸 O ladrão paga **10% do seu saldo** como multa (máximo = valor que ia roubar)
- 💰 A multa vai para a vítima como recompensa

**Exemplo:**
```
🛡️ DEFESA BEM SUCEDIDA!
João defendeu com sucesso!

✅ Resposta Correta: 25
💸 Penalidade: Pedro pagou 500 🪙 de multa!
```

#### 💰 ROUBO BEM SUCEDIDO
**Se a vítima ERRAR ou NÃO RESPONDER a tempo:**
- 💰 O ladrão **rouba as moedas**
- 📉 A vítima **perde o valor**
- ⏰ Ladrão entra em **cooldown de 5 minutos**

**Exemplo:**
```
💰 ROUBO BEM SUCEDIDO!
Pedro levou na malandragem de João!

❌ Resposta Errada
Você disse: 24
Correto era: 25

💰 Lucro do Ladrão: +1.500 🪙
```

---

## 📋 Requisitos

### Para Roubar:
- ✅ Você precisa ter pelo menos **100 moedas**
- ✅ Alvo precisa ter pelo menos **500 moedas**
- ✅ Não pode estar em cooldown (5 minutos entre roubos)
- ❌ Não pode roubar bots
- ❌ Não pode roubar você mesmo

### Valores Roubados:
- **Mínimo:** 100 moedas
- **Máximo:** 15% do saldo da vítima
- **Faixa:** 5% a 15% do saldo do alvo

---

## ⏰ Cooldown

Após um roubo **bem sucedido**, você precisa esperar:
- ⏰ **5 minutos** antes de tentar roubar novamente
- Se a defesa funcionar, você **não** entra em cooldown (mas perde a multa!)

---

## 💡 Estratégias

### 👨‍💼 Para Ladrões:
- 🎯 Mire em jogadores com saldo alto (mais lucro)
- ⏰ Escolha horários que o alvo possa estar AFK
- 📊 Observe quem é bom em desafios antes de roubar
- 💰 Tenha saldo para pagar multa se falhar

### 🛡️ Para Vítimas:
- ⚡ Responda RÁPIDO (15 segundos)
- 🧠 Matemática é o desafio mais fácil
- 📝 Tenha cuidado com palavras embaralhadas
- 💡 Use calculadora se precisar (mas seja rápido!)
- ⌨️ Digite apenas a resposta, sem texto extra

---

## 📊 Estatísticas

### Dificuldades dos Desafios:

| Desafio | Dificuldade | Taxa de Sucesso Estimada |
|---------|-------------|--------------------------|
| 🧮 Matemática | Fácil | ~80% |
| 🎯 Emoji | Média | ~60% |
| 🔢 Sequência | Média | ~50% |
| 📝 Palavra | Difícil | ~40% |

### Rentabilidade:

**Roubo bem sucedido:**
- Lucro: 5-15% do saldo da vítima
- Risco: 10% do SEU saldo se falhar

**Exemplo de cálculo:**
```
Vítima tem: 10.000 🪙
Você rouba: 1.500 🪙 (15%)

Se falhar e pagar multa:
Sua multa: 10% do seu saldo
```

---

## 🎭 Mensagens Variadas

O bot usa mensagens aleatórias para tornar cada roubo único:

### 💰 Sucesso:
- "conseguiu roubar"
- "surrupiou"
- "levou na malandragem"
- "deu um golpe e pegou"
- E mais...

### 🛡️ Defesa:
- "defendeu com sucesso"
- "botou o ladrão pra correr"
- "meteu o dedo na cara do ladrão"
- "salvou suas moedas"
- E mais...

### ❌ Falha:
- "foi pego tentando roubar"
- "pisou na bola"
- "tomou na cabeça"
- E mais...

---

## ⚠️ Avisos Importantes

1. **Não é griefing:** É parte do jogo! Roubar é uma mecânica legítima.
2. **Defesa é possível:** Sempre há chance de defender se você for rápido.
3. **Cooldown existe:** Não dá pra farmar roubando o tempo todo.
4. **Multa é pesada:** 10% do SEU saldo se falhar na tentativa.
5. **Mínimos existem:** Não dá pra roubar quem tem pouco dinheiro.

---

## 🎯 Exemplos Práticos

### Exemplo 1: Roubo Bem Sucedido
```
Jogador: /roubar @João

🚨 ROUBO EM ANDAMENTO! 🚨
Pedro está tentando roubar João!

💰 Em Jogo: 1.200 🪙 (uma boa grana)

🧮 DESAFIO: Matemática Rápida
Quanto é: 34 + 28?

@João responda em 15 segundos!

[João não responde a tempo]

💰 ROUBO BEM SUCEDIDO!
Pedro levou na malandragem de João!

⏰ Tempo Esgotado!
João não respondeu a tempo...

💰 Lucro do Ladrão: +1.200 🪙
💡 Resposta Correta Era: 62
```

### Exemplo 2: Defesa Bem Sucedida
```
Jogador: /roubar @Maria

🚨 ROUBO EM ANDAMENTO! 🚨
Carlos está tentando roubar Maria!

💰 Em Jogo: 2.500 🪙 (uma fortuna)

📝 DESAFIO: Palavra Embaralhada
Desembaralhe a palavra 🪙:
DAMEO

@Maria responda em 15 segundos!

[Maria responde: MOEDA]

🛡️ DEFESA BEM SUCEDIDA!
Maria defendeu com sucesso!

✅ Resposta Correta: MOEDA
💸 Penalidade: Carlos pagou 800 🪙 de multa!

Crime não compensa!
```

---

## 🏆 Dicas Profissionais

### Para Maximizar Lucros:
1. 🎯 Roube de jogadores ricos (>10.000 moedas)
2. ⏰ Tente quando o servidor estiver quieto
3. 🔄 Use o cooldown para fazer outras atividades
4. 💰 Mantenha saldo alto para pagar multas se necessário

### Para Se Defender:
1. ⚡ Fique atento quando tiver muito dinheiro
2. 🧮 Pratique matemática mental
3. 📱 Mantenha calculadora por perto
4. ⌨️ Seja RÁPIDO ao digitar
5. 🎯 Leia o desafio com atenção

---

## 🎮 Integração com Economia

O sistema de roubo está **totalmente integrado** com a economia:
- ✅ Transações registradas no histórico
- ✅ Afeta conquistas e estatísticas
- ✅ Cooldowns persistem entre sessões
- ✅ Balanço do servidor é mantido (dinheiro não é criado/destruído, apenas transferido)

---

## 🎊 Diversão Garantida!

O sistema de roubo adiciona:
- 🎲 **Risco vs Recompensa** dinâmico
- 🧠 **Desafios mentais** variados
- ⚔️ **Interação PvP** entre jogadores
- 🎭 **Momentos épicos** e engraçados
- 💰 **Nova forma** de ganhar moedas

**Boa sorte, ladrões e defensores! 🦹‍♂️🛡️**
