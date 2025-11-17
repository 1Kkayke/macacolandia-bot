"""Modelos de dados para o banco de dados"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    """Modelo de usuário"""
    id_usuario: str
    nome_usuario: str
    moedas: int = 1000
    total_ganho: int = 0
    total_perdido: int = 0
    jogos_jogados: int = 0
    criado_em: datetime = None
    ultimo_diario: Optional[datetime] = None
    sequencia: int = 0


@dataclass
class Transacao:
    """Modelo de transação"""
    id: int
    id_usuario: str
    quantia: int
    tipo_transacao: str
    descricao: Optional[str]
    data_hora: datetime


@dataclass
class ConquistaModel:
    """Modelo de conquista"""
    id: int
    id_usuario: str
    nome_conquista: str
    desbloqueada_em: datetime


@dataclass
class HistoricoJogo:
    """Modelo de histórico de jogo"""
    id: int
    id_usuario: str
    tipo_jogo: str
    valor_aposta: int
    resultado: str
    ganhos: int
    data_hora: datetime
