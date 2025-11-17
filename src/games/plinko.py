"""Plinko game implementation"""

import random
from typing import Tuple


class PlinkoGame:
    """Plinko ball drop game"""
    
    # Rows of pegs
    ROWS = 12
    
    # Multipliers for each slot (low, medium, high risk)
    MULTIPLIERS = {
        'baixo': [0.5, 1.0, 1.2, 1.5, 1.8, 2.0, 1.8, 1.5, 1.2, 1.0, 0.5],
        'medio': [0.3, 0.7, 1.5, 2.0, 3.0, 4.0, 3.0, 2.0, 1.5, 0.7, 0.3],
        'alto': [0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 5.0, 2.0, 1.0, 0.5, 0.2]
    }
    
    RISK_LEVELS = ['baixo', 'medio', 'alto']
    
    @staticmethod
    def validate_risk(risk: str) -> bool:
        """Validate risk level"""
        return risk.lower() in PlinkoGame.RISK_LEVELS
    
    @staticmethod
    def drop_ball(rows: int = ROWS) -> int:
        """
        Simulate ball drop through pegs
        Returns: final slot position (0 to rows)
        """
        position = 0
        
        # Each row, ball goes left or right
        for _ in range(rows):
            if random.random() < 0.5:
                position += 0
            else:
                position += 1
        
        # Normalize to slot index (0 to 10)
        slots = 11
        slot = min(int((position / rows) * slots), slots - 1)
        
        return slot
    
    @staticmethod
    def calculate_win(slot: int, risk_level: str) -> Tuple[bool, float]:
        """
        Calculate win based on slot and risk
        Returns: (won, multiplier)
        """
        risk_level = risk_level.lower()
        if risk_level not in PlinkoGame.MULTIPLIERS:
            return False, 0.0
        
        multipliers = PlinkoGame.MULTIPLIERS[risk_level]
        multiplier = multipliers[slot]
        won = multiplier > 1.0
        
        return won, multiplier
    
    @staticmethod
    def format_multipliers(risk_level: str) -> str:
        """Format multipliers for display"""
        risk_level = risk_level.lower()
        if risk_level not in PlinkoGame.MULTIPLIERS:
            return ""
        
        multipliers = PlinkoGame.MULTIPLIERS[risk_level]
        formatted = []
        for i, mult in enumerate(multipliers):
            formatted.append(f"{i}: {mult}x")
        
        return " | ".join(formatted)
    
    @staticmethod
    def format_board(slot: int, risk_level: str) -> str:
        """Format plinko board with result"""
        risk_level = risk_level.lower()
        multipliers = PlinkoGame.MULTIPLIERS.get(risk_level, PlinkoGame.MULTIPLIERS['medio'])
        
        board = "```\n"
        board += "       🎯 PLINKO\n"
        board += "       ▼\n"
        board += "      ◯\n"
        
        # Show some pegs
        for i in range(4):
            indent = "    " + "  " * i
            pegs = "◦ " * (i + 2)
            board += f"{indent}{pegs}\n"
        
        board += "\n"
        
        # Show slots with multipliers
        board += "[ "
        for i, mult in enumerate(multipliers):
            if i == slot:
                board += f">{mult}< "
            else:
                board += f"{mult} "
        board += "]\n"
        board += "```"
        
        return board
    
    @staticmethod
    def get_risk_description(risk_level: str) -> str:
        """Get risk level description"""
        descriptions = {
            'baixo': '🟢 Baixo Risco - Mais estável, menores variações',
            'medio': '🟡 Risco Médio - Balanceado entre segurança e ganhos',
            'alto': '🔴 Alto Risco - Grandes prêmios ou perdas!'
        }
        return descriptions.get(risk_level.lower(), '')
