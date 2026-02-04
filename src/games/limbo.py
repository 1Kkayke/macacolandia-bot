"""Limbo game implementation"""

import random
from typing import Tuple


class LimboGame:
    """Limbo multiplier bar game"""
    
    MIN_TARGET = 1.01
    MAX_TARGET = 1000.0
    
    @staticmethod
    def validate_target(target: float) -> bool:
        """Validate target multiplier"""
        return LimboGame.MIN_TARGET <= target <= LimboGame.MAX_TARGET
    
    @staticmethod
    def generate_result() -> float:
        """Generate a random limbo result"""
        # Generate with exponential distribution for realistic results
        # Most results will be low, with occasional high values
        
        # Use inverse transform sampling for exponential-like distribution
        r = random.random()
        
        # Adjust to favor lower multipliers
        if r < 0.5:
            # 50% chance of 1.0 - 2.0
            result = 1.0 + r * 2.0
        elif r < 0.8:
            # 30% chance of 2.0 - 10.0
            result = 2.0 + ((r - 0.5) / 0.3) * 8.0
        elif r < 0.95:
            # 15% chance of 10.0 - 100.0
            result = 10.0 + ((r - 0.8) / 0.15) * 90.0
        else:
            # 5% chance of 100.0 - 1000.0
            result = 100.0 + ((r - 0.95) / 0.05) * 900.0
        
        return round(result, 2)
    
    @staticmethod
    def check_win(result: float, target: float) -> Tuple[bool, float]:
        """
        Check if player won (result >= target)
        Returns: (won, multiplier)
        """
        won = result >= target
        multiplier = target if won else 0.0
        return won, multiplier
    
    @staticmethod
    def format_result(result: float, target: float, won: bool) -> str:
        """Format result for display"""
        if won:
            return f"✅ **{result}x** (target: {target}x) - Passed!"
        else:
            return f"❌ **{result}x** (target: {target}x) - Did not reach"
    
    @staticmethod
    def get_risk_level(target: float) -> str:
        """Get risk level description"""
        if target < 2.0:
            return "🟢 Low Risk"
        elif target < 5.0:
            return "🟡 Medium Risk"
        elif target < 10.0:
            return "🟠 High Risk"
        elif target < 50.0:
            return "🔴 Very High Risk"
        else:
            return "💀 Extreme Risk"
    
    @staticmethod
    def calculate_win_chance(target: float) -> float:
        """Calculate approximate win chance percentage"""
        # Simplified calculation based on house edge
        # Higher target = lower chance
        if target <= 1.0:
            return 99.0
        
        # Approximate: 99% / target (with house edge adjustment)
        chance = (99.0 / target)
        return min(99.0, max(0.1, chance))
    
    @staticmethod
    def format_bar(result: float, max_display: float = 20.0) -> str:
        """Format limbo bar animation"""
        # Normalize result to display range
        normalized = min(result / max_display, 1.0)
        bar_length = 20
        filled = int(normalized * bar_length)
        
        bar = "█" * filled + "░" * (bar_length - filled)
        return f"[{bar}] {result}x"
    
    @staticmethod
    def get_help_text() -> str:
        """Get help text"""
        return (
            "**How to Play Limbo:**\n"
            "1. Choose a target multiplier (e.g., 2.0x)\n"
            "2. A random result will be generated\n"
            "3. If result >= your target, you win!\n"
            "4. Higher target = bigger prize, lower chance\n\n"
            "**Examples:**\n"
            "• Target 2.0x: ~50% chance\n"
            "• Target 10.0x: ~10% chance\n"
            "• Target 100.0x: ~1% chance"
        )
