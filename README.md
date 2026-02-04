# 🎮 Casino Bot for Discord

A Discord bot with music playback, casino games, economy system, and interactive commands.

## Features

- 🎵 **Music**: Play from YouTube, queue management, volume control
- 🎰 **Casino**: Slots, roulette, blackjack, crash, mines, and more
- 💰 **Economy**: Virtual coins, daily rewards, transfers, leaderboards
- 🏆 **Achievements**: Unlock rewards by playing
- 🎉 **Fun**: Jokes, trivia, polls, magic 8-ball

## Quick Start

### Requirements

- Python 3.8+
- FFmpeg
- Discord bot token

### Installation

```bash
# Clone the repo
git clone https://github.com/1Kkayke/macacolandia-bot.git
cd macacolandia-bot

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your DISCORD_TOKEN

# Run the bot
python run.py
```

### Docker

```bash
docker-compose up -d
```

## Commands

### Music
| Command | Description |
|---------|-------------|
| `/play <url/search>` | Play a song |
| `/pause` | Pause playback |
| `/skip` | Skip to next song |
| `/queue` | Show queue |
| `/volume <0-100>` | Set volume |

### Economy
| Command | Description |
|---------|-------------|
| `/balance` | Check your coins |
| `/daily` | Claim daily reward |
| `/transfer @user <amount>` | Send coins |
| `/ranking` | Top 10 players |
| `/achievements` | View achievements |

### Casino
| Command | Description |
|---------|-------------|
| `/slots <amount>` | Slot machine |
| `/roulette <amount> <type> <bet>` | Roulette |
| `/blackjack <amount>` | Blackjack |
| `/crash <amount> [target]` | Crash game |
| `/mines <amount> [difficulty]` | Minesweeper |
| `/coinflip <amount> <heads/tails>` | Coin flip |
| `/games` | List all games |

### Fun
| Command | Description |
|---------|-------------|
| `/joke` | Random joke |
| `/trivia` | Quiz with rewards |
| `/poll <min> "question" "opt1" "opt2"` | Create poll |
| `/8ball <question>` | Magic 8-ball |

## Project Structure

```
src/
├── bot.py          # Main entry point
├── config.py       # Configuration
├── cogs/           # Command modules
├── core/           # Core utilities
├── database/       # Data persistence
├── economy/        # Economy system
├── games/          # Casino games
├── fun/            # Fun commands
└── music/          # Music playback
```

## Troubleshooting

- **Bot doesn't connect**: Check your token in `.env`
- **Music doesn't play**: Make sure FFmpeg is installed
- **Commands don't work**: Check bot permissions in your server

## License

Open source for personal and educational use.

## Author

**1Kkayke**
