"""Implementação do jogo de dados"""

import random
from typing import Tuple


class JogoDados:
    """Jogo simples de apostas com dados"""
    
    @staticmethod
    def rolar_dados(num_dados: int = 2) -> list:
        """Rola os dados"""
        return [random.randint(1, 6) for _ in range(num_dados)]
    
    @staticmethod
    def jogar_acima_abaixo(tipo_aposta: str, limite: int = 7) -> Tuple[bool, list, int, float]:
        """
        Joga o jogo acima/abaixo com 2 dados
        Retorna: (ganhou, dados, total, multiplicador)
        """
        dados = JogoDados.rolar_dados(2)
        total = sum(dados)
        
        tipo_aposta = tipo_aposta.lower()
        
        ganhou = False
        multiplicador = 2.0
        
        if tipo_aposta in ['over', 'acima'] and total > limite:
            ganhou = True
        elif tipo_aposta in ['under', 'abaixo'] and total < limite:
            ganhou = True
        elif tipo_aposta == 'seven' or tipo_aposta == 'sete' and total == limite:
            ganhou = True
            multiplicador = 5.0  # Pagamento maior para exatamente 7
        
        return ganhou, dados, total, multiplicador
    
    @staticmethod
    def jogar_alto_baixo(previsao: str) -> Tuple[bool, int, float]:
        """
        Joga o jogo alto/baixo com 1 dado
        Retorna: (ganhou, resultado, multiplicador)
        """
        resultado = random.randint(1, 6)
        previsao = previsao.lower()
        
        ganhou = False
        multiplicador = 2.0
        
        # Alto = 4, 5, 6 | Baixo = 1, 2, 3
        if previsao in ['high', 'alto'] and resultado >= 4:
            ganhou = True
        elif previsao in ['low', 'baixo'] and resultado <= 3:
            ganhou = True
        
        return ganhou, resultado, multiplicador
    
    @staticmethod
    def jogar_numero_especifico(numero_aposta: int) -> Tuple[bool, int, float]:
        """
        Aposta em um número específico
        Retorna: (ganhou, resultado, multiplicador)
        """
        resultado = random.randint(1, 6)
        ganhou = resultado == numero_aposta
        multiplicador = 6.0  # Pagamento 6x para número específico
        
        return ganhou, resultado, multiplicador
    
    @staticmethod
    def formatar_dados(dados: list) -> str:
        """Formata dados com emojis"""
        dados_emoji = {
            1: '⚀',
            2: '⚁',
            3: '⚂',
            4: '⚃',
            5: '⚄',
            6: '⚅'
        }
        return ' '.join([dados_emoji.get(d, '?') for d in dados])
