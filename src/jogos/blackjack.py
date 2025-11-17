"""Implementação do jogo de blackjack"""

import random
from typing import List, Tuple
from enum import Enum


class NaipeCarta(Enum):
    """Naipes das cartas"""
    COPAS = '♥️'
    OUROS = '♦️'
    PAUS = '♣️'
    ESPADAS = '♠️'


class Carta:
    """Carta de jogar"""
    
    def __init__(self, valor: str, naipe: NaipeCarta):
        self.valor = valor
        self.naipe = naipe
    
    def obter_valor(self) -> int:
        """Obtém o valor da carta para blackjack"""
        if self.valor in ['J', 'Q', 'K']:
            return 10
        elif self.valor == 'A':
            return 11  # Ases são tratados especialmente no cálculo da mão
        else:
            return int(self.valor)
    
    def __str__(self):
        return f"{self.valor}{self.naipe.value}"


class Mao:
    """Mão de blackjack"""
    
    def __init__(self):
        self.cartas: List[Carta] = []
    
    def adicionar_carta(self, carta: Carta):
        """Adiciona uma carta à mão"""
        self.cartas.append(carta)
    
    def obter_valor(self) -> int:
        """Calcula o valor da mão com tratamento de ases"""
        valor = 0
        ases = 0
        
        for carta in self.cartas:
            if carta.valor == 'A':
                ases += 1
                valor += 11
            else:
                valor += carta.obter_valor()
        
        # Ajusta para ases se estourou
        while valor > 21 and ases > 0:
            valor -= 10
            ases -= 1
        
        return valor
    
    def eh_blackjack(self) -> bool:
        """Verifica se a mão é um blackjack (21 com 2 cartas)"""
        return len(self.cartas) == 2 and self.obter_valor() == 21
    
    def estourou(self) -> bool:
        """Verifica se a mão estourou"""
        return self.obter_valor() > 21
    
    def __str__(self):
        return ' '.join([str(carta) for carta in self.cartas])


class JogoBlackjack:
    """Jogo de blackjack"""
    
    def __init__(self):
        self.baralho: List[Carta] = []
        self.mao_jogador = Mao()
        self.mao_dealer = Mao()
        self._inicializar_baralho()
    
    def _inicializar_baralho(self):
        """Inicializa um baralho padrão de 52 cartas"""
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        naipes = list(NaipeCarta)
        
        self.baralho = [Carta(valor, naipe) for naipe in naipes for valor in valores]
        random.shuffle(self.baralho)
    
    def distribuir_carta(self) -> Carta:
        """Distribui uma carta do baralho"""
        if len(self.baralho) < 10:  # Embaralha novamente se estiver acabando
            self._inicializar_baralho()
        return self.baralho.pop()
    
    def iniciar_jogo(self):
        """Inicia um novo jogo"""
        self.mao_jogador = Mao()
        self.mao_dealer = Mao()
        
        # Distribui cartas iniciais
        self.mao_jogador.adicionar_carta(self.distribuir_carta())
        self.mao_dealer.adicionar_carta(self.distribuir_carta())
        self.mao_jogador.adicionar_carta(self.distribuir_carta())
        self.mao_dealer.adicionar_carta(self.distribuir_carta())
    
    def jogador_pedir(self):
        """Jogador pede carta (pega outra carta)"""
        self.mao_jogador.adicionar_carta(self.distribuir_carta())
    
    def dealer_jogar(self):
        """Dealer joga seguindo as regras padrão (pedir até 17+)"""
        while self.mao_dealer.obter_valor() < 17:
            self.mao_dealer.adicionar_carta(self.distribuir_carta())
    
    def determinar_vencedor(self) -> Tuple[str, float]:
        """
        Determina o vencedor do jogo e o multiplicador de pagamento
        Retorna: (resultado, multiplicador)
        """
        valor_jogador = self.mao_jogador.obter_valor()
        valor_dealer = self.mao_dealer.obter_valor()
        
        # Jogador estourou
        if self.mao_jogador.estourou():
            return 'vitoria_dealer', 0.0
        
        # Blackjack do jogador
        if self.mao_jogador.eh_blackjack():
            if self.mao_dealer.eh_blackjack():
                return 'empate', 1.0  # Empate, devolve aposta
            return 'blackjack_jogador', 2.5  # Blackjack paga 3:2
        
        # Dealer estourou
        if self.mao_dealer.estourou():
            return 'vitoria_jogador', 2.0
        
        # Compara valores
        if valor_jogador > valor_dealer:
            return 'vitoria_jogador', 2.0
        elif valor_jogador < valor_dealer:
            return 'vitoria_dealer', 0.0
        else:
            return 'empate', 1.0  # Empate, devolve aposta
    
    def obter_mao_jogador_str(self) -> str:
        """Obtém a mão do jogador formatada"""
        return f"{self.mao_jogador} (Valor: {self.mao_jogador.obter_valor()})"
    
    def obter_mao_dealer_str(self, esconder_segunda: bool = False) -> str:
        """Obtém a mão do dealer formatada"""
        if esconder_segunda and len(self.mao_dealer.cartas) >= 2:
            return f"{self.mao_dealer.cartas[0]} 🂠"
        return f"{self.mao_dealer} (Valor: {self.mao_dealer.obter_valor()})"
    
    def jogador_pode_pedir(self) -> bool:
        """Verifica se o jogador pode pedir carta"""
        return not self.mao_jogador.estourou() and not self.mao_jogador.eh_blackjack()
