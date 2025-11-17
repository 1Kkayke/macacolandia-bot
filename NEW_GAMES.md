# 🎰 New Casino Games Documentation

## 10 New Intuitive Casino Games Added!

This document describes the 10 new casino games added to the Macacolândia Bot. All games follow the same pattern for balance handling and error prevention.

---

## 🆕 New Games

### 1. 🪙 Coin Flip (Cara ou Coroa)
**Command:** `/coinflip <valor> <cara|coroa>`  
**Aliases:** `moeda`, `cara`, `coroa`, `flip`

The simplest game - guess heads or tails!

**How to Play:**
- Choose cara (heads) or coroa (tails)
- Place your bet
- Win 2x your bet if correct

**Example:** `/coinflip 100 cara`

---

### 2. 🎡 Wheel of Fortune (Roda da Fortuna)
**Command:** `/wheel <valor>`  
**Aliases:** `roda`, `fortune`

Spin the wheel and win prizes!

**Prize Multipliers:**
- 0x - Lost
- 0.5x - Half back
- 1.2x - +20%
- 1.5x - +50%
- 2.0x - Double
- 3.0x - Triple
- 5.0x - 5x
- 10.0x - 10x (rare!)

**Example:** `/wheel 100`

---

### 3. 🎯 Plinko
**Command:** `/plinko <valor> [risco]`  
**Aliases:** `pl`

Drop a ball through pegs to land in prize slots!

**Risk Levels:**
- **baixo** - Stable multipliers (0.5x - 2.0x)
- **medio** - Balanced (0.3x - 4.0x)
- **alto** - High risk/reward (0.2x - 10.0x)

**Example:** `/plinko 100 alto`

---

### 4. 🎲 Limbo
**Command:** `/limbo <valor> <multiplicador_alvo>`  
**Aliases:** `lb`

Set a target multiplier - if the result is higher, you win!

**How it Works:**
- Choose your target multiplier (1.01x - 1000x)
- A random result is generated
- If result ≥ target, you win the target multiplier
- Higher targets = lower chance but bigger wins

**Risk Levels:**
- < 2.0x: Low Risk 🟢
- 2.0x - 5.0x: Medium Risk 🟡
- 5.0x - 10.0x: High Risk 🟠
- > 10.0x: Extreme Risk 🔴

**Examples:**
- `/limbo 100 2.0` - 50% chance, 2x payout
- `/limbo 100 10.0` - ~10% chance, 10x payout

---

### 5. 🎫 Scratch Card (Raspadinha)
**Command:** `/scratch <valor>`  
**Aliases:** `raspadinha`, `sc`

Instant win scratch card game!

**Prizes:**
- ❌ Lost (0x)
- 💸 Half (0.5x)
- 🤝 Tie (1.0x)
- 💰 Double (2x)
- 💎 Triple (3x)
- 🌟 5x
- ⭐ 10x
- 🎊 25x
- 🎰 JACKPOT! (100x)

**Example:** `/scratch 100`

---

### 6. 🎱 Keno
**Command:** `/keno <valor> <num1> <num2> ...`  
**Aliases:** `kn`

Pick 1-10 numbers from 1-40, then 10 numbers are drawn!

**How to Play:**
1. Choose 1 to 10 numbers between 1 and 40
2. 10 numbers will be drawn
3. Match numbers to win!

**Payout Examples:**
- Pick 5 numbers:
  - 3 matches = 2x
  - 4 matches = 8x
  - 5 matches = 40x
- Pick 10 numbers:
  - 6 matches = 3x
  - 7 matches = 10x
  - 8 matches = 30x
  - 9 matches = 100x
  - 10 matches = 500x JACKPOT!

**Example:** `/keno 100 5 12 23 34 40`

---

### 7. 🎴 Baccarat
**Command:** `/baccarat <valor> <jogador|banca|empate>`  
**Aliases:** `bac`

Classic casino card game - bet on Player, Banker, or Tie!

**Bet Types:**
- **jogador** (player) - 2.0x payout
- **banca** (banker) - 1.95x payout (5% commission)
- **empate** (tie) - 9.0x payout

**How Cards Work:**
- Aces = 1 point
- 2-9 = Face value
- 10, J, Q, K = 0 points
- Only last digit of total counts (e.g., 15 = 5)

**Example:** `/baccarat 100 jogador`

---

### 8. 🎴 Hi-Lo Card
**Command:** `/hilo <valor> <alto|baixo|igual>`  
**Aliases:** `highlow`, `hl`

Guess if the next card is higher, lower, or equal!

**Payouts:**
- **alto** (higher) - 2x
- **baixo** (lower) - 2x
- **igual** (same) - 14x

The game shows you odds based on the current card!

**Example:** `/hilo 100 alto`

---

### 9. 🗼 Tower
**Command:** `/tower <valor> [dificuldade]`  
**Aliases:** `torre`, `tw`

Climb the tower by choosing safe tiles - interactive game!

**Difficulties:**
- **facil** - 8 levels, 2/3 tiles safe
- **medio** - 12 levels, 2/3 tiles safe
- **dificil** - 10 levels, 2/4 tiles safe
- **extremo** - 12 levels, 1/4 tiles safe

**How to Play:**
1. Each level has 3-4 tiles
2. Choose a tile number (0, 1, 2, or 3)
3. If safe, climb to next level (multiplier increases!)
4. Type `sair` to cash out anytime
5. One wrong tile = game over!

**Strategy:** Higher levels = higher multiplier but more risk!

**Example:** `/tower 100 medio`

---

### 10. 🎰 Video Poker
**Command:** `/videopoker <valor>`  
**Aliases:** `poker`, `vp`

Classic Jacks or Better video poker!

**How to Play:**
1. You're dealt 5 cards
2. Choose which cards to hold (0-4)
3. Unwanted cards are replaced
4. Win based on poker hand!

**Paytable:**
- Royal Flush: 800x
- Straight Flush: 50x
- Four of a Kind: 25x
- Full House: 9x
- Flush: 6x
- Straight: 4x
- Three of a Kind: 3x
- Two Pair: 2x
- Jacks or Better: 1x

**Example:** `/videopoker 100`  
Then respond with: `0 2 4` (to hold cards at positions 0, 2, and 4)

---

## 🎯 Common Features

All games share these features:

### ✅ Balance Safety
- Minimum bet: 10 🪙
- Atomic balance operations (no double-spending)
- Balance check before game starts
- Prevents concurrent games

### ✅ User-Friendly
- Clear embed-based UI
- Animated results
- Error messages in Portuguese
- Consistent command structure

### ✅ No "Forbidden" Errors
- Games work with or without reaction permissions
- Text-based alternatives available
- Fallback mechanisms included

### ✅ Economy Integration
- Uses process_bet() for proper accounting
- Transaction history tracking
- Achievement system compatible
- Leaderboard compatible

---

## 📊 Game Comparison

| Game | Complexity | Interaction | Max Multiplier | House Edge |
|------|-----------|-------------|----------------|------------|
| Coin Flip | ⭐ | None | 2x | Low |
| Wheel | ⭐ | None | 10x | Medium |
| Scratch | ⭐ | None | 100x | Medium |
| Plinko | ⭐⭐ | Risk choice | 10x | Medium |
| Limbo | ⭐⭐ | Target choice | 1000x | Low |
| Hi-Lo | ⭐⭐ | Guess choice | 14x | Low |
| Baccarat | ⭐⭐ | Bet choice | 9x | Low |
| Keno | ⭐⭐⭐ | Number selection | 500x | High |
| Tower | ⭐⭐⭐⭐ | Interactive | Variable | Medium |
| Video Poker | ⭐⭐⭐⭐ | Interactive | 800x | Low |

---

## 🎮 Quick Start Examples

```bash
# Simple games
/coinflip 100 cara
/wheel 100
/scratch 50

# Risk-based games
/plinko 100 alto
/limbo 100 3.0

# Choice-based games
/baccarat 100 jogador
/hilo 100 alto

# Number games
/keno 100 5 10 15 20 25

# Interactive games
/tower 100 medio
/videopoker 100
```

---

## 🔧 Technical Details

### Architecture
- Each game is a separate module in `src/games/`
- Command handlers in `src/cogs/games.py`
- Follows existing game patterns
- Uses EconomyManager for all transactions

### Balance Management
```python
# All games use this pattern:
success, net_change = self.economy.process_bet(
    user_id,
    username,
    bet_amount,
    game_type,
    won,
    multiplier
)
```

### Error Prevention
- `ensure_not_playing()` - prevents concurrent games
- `check_balance()` - validates sufficient funds
- `start_game()` / `end_game()` - tracks game state
- Try/finally blocks ensure cleanup

---

## 📈 Statistics

**Total Games Available:** 18  
**Original Games:** 8  
**New Games:** 10  
**Interactive Games:** 4 (Mines, Tower, Blackjack, Video Poker)  
**Quick Games:** 14

---

Made with ❤️ for the Macacolândia community!
