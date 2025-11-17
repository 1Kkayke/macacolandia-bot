"""Sistema de enquetes/votação"""

from typing import Dict, List
from datetime import datetime, timedelta


class Enquete:
    """Objeto de enquete/votação"""
    
    def __init__(self, pergunta: str, opcoes: List[str], id_criador: str, duracao_minutos: int = 5):
        self.pergunta = pergunta
        self.opcoes = opcoes
        self.id_criador = id_criador
        self.votos: Dict[str, int] = {}  # id_usuario -> indice_opcao
        self.criada_em = datetime.now()
        self.expira_em = self.criada_em + timedelta(minutes=duracao_minutos)
    
    def votar(self, id_usuario: str, indice_opcao: int) -> bool:
        """Registra um voto"""
        if indice_opcao < 0 or indice_opcao >= len(self.opcoes):
            return False
        self.votos[id_usuario] = indice_opcao
        return True
    
    def obter_resultados(self) -> Dict[str, int]:
        """Obtém a contagem de votos para cada opção"""
        resultados = {i: 0 for i in range(len(self.opcoes))}
        for voto in self.votos.values():
            resultados[voto] = resultados.get(voto, 0) + 1
        return resultados
    
    def expirou(self) -> bool:
        """Verifica se a enquete expirou"""
        return datetime.now() > self.expira_em
    
    def obter_total_votos(self) -> int:
        """Obtém o número total de votos"""
        return len(self.votos)
    
    def usuario_votou(self, id_usuario: str) -> bool:
        """Verifica se o usuário já votou"""
        return id_usuario in self.votos


class GerenciadorEnquetes:
    """Gerencia enquetes ativas"""
    
    def __init__(self):
        self.enquetes_ativas: Dict[int, Enquete] = {}  # id_mensagem -> Enquete
        self._proximo_id = 1
    
    def criar_enquete(self, pergunta: str, opcoes: List[str], id_criador: str, 
                     duracao_minutos: int = 5) -> int:
        """Cria uma nova enquete e retorna seu ID"""
        id_enquete = self._proximo_id
        self._proximo_id += 1
        
        enquete = Enquete(pergunta, opcoes, id_criador, duracao_minutos)
        self.enquetes_ativas[id_enquete] = enquete
        return id_enquete
    
    def obter_enquete(self, id_enquete: int) -> Enquete:
        """Obtém uma enquete por ID"""
        return self.enquetes_ativas.get(id_enquete)
    
    def fechar_enquete(self, id_enquete: int) -> bool:
        """Fecha e remove uma enquete"""
        if id_enquete in self.enquetes_ativas:
            del self.enquetes_ativas[id_enquete]
            return True
        return False
    
    def limpar_expiradas(self):
        """Remove enquetes expiradas"""
        expiradas = [id_enq for id_enq, enquete in self.enquetes_ativas.items() if enquete.expirou()]
        for id_enq in expiradas:
            del self.enquetes_ativas[id_enq]
