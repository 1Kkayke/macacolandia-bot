"""Wheel of Fortune game implementation"""

import random
from typing import Tuple


class WheelGame:
    """Wheel of Fortune spinning game"""
    
    # Wheel segments with multipliers and weights
    SEGMENTS = [
        {'multiplier': 0, 'label': 'Lost', 'emoji': '❌', 'weight': 25},
        {'multiplier': 0.5, 'label': 'Metade', 'emoji': '😐', 'weight': 20},
        {'multiplier': 1.2, 'label': '+20%', 'emoji': '🙂', 'weight': 18},
        {'multiplier': 1.5, 'label': '+50%', 'emoji': '😊', 'weight': 15},
        {'multiplier': 2.0, 'label': 'Dobro', 'emoji': '😄', 'weight': 12},
        {'multiplier': 3.0, 'label': 'Triplo', 'emoji': '🎉', 'weight': 7},
        {'multiplier': 5.0, 'label': 'x5', 'emoji': '🌟', 'weight': 2},
        {'multiplier': 10.0, 'label': 'x10', 'emoji': '💎', 'weight': 1},
    ]
    
    @staticmethod
    def spin() -> dict:
        """Spin the wheel and return a segment"""
        segments = WheelGame.SEGMENTS
        weights = [s['weight'] for s in segments]
        return random.choices(segments, weights=weights, k=1)[0]
    
    @staticmethod
    def calculate_win(segment: dict) -> Tuple[bool, float, str]:
        """
        Calculate win from segment
        Returns: (won, multiplier, description)
        """
        multiplier = segment['multiplier']
        won = multiplier > 0
        description = f"{segment['emoji']} {segment['label']}"
        return won, multiplier, description
    
    @staticmethod
    def format_wheel() -> str:
        """Format wheel display"""
        wheel = "🎡 Roda da Fortuna\n\n"
        for segment in WheelGame.SEGMENTS:
            wheel += f"{segment['emoji']} {segment['label']} ({segment['multiplier']}x)\n"
        return wheel
    
    @staticmethod
    def format_result(segment: dict) -> str:
        """Format result for display"""
        return f"{segment['emoji']} **{segment['label']}** ({segment['multiplier']}x)"
