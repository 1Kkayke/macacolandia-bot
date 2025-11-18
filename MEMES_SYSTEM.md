# 🎭 Sistema de Memes - Macacolândia Bot

## 📋 Visão Geral

Sistema completo de memes que busca imagens da internet usando a **API pública do Reddit** (sem necessidade de chave de API).

---

## 🎮 Comandos Disponíveis

### 📚 Curiosidades
- `/fact` ou `/fato` ou `/curiosidade`
  - Compartilha uma curiosidade engraçada aleatória
  - 100+ fatos divertidos sobre animais, tecnologia, história, etc.

### 😂 Memes Aleatórios
- `/randommeme` ou `/meme`
  - Envia um meme completamente aleatório
  - Busca de subreddits populares

- `/memealeatório` ou `/meme-aleatorio`
  - Outro comando para meme aleatório
  - Funciona da mesma forma que `/randommeme`

### 🔥 Memes por Categoria

- `/meme2025` ou `/meme-2025`
  - Memes da moda em 2025
  - Subreddits: r/memes, r/dankmemes, r/GenZ

- `/memedodia` ou `/meme-do-dia` ou `/dailymeme`
  - Meme do dia (cached)
  - Sempre o mesmo meme durante o dia inteiro
  - Reseta à meia-noite

- `/memedesucesso` ou `/meme-sucesso`
  - Memes motivacionais e de sucesso
  - Subreddits: r/GetMotivated, r/wholesomememes, r/MadeMeSmile

- `/memedefracasso` ou `/meme-fracasso`
  - Memes de falhas e fracassos
  - Subreddits: r/Wellthatsucks, r/facepalm, r/therewasanattempt

- `/memedetroll` ou `/meme-troll` ou `/troll`
  - Memes de trollagem
  - Subreddits: r/trollface, r/memes, r/dankmemes

- `/memedezoacao` ou `/meme-zoacao` ou `/zoeira`
  - Memes de zoação
  - Subreddits: r/ComedyCemetery, r/terriblefacebookmemes, r/shitposting

### 🇧🇷 Memes Brasileiros
- `/memebr` ou `/meme-br` ou `/memebrasil`
  - Memes brasileiros
  - Subreddits: r/brasilmemes, r/brasil, r/circojeca, r/DiretoDoZapZap

### 🏆 Top Memes
- `/topmeme` ou `/top-meme` ou `/memetop`
  - Memes mais votados de hoje
  - Ordenados por score (upvotes)

---

## 🔧 Como Funciona

### API do Reddit
```python
# URL base para buscar posts
https://www.reddit.com/r/{subreddit}/hot.json?limit=100

# Para top memes
https://www.reddit.com/r/{subreddit}/top.json?t=day&limit=50
```

### Filtragem
- ✅ Apenas imagens (`.jpg`, `.png`, `.gif`, `.webp`)
- ✅ Suporta links do Reddit (i.redd.it) e Imgur
- ❌ Filtra conteúdo NSFW automaticamente
- ✅ Retorna posts com título, URL, subreddit e score

### Cache
- **Meme do Dia**: Cached diariamente
  - Mesmo meme para todos durante o dia
  - Reseta automaticamente à meia-noite
  - Economiza requisições à API

### Subreddits Usados

**Internacionais:**
- r/memes - Memes gerais
- r/dankmemes - Memes dank/edgy
- r/me_irl - Relatable memes
- r/wholesomememes - Memes wholesome
- r/AdviceAnimals - Image macros clássicos
- r/terriblefacebookmemes - Memes ruins/cringe
- r/ComedyCemetery - Piadas ruins

**Brasileiros:**
- r/brasilmemes - Memes BR
- r/brasil - Brasil geral
- r/circojeca - Shitpost BR
- r/DiretoDoZapZap - Memes de WhatsApp

**Por Categoria:**
- Sucesso: r/GetMotivated, r/wholesomememes, r/MadeMeSmile
- Fracasso: r/Wellthatsucks, r/facepalm, r/therewasanattempt
- Troll: r/trollface, r/memes, r/dankmemes
- Zoação: r/ComedyCemetery, r/terriblefacebookmemes, r/shitposting
- 2025: r/memes, r/dankmemes, r/GenZ

---

## 📊 Estatísticas

### Curiosidades (Facts)
- **Total**: 100+ fatos engraçados
- **Categorias**: 
  - Animais (20+)
  - Tecnologia (15+)
  - Comida (10+)
  - História (10+)
  - Ciência (10+)
  - Internet/Gaming (10+)
  - Corpo Humano (10+)
  - Cultura Pop (15+)

### Subreddits
- **Total**: 15+ subreddits
- **Internacionais**: 7
- **Brasileiros**: 4
- **Por categoria**: 15+

---

## 🎨 Exemplos de Uso

```
/fact
💡 Curiosidade Aleatória
🦆 Patos têm uma corkscrew... estrutura anatômica. Sim, é estranho.

/randommeme
😂 When you realize it's Monday tomorrow
[imagem do meme]
r/memes • 15.2k ⬆️

/memedodia
📅 Meme do Dia: This is fine
[imagem do cachorro no fogo]
r/memes • Meme oficial do dia!

/memebr
🇧🇷 Calma Calabreso
[imagem brasileira]
r/brasilmemes • Meme raiz BR!
```

---

## ⚙️ Configuração

### Dependências
```bash
# Já instalado no requirements.txt
aiohttp==3.9.4
```

### Estrutura de Arquivos
```
src/
  ├── fun/
  │   └── memes.py          # MemeManager (lógica de busca)
  └── cogs/
      └── memes.py          # Cog de comandos
```

### Carregamento Automático
O bot carrega o cog automaticamente ao iniciar através do sistema de cogs.

---

## 🔒 Segurança

- ✅ **NSFW Filtering**: Todo conteúdo NSFW é automaticamente filtrado
- ✅ **User-Agent**: Requisições identificadas corretamente
- ✅ **Rate Limiting**: Respeita limites do Reddit
- ✅ **Error Handling**: Tratamento de erros de rede/API
- ✅ **Fallback**: Se falhar, sugere comando alternativo

---

## 🚀 Performance

- **Cache**: Meme do dia é cached (reduz requisições)
- **Async**: Todas as requisições são assíncronas
- **Timeout**: Sem timeout definido (usa padrão do aiohttp)
- **Typing Indicator**: Mostra "digitando..." enquanto busca

---

## 🛠️ Troubleshooting

### Erro: "Não consegui encontrar um meme"
**Causa**: Reddit API retornou erro ou sem posts com imagem
**Solução**: Tente outro comando ou aguarde alguns segundos

### Erro: Conexão falhou
**Causa**: Problema de rede ou Reddit offline
**Solução**: Verifique conexão com internet

### Memes repetidos
**Causa**: Pool limitado de posts "hot" no subreddit
**Solução**: Use `/topmeme` ou espere novos posts

---

## 📈 Futuras Melhorias

### Possíveis Adições:
1. **Mais Subreddits**: Adicionar mais fontes
2. **Favoritos**: Usuários salvarem memes favoritos
3. **Votação**: Sistema de upvote/downvote interno
4. **Histórico**: Não repetir memes já vistos
5. **Customização**: Usuários escolherem subreddits preferidos
6. **Tradução**: Traduzir títulos automaticamente
7. **Filtros**: Filtrar por idioma/país
8. **API Alternativa**: Imgflip API como backup
9. **Gifs Animados**: Suporte melhorado para GIFs
10. **Reações**: Sistema de reações aos memes

---

## 📝 Notas

- Reddit API pública tem rate limit (aprox. 60 req/min)
- Memes são buscados em tempo real (sempre atualizados)
- Qualidade das imagens depende do post original
- Subreddits brasileiros têm menos conteúdo
- Sistema não requer autenticação OAuth do Reddit

---

## ✅ Testado e Funcionando

- ✅ Busca de memes do Reddit
- ✅ Filtro NSFW
- ✅ Cache do meme do dia
- ✅ Categorias funcionais
- ✅ Memes brasileiros
- ✅ Top memes por score
- ✅ 100+ curiosidades
- ✅ Error handling robusto
- ✅ Embeds com formatação bonita
- ✅ Múltiplos aliases por comando

🎉 **Sistema pronto para uso!**
