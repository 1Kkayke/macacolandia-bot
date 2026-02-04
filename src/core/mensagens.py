"""Random messages for the bot"""

import random


class MensagensCasuais:
    """Random casual messages"""
    
    APOSTA_MINIMA = [
        '❌ Minimum bet is 10 coins!',
        '❌ You need to bet at least 10 coins!',
        '❌ Minimum is 10 🪙!',
    ]
    
    SALDO_INSUFICIENTE = [
        '❌ Not enough coins! Get more first 💸',
        '❌ Insufficient balance! Need more coins',
        '❌ You\'re broke! Get more coins',
    ]
    
    ERRO_PROCESSAR = [
        '❌ Error processing bet! Try again',
        '❌ Something went wrong! Try again',
    ]
    
    ESCOLHA_INVALIDA = [
        '❌ Invalid choice! Check the options',
        '❌ Wrong choice! Check options again',
    ]
    
    VITORIA = [
        '🎉 You won!',
        '🎉 Nice one! Winner!',
        '🎉 Great job! You won!',
    ]
    
    VITORIA_GRANDE = [
        '🎉💰 HUGE WIN! Amazing!',
        '🎉💰 JACKPOT! You\'re rich!',
    ]
    
    DERROTA = [
        '❌ You lost! Better luck next time',
        '❌ Didn\'t win this time! Try again',
    ]
    
    DERROTA_GRANDE = [
        '❌💀 Big loss! That hurts!',
        '❌💀 Major loss! Ouch!',
    ]
    
    GIRANDO = [
        '🎰 Spinning...',
        '🎰 Rolling...',
    ]
    
    PROCESSANDO = [
        '⏳ Processing...',
        '⏳ Loading...',
    ]
    
    EMPATE = [
        '🤝 It\'s a tie! Money returned',
        '🤝 Draw! You get your coins back',
    ]
    
    INICIANDO = [
        '🎮 Let\'s play!',
        '🎮 Game starting!',
    ]
    
    TIMEOUT = [
        '⏰ Time\'s up!',
        '⏰ Too slow! Game ended',
    ]
    
    CONQUISTA = [
        '🏆 Achievement unlocked!',
        '🏆 New achievement!',
    ]
    
    @staticmethod
    def get_random(lista: list) -> str:
        return random.choice(lista)
    
    @staticmethod
    def aposta_minima() -> str:
        return MensagensCasuais.get_random(MensagensCasuais.APOSTA_MINIMA)
    
    @staticmethod
    def saldo_insuficiente() -> str:
        return MensagensCasuais.get_random(MensagensCasuais.SALDO_INSUFICIENTE)
    
    @staticmethod
    def erro_processar() -> str:
        return MensagensCasuais.get_random(MensagensCasuais.ERRO_PROCESSAR)
    
    @staticmethod
    def escolha_invalida() -> str:
        return MensagensCasuais.get_random(MensagensCasuais.ESCOLHA_INVALIDA)
    
    @staticmethod
    def vitoria(grande: bool = False) -> str:
        if grande:
            return MensagensCasuais.get_random(MensagensCasuais.VITORIA_GRANDE)
        return MensagensCasuais.get_random(MensagensCasuais.VITORIA)
    
    @staticmethod
    def derrota(grande: bool = False) -> str:
        if grande:
            return MensagensCasuais.get_random(MensagensCasuais.DERROTA_GRANDE)
        return MensagensCasuais.get_random(MensagensCasuais.DERROTA)
    
    @staticmethod
    def girando() -> str:
        return MensagensCasuais.get_random(MensagensCasuais.GIRANDO)
    
    @staticmethod
    def processando() -> str:
        return MensagensCasuais.get_random(MensagensCasuais.PROCESSANDO)
    
    @staticmethod
    def empate() -> str:
        return MensagensCasuais.get_random(MensagensCasuais.EMPATE)
    
    @staticmethod
    def iniciando() -> str:
        return MensagensCasuais.get_random(MensagensCasuais.INICIANDO)
    
    @staticmethod
    def timeout() -> str:
        return MensagensCasuais.get_random(MensagensCasuais.TIMEOUT)
    
    @staticmethod
    def conquista() -> str:
        return MensagensCasuais.get_random(MensagensCasuais.CONQUISTA)
