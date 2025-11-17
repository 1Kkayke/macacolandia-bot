"""Casino games module"""

from .roulette import RouletteGame
from .slots import SlotsGame
from .dice import DiceGame
from .blackjack import BlackjackGame
from .tigrinho import TigrinhoGame
from .mines import MinesGame
from .crash import CrashGame
from .double import DoubleGame
from .coinflip import CoinFlipGame
from .wheel import WheelGame
from .keno import KenoGame
from .plinko import PlinkoGame
from .baccarat import BaccaratGame
from .hilo import HiLoGame
from .limbo import LimboGame
from .tower import TowerGame
from .scratch import ScratchCardGame
from .videopoker import VideoPokerGame

__all__ = [
    'RouletteGame',
    'SlotsGame',
    'DiceGame',
    'BlackjackGame',
    'TigrinhoGame',
    'MinesGame',
    'CrashGame',
    'DoubleGame',
    'CoinFlipGame',
    'WheelGame',
    'KenoGame',
    'PlinkoGame',
    'BaccaratGame',
    'HiLoGame',
    'LimboGame',
    'TowerGame',
    'ScratchCardGame',
    'VideoPokerGame'
]
