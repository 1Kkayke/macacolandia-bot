"""Double (Color Betting) casino game implementation"""

import random
from typing import Tuple


class DoubleGame:
    """
    Double game - A simple color betting game
    Bet on Red, Black, or White
    Red/Black pays 2x, White pays 14x
    """
    
    # Color definitions with their probabilities
    COLORS = {
        'vermelho': {'emoji': '🔴', 'weight': 7, 'multiplier': 2.0, 'name': 'Vermelho'},
        'preto': {'emoji': '⚫', 'weight': 7, 'multiplier': 2.0, 'name': 'Preto'},
        'branco': {'emoji': '⚪', 'weight': 1, 'multiplier': 14.0, 'name': 'Branco'},
    }
    
    # Recent results history (for display)
    history = []
    MAX_HISTORY = 10
    
    @staticmethod
    def spin() -> str:
        """
        Spin the color wheel
        Returns the color that landed (as key name)
        """
        colors = []
        weights = []
        
        for color_key, data in DoubleGame.COLORS.items():
            colors.append(color_key)
            weights.append(data['weight'])
        
        result = random.choices(colors, weights=weights, k=1)[0]
        
        # Add to history
        DoubleGame.history.append(result)
        if len(DoubleGame.history) > DoubleGame.MAX_HISTORY:
            DoubleGame.history.pop(0)
        
        return result
    
    @staticmethod
    def check_win(result: str, bet_color: str) -> Tuple[bool, float]:
        """
        Check if bet won
        
        Args:
            result: The color that was spun
            bet_color: The color that was bet on
        
        Returns:
            (won, multiplier)
        """
        bet_color_lower = bet_color.lower()
        
        # Normalize color names
        color_aliases = {
            'red': 'vermelho',
            'black': 'preto',
            'white': 'branco',
            'r': 'vermelho',
            'b': 'preto',
            'w': 'branco',
        }
        
        bet_color_normalized = color_aliases.get(bet_color_lower, bet_color_lower)
        
        if bet_color_normalized not in DoubleGame.COLORS:
            # Invalid color
            return False, 0.0
        
        if result == bet_color_normalized:
            multiplier = DoubleGame.COLORS[result]['multiplier']
            return True, multiplier
        else:
            return False, 0.0
    
    @staticmethod
    def format_result(result: str) -> str:
        """Format the result for display"""
        data = DoubleGame.COLORS[result]
        return f"{data['emoji']} **{data['name']}**"
    
    @staticmethod
    def format_wheel_animation() -> str:
        """Create a spinning wheel animation frame"""
        # Random sequence of colors for animation
        colors = list(DoubleGame.COLORS.keys())
        sequence = [random.choice(colors) for _ in range(7)]
        
        emojis = [DoubleGame.COLORS[c]['emoji'] for c in sequence]
        return ' → '.join(emojis)
    
    @staticmethod
    def format_history() -> str:
        """Format recent results history"""
        if not DoubleGame.history:
            return 'Sem histórico ainda'
        
        emojis = [DoubleGame.COLORS[color]['emoji'] for color in DoubleGame.history]
        return ' '.join(emojis[-10:])  # Show last 10
    
    @staticmethod
    def get_color_info() -> str:
        """Get information about color probabilities and payouts"""
        info = []
        for color_key, data in DoubleGame.COLORS.items():
            total_weight = sum(c['weight'] for c in DoubleGame.COLORS.values())
            probability = (data['weight'] / total_weight) * 100
            info.append(
                f"{data['emoji']} **{data['name']}**: "
                f"{data['multiplier']:.0f}x ({probability:.1f}%)"
            )
        return '\n'.join(info)
    
    @staticmethod
    def validate_color(color: str) -> bool:
        """Check if color name is valid"""
        color_lower = color.lower()
        
        color_aliases = {
            'red': 'vermelho',
            'black': 'preto',
            'white': 'branco',
            'r': 'vermelho',
            'b': 'preto',
            'w': 'branco',
            'vermelho': 'vermelho',
            'preto': 'preto',
            'branco': 'branco',
        }
        
        return color_lower in color_aliases
