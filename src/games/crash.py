"""Crash casino game implementation"""

import random
from typing import Tuple


class CrashGame:
    """
    Crash game - Multiplier starts at 1.0x and increases until it crashes
    Player must cash out before the crash to win
    """
    
    @staticmethod
    def generate_crash_point() -> float:
        """
        Generate a crash point using house edge
        Uses exponential distribution for realistic crash behavior
        Average crash point is around 1.98x (house edge ~1%)
        """
        # Use inverse exponential distribution
        # This creates realistic crash behavior with occasional high multipliers
        house_edge = 0.01
        random_value = random.random()
        
        # Ensure we don't get zero or negative
        if random_value <= 0.0001:
            random_value = 0.0001
        
        crash_point = (1 - house_edge) / random_value
        
        # Cap extremely high values at 100x
        if crash_point > 100:
            crash_point = 100.0
        
        # Round to 2 decimal places
        return round(crash_point, 2)
    
    @staticmethod
    def simulate_crash(crash_point: float, target_multiplier: float = None) -> Tuple[bool, float]:
        """
        Simulate a crash game
        
        Args:
            crash_point: The point where the game will crash
            target_multiplier: Optional auto-cashout multiplier
        
        Returns:
            (won, final_multiplier) - If won, final_multiplier is the cashout point
        """
        if target_multiplier is None:
            # No auto-cashout, game crashes
            return False, crash_point
        
        if target_multiplier <= crash_point:
            # Player cashed out before crash
            return True, target_multiplier
        else:
            # Crash happened before target
            return False, crash_point
    
    @staticmethod
    def format_multiplier_animation(current: float) -> str:
        """Format multiplier for display during animation"""
        # Create visual indicator of multiplier
        bars = int(current * 2)  # 2 bars per 1.0x
        bar_str = '█' * min(bars, 20)  # Cap at 20 bars
        
        # Color emoji based on multiplier
        if current < 2.0:
            emoji = '🟢'
        elif current < 5.0:
            emoji = '🟡'
        elif current < 10.0:
            emoji = '🟠'
        else:
            emoji = '🔴'
        
        return f'{emoji} **{current:.2f}x** {bar_str}'
    
    @staticmethod
    def format_crash(crash_point: float) -> str:
        """Format crash message"""
        return f'💥 **CRASH em {crash_point:.2f}x** 💥'
    
    @staticmethod
    def get_multiplier_steps(crash_point: float, num_steps: int = 10) -> list:
        """
        Generate a list of multiplier values leading up to crash point
        Used for animation
        
        Args:
            crash_point: Where the game will crash
            num_steps: Number of animation steps
        
        Returns:
            List of multiplier values
        """
        if crash_point < 1.1:
            # Very quick crash
            return [1.0, crash_point]
        
        steps = []
        if crash_point <= 2.0:
            # Quick crash, smaller increments
            increment = (crash_point - 1.0) / num_steps
            for i in range(num_steps):
                steps.append(round(1.0 + (increment * i), 2))
        elif crash_point <= 5.0:
            # Medium crash
            for i in range(num_steps):
                progress = i / num_steps
                value = 1.0 + (crash_point - 1.0) * progress
                steps.append(round(value, 2))
        else:
            # High crash - accelerate growth
            for i in range(num_steps):
                progress = i / num_steps
                # Exponential growth for high multipliers
                value = 1.0 + (crash_point - 1.0) * (progress ** 1.5)
                steps.append(round(value, 2))
        
        return steps
    
    @staticmethod
    def get_risk_level(target: float) -> str:
        """Get risk level description based on target multiplier"""
        if target < 1.5:
            return '🟢 Baixo Risco'
        elif target < 2.0:
            return '🟡 Risco Moderado'
        elif target < 5.0:
            return '🟠 Alto Risco'
        else:
            return '🔴 Risco Extremo'
