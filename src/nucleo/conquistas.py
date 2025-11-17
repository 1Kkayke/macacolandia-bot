"""Definições e gerenciamento de conquistas"""

from typing import Dict, List, Callable
from src.banco_dados.gerenciador_bd import GerenciadorBancoDados


class Conquista:
    """Definição de uma conquista"""
    
    def __init__(self, nome: str, titulo: str, descricao: str, 
                 emoji: str, condicao: Callable, recompensa: int = 0):
        self.nome = nome
        self.titulo = titulo
        self.descricao = descricao
        self.emoji = emoji
        self.condicao = condicao
        self.recompensa = recompensa


class GerenciadorConquistas:
    """Gerencia conquistas e verificações"""
    
    def __init__(self, bd: GerenciadorBancoDados):
        self.bd = bd
        self.conquistas = self._definir_conquistas()
    
    def _definir_conquistas(self) -> Dict[str, Conquista]:
        """Define todas as conquistas"""
        conquistas = {
            'primeiro_jogo': Conquista(
                'primeiro_jogo',
                'Primeira Aposta',
                'Jogou seu primeiro jogo',
                '🎮',
                lambda stats_usuario: stats_usuario['jogos_jogados'] >= 1,
                100
            ),
            'apostador_elite': Conquista(
                'apostador_elite',
                'Apostador de Elite',
                'Tenha 10.000 moedas ou mais',
                '💎',
                lambda stats_usuario: stats_usuario['moedas'] >= 10000,
                500
            ),
            'veterano': Conquista(
                'veterano',
                'Veterano',
                'Jogue 100 jogos',
                '🎖️',
                lambda stats_usuario: stats_usuario['jogos_jogados'] >= 100,
                1000
            ),
            'sequencia_sortuda': Conquista(
                'sequencia_sortuda',
                'Sortudo',
                'Mantenha uma sequência de 7 dias de recompensas diárias',
                '🍀',
                lambda stats_usuario: stats_usuario['sequencia'] >= 7,
                500
            ),
            'grande_vencedor': Conquista(
                'grande_vencedor',
                'Grande Vencedor',
                'Ganhe 5.000 moedas no total',
                '🏆',
                lambda stats_usuario: stats_usuario['total_ganho'] >= 5000,
                250
            ),
            'milionario': Conquista(
                'milionario',
                'Milionário',
                'Acumule 50.000 moedas',
                '💰',
                lambda stats_usuario: stats_usuario['moedas'] >= 50000,
                5000
            ),
        }
        return conquistas
    
    def verificar_conquistas(self, id_usuario: str, nome_usuario: str) -> List[Conquista]:
        """Verifica e desbloqueia novas conquistas para um usuário"""
        usuario = self.bd.obter_usuario(id_usuario, nome_usuario)
        stats_usuario = dict(usuario)
        
        desbloqueadas = []
        
        for conquista in self.conquistas.values():
            if conquista.condicao(stats_usuario):
                if self.bd.desbloquear_conquista(id_usuario, conquista.nome):
                    # Conquista acabou de ser desbloqueada, dar recompensa
                    if conquista.recompensa > 0:
                        self.bd.atualizar_moedas(id_usuario, conquista.recompensa)
                        self.bd.adicionar_transacao(
                            id_usuario, 
                            conquista.recompensa, 
                            'conquista',
                            f'Conquista desbloqueada: {conquista.titulo}'
                        )
                    desbloqueadas.append(conquista)
        
        return desbloqueadas
    
    def obter_conquista(self, nome: str) -> Conquista:
        """Obtém conquista pelo nome"""
        return self.conquistas.get(nome)
    
    def obter_todas_conquistas(self) -> List[Conquista]:
        """Obtém todas as conquistas"""
        return list(self.conquistas.values())
