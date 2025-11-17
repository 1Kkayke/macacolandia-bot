"""Implementação do jogo de roleta"""

import random
from typing import Tuple


class JogoRoleta:
    """Jogo de Roleta Europeia"""
    
    # Números da roleta com cores
    NUMEROS_VERMELHOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    NUMEROS_PRETOS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    
    @staticmethod
    def girar() -> int:
        """Gira a roleta (0-36)"""
        return random.randint(0, 36)
    
    @staticmethod
    def obter_cor(numero: int) -> str:
        """Obtém a cor de um número"""
        if numero == 0:
            return 'verde'
        elif numero in JogoRoleta.NUMEROS_VERMELHOS:
            return 'vermelho'
        else:
            return 'preto'
    
    @staticmethod
    def verificar_aposta(numero: int, tipo_aposta: str, valor_aposta: str) -> Tuple[bool, float]:
        """
        Verifica se a aposta ganhou e retorna o multiplicador
        Retorna: (ganhou, multiplicador)
        """
        tipo_aposta = tipo_aposta.lower()
        valor_aposta = valor_aposta.lower()
        
        # Número direto (número único)
        if tipo_aposta == 'numero' or tipo_aposta == 'número':
            try:
                num_aposta = int(valor_aposta)
                if numero == num_aposta:
                    return True, 35.0
            except ValueError:
                pass
            return False, 0.0
        
        # Vermelho/Preto
        if tipo_aposta == 'cor':
            cor = JogoRoleta.obter_cor(numero)
            if valor_aposta in ['vermelho', 'preto'] and valor_aposta == cor:
                return True, 2.0
            return False, 0.0
        
        # Par/Ímpar
        if tipo_aposta == 'paridade':
            if numero == 0:
                return False, 0.0
            eh_par = numero % 2 == 0
            if (valor_aposta == 'par' and eh_par) or (valor_aposta == 'impar' or valor_aposta == 'ímpar') and not eh_par:
                return True, 2.0
            return False, 0.0
        
        # Alto/Baixo
        if tipo_aposta == 'altura':
            if numero == 0:
                return False, 0.0
            if (valor_aposta == 'baixo' and 1 <= numero <= 18) or (valor_aposta == 'alto' and 19 <= numero <= 36):
                return True, 2.0
            return False, 0.0
        
        return False, 0.0
    
    @staticmethod
    def obter_tipos_aposta() -> str:
        """Obtém descrição formatada dos tipos de aposta"""
        return """
**Tipos de Aposta:**
• `numero <0-36>` - Aposta em um número específico (35x)
• `cor <vermelho/preto>` - Aposta na cor (2x)
• `paridade <par/impar>` - Aposta em par ou ímpar (2x)
• `altura <baixo/alto>` - Baixo (1-18) ou Alto (19-36) (2x)
        """
