"""Mensagens casuais e brasileiras para o bot"""

import random


class MensagensCasuais:
    """Mensagens com gírias e palavrões brasileiros"""
    
    # Mensagens de erro
    APOSTA_MINIMA = [
        '❌ Ó parceiro, aposta mínima é 10 conto! Bora caprichar!',
        '❌ Eita porra, tem que ser no mínimo 10 moedas, mano!',
        '❌ Calma lá, chefe! Mínimo é 10 🪙!',
        '❌ Pô véi, aposta pelo menos 10 moedas aí!',
        '❌ Negativo! Tem que ser 10 moedas no mínimo, brother!',
    ]
    
    SALDO_INSUFICIENTE = [
        '❌ Tá liso, irmão! Vai ganhar umas moedas primeiro 💸',
        '❌ Quebrado demais! Sem grana pra essa aposta não',
        '❌ Porra, tá duro hein! Precisa de mais moeda aí',
        '❌ Saldo zerado! Bora conseguir mais grana antes',
        '❌ Eita, tá ralado! Sem bufunfa suficiente pra jogar',
    ]
    
    ERRO_PROCESSAR = [
        '❌ Deu ruim ao processar sua aposta, mano! Tenta de novo',
        '❌ Eita porra, bugou aqui! Tenta aí outra vez',
        '❌ Opa, deu treta pra processar! Vai de novo',
        '❌ Porra, deu erro! Tenta mais uma vez aí',
    ]
    
    ESCOLHA_INVALIDA = [
        '❌ Pô, essa escolha não rola não! Vê as opções direito',
        '❌ Eita, escolha errada aí! Olha as opções de novo',
        '❌ Ó, não é assim não! Escolhe direito, chefe',
        '❌ Rapaz, essa opção não existe! Confere aí',
    ]
    
    # Mensagens de vitória
    VITORIA = [
        '🎉 BOOOOOA CARALHO! Ganhou!',
        '🎉 PORRAAA MANO! Acertou em cheio!',
        '🎉 FODA DEMAIS! Mandou bem pra caralho!',
        '🎉 AEEEEE PORRA! Ganhou geral, monstro!',
        '🎉 QUE ISSO IRMÃO! Lucrou legal!',
        '🎉 SHOW DE BOLA! Arrebentou!',
        '🎉 PUTA QUE PARIU! Que sorte fudida!',
        '🎉 CARALHO VÉIO! Ficou rico!',
    ]
    
    VITORIA_GRANDE = [
        '🎉💰 PORRAAAAAA! GANHOU PACA! Que tacada fudida!',
        '🎉💰 MEU DEUS! Ganhou pra caralho, monstro!',
        '🎉💰 HOLY SHIT! Ficou milionário agora!',
        '🎉💰 PUTA MERDA! Que sorte absurda!',
        '🎉💰 CARALHO! Lucro monstro, maluco!',
    ]
    
    # Mensagens de derrota
    DERROTA = [
        '❌ Perdeu, fudeu mermão! F no chat',
        '❌ Deu ruim, brother! Bora de novo',
        '❌ Azarou legal hein! Foi mal',
        '❌ Porra, não deu dessa vez! Tenta outra',
        '❌ F! Perdeu tudo, parceiro',
        '❌ Eita, se fudeu! Próxima vai',
        '❌ Perdeu feio hein! Mas bora lá de novo',
    ]
    
    DERROTA_GRANDE = [
        '❌💀 CARALHO! Perdeu paca hein!',
        '❌💀 EITA PORRA! Perdeu uma grana absurda!',
        '❌💀 PUTA MERDA! Que azar fudido!',
        '❌💀 MEU DEUS! Faliu de vez!',
    ]
    
    # Mensagens de jogo em andamento
    GIRANDO = [
        '🎰 Girando essa porra...',
        '🎰 Rodando aí...',
        '🎰 Vamo ver no que dá...',
        '🎰 Segura aí que vai...',
        '🎰 Ó o giro vindo...',
    ]
    
    PROCESSANDO = [
        '⏳ Processando essa bagaça...',
        '⏳ Calma aí que tá carregando...',
        '⏳ Ó, já vai...',
        '⏳ Aguenta os 10, mano...',
    ]
    
    # Mensagens de empate
    EMPATE = [
        '🤝 Empatou! Devolvo tua grana aí',
        '🤝 Deu empate! Tá de volta a bufunfa',
        '🤝 Empatô! Fica com tua grana aí',
    ]
    
    # Mensagens de início de jogo
    INICIANDO = [
        '🎮 Bora jogar essa porra!',
        '🎮 Partiu jogo!',
        '🎮 Vai começar! Segura aí',
        '🎮 Vamo nessa!',
    ]
    
    # Mensagens de timeout
    TIMEOUT = [
        '⏰ Ó, passou do tempo! Encerrando aqui',
        '⏰ Eita, demorou demais! Fechou',
        '⏰ Tempo esgotado, chefe!',
        '⏰ Cabou o tempo, parceiro!',
    ]
    
    # Mensagens de conquista
    CONQUISTA = [
        '🏆 CARALHO! Desbloqueou uma conquista!',
        '🏆 BOOOA! Nova conquista!',
        '🏆 FODA! Conquistou mais uma!',
        '🏆 SHOW! Mais uma conquista desbloqueada!',
    ]
    
    @staticmethod
    def get_random(lista: list) -> str:
        """Retorna uma mensagem aleatória da lista"""
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
