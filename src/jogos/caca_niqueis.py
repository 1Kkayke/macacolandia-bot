"""Implementação do jogo de caça-níqueis"""

import random
from typing import Tuple, List


class JogoCacaNiqueis:
    """Jogo de caça-níqueis com 3 rolos"""
    
    # Símbolos do caça-níqueis com seus pesos (maior = mais comum)
    SIMBOLOS = {
        '🍒': {'peso': 35, 'valor': 2},    # Cereja - comum, valor baixo
        '🍋': {'peso': 30, 'valor': 3},    # Limão
        '🍊': {'peso': 25, 'valor': 4},    # Laranja
        '🍇': {'peso': 20, 'valor': 5},    # Uva
        '🍉': {'peso': 15, 'valor': 7},    # Melancia
        '⭐': {'peso': 10, 'valor': 10},   # Estrela
        '💎': {'peso': 5, 'valor': 20},    # Diamante - raro, valor alto
        '🎰': {'peso': 3, 'valor': 50},    # Jackpot - muito raro
    }
    
    @staticmethod
    def girar() -> List[str]:
        """Gira o caça-níqueis (3 rolos)"""
        simbolos = []
        pesos = []
        
        for simbolo, dados in JogoCacaNiqueis.SIMBOLOS.items():
            simbolos.append(simbolo)
            pesos.append(dados['peso'])
        
        # Escolhe 3 símbolos
        resultado = random.choices(simbolos, weights=pesos, k=3)
        return resultado
    
    @staticmethod
    def calcular_ganho(rolos: List[str]) -> Tuple[bool, float, str]:
        """
        Calcula os ganhos do resultado dos rolos
        Retorna: (ganhou, multiplicador, descricao)
        """
        # Verifica 3 iguais
        if rolos[0] == rolos[1] == rolos[2]:
            simbolo = rolos[0]
            multiplicador = JogoCacaNiqueis.SIMBOLOS[simbolo]['valor']
            return True, float(multiplicador), f'🎉 JACKPOT! 3x {simbolo}'
        
        # Verifica 2 iguais
        if rolos[0] == rolos[1] or rolos[1] == rolos[2] or rolos[0] == rolos[2]:
            # Obtém o símbolo correspondente
            if rolos[0] == rolos[1]:
                simbolo = rolos[0]
            elif rolos[1] == rolos[2]:
                simbolo = rolos[1]
            else:
                simbolo = rolos[0]
            
            multiplicador = JogoCacaNiqueis.SIMBOLOS[simbolo]['valor'] * 0.5
            return True, multiplicador, f'✨ 2x {simbolo}'
        
        # Sem combinação
        return False, 0.0, 'Sem combinação'
    
    @staticmethod
    def formatar_rolos(rolos: List[str]) -> str:
        """Formata rolos para exibição"""
        return f"[ {rolos[0]} | {rolos[1]} | {rolos[2]} ]"
