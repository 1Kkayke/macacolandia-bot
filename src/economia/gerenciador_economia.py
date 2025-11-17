"""Sistema de gerenciamento de economia"""

from typing import Tuple
from src.banco_dados.gerenciador_bd import GerenciadorBancoDados


class GerenciadorEconomia:
    """Gerencia o sistema de economia do bot"""
    
    def __init__(self, bd: GerenciadorBancoDados):
        self.bd = bd
    
    def obter_saldo(self, id_usuario: str, nome_usuario: str) -> int:
        """Obtém o saldo de moedas do usuário"""
        usuario = self.bd.obter_usuario(id_usuario, nome_usuario)
        return usuario['coins']
    
    def adicionar_moedas(self, id_usuario: str, quantia: int, motivo: str = None) -> bool:
        """Adiciona moedas à conta do usuário"""
        if self.bd.atualizar_moedas(id_usuario, quantia):
            self.bd.adicionar_transacao(id_usuario, quantia, 'ganho', motivo)
            return True
        return False
    
    def remover_moedas(self, id_usuario: str, quantia: int, motivo: str = None) -> bool:
        """Remove moedas da conta do usuário"""
        if self.bd.atualizar_moedas(id_usuario, -quantia):
            self.bd.adicionar_transacao(id_usuario, -quantia, 'gasto', motivo)
            return True
        return False
    
    def transferir_moedas(self, usuario_origem: str, usuario_destino: str, quantia: int) -> Tuple[bool, str]:
        """Transfere moedas entre usuários"""
        return self.bd.transferir_moedas(usuario_origem, usuario_destino, quantia)
    
    def pode_pagar(self, id_usuario: str, nome_usuario: str, quantia: int) -> bool:
        """Verifica se o usuário pode pagar uma quantia"""
        saldo = self.obter_saldo(id_usuario, nome_usuario)
        return saldo >= quantia
    
    def processar_aposta(self, id_usuario: str, nome_usuario: str, valor_aposta: int, 
                        tipo_jogo: str, ganhou: bool, multiplicador: float = 1.0) -> Tuple[bool, int]:
        """
        Processa o resultado de uma aposta
        Retorna: (sucesso, mudanca_liquida)
        """
        if not self.pode_pagar(id_usuario, nome_usuario, valor_aposta):
            return False, 0
        
        # Remove o valor da aposta
        self.remover_moedas(id_usuario, valor_aposta, f'{tipo_jogo} - Aposta')
        
        if ganhou:
            ganhos = int(valor_aposta * multiplicador)
            self.adicionar_moedas(id_usuario, ganhos, f'{tipo_jogo} - Vitória')
            mudanca_liquida = ganhos - valor_aposta
            
            # Registra jogo
            self.bd.registrar_jogo(id_usuario, tipo_jogo, valor_aposta, 'vitoria', mudanca_liquida)
            return True, mudanca_liquida
        else:
            # Registra jogo
            self.bd.registrar_jogo(id_usuario, tipo_jogo, valor_aposta, 'derrota', -valor_aposta)
            return True, -valor_aposta
