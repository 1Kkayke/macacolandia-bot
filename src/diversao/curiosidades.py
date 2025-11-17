"""Sistema de trivia/quiz"""

import random
from typing import Dict, List


class Pergunta:
    """Pergunta de trivia"""
    
    def __init__(self, pergunta: str, opcoes: List[str], correta: int, categoria: str):
        self.pergunta = pergunta
        self.opcoes = opcoes
        self.correta = correta
        self.categoria = categoria


class GerenciadorCuriosidades:
    """Gerencia perguntas de trivia"""
    
    def __init__(self):
        self.perguntas = self._carregar_perguntas()
    
    def _carregar_perguntas(self) -> List[Pergunta]:
        """Carrega perguntas de trivia"""
        return [
            Pergunta(
                "Qual é a linguagem de programação criada por Guido van Rossum?",
                ["Java", "Python", "Ruby", "JavaScript"],
                1,
                "Programação"
            ),
            Pergunta(
                "Em que ano foi fundado o Discord?",
                ["2013", "2014", "2015", "2016"],
                2,
                "Tecnologia"
            ),
            Pergunta(
                "Qual é o nome do macaco mais inteligente?",
                ["Gorila", "Chimpanzé", "Orangotango", "Babuíno"],
                1,
                "Animais"
            ),
            Pergunta(
                "Quantos bits tem um byte?",
                ["4", "8", "16", "32"],
                1,
                "Computação"
            ),
            Pergunta(
                "Qual destas NÃO é uma linguagem de programação?",
                ["Python", "JavaScript", "HTML", "Ruby"],
                2,
                "Programação"
            ),
            Pergunta(
                "O que significa CPU?",
                ["Central Processing Unit", "Computer Personal Unit", "Central Program Unit", "Computer Processing Unit"],
                0,
                "Hardware"
            ),
            Pergunta(
                "Qual é o sistema operacional de código aberto mais usado em servidores?",
                ["Windows", "Linux", "macOS", "BSD"],
                1,
                "Sistemas"
            ),
            Pergunta(
                "Qual empresa criou o React?",
                ["Google", "Facebook", "Microsoft", "Amazon"],
                1,
                "Desenvolvimento"
            ),
            Pergunta(
                "O que é Git?",
                ["Uma linguagem de programação", "Um editor de texto", "Um sistema de controle de versão", "Um navegador"],
                2,
                "Ferramentas"
            ),
            Pergunta(
                "Qual é a porta padrão do HTTP?",
                ["21", "22", "80", "443"],
                2,
                "Redes"
            ),
            Pergunta(
                "Quantos planetas existem no Sistema Solar?",
                ["7", "8", "9", "10"],
                1,
                "Ciência"
            ),
            Pergunta(
                "Qual é a velocidade da luz?",
                ["300.000 km/s", "150.000 km/s", "450.000 km/s", "600.000 km/s"],
                0,
                "Física"
            ),
            Pergunta(
                "Quem pintou a Mona Lisa?",
                ["Van Gogh", "Picasso", "Leonardo da Vinci", "Michelangelo"],
                2,
                "Arte"
            ),
            Pergunta(
                "Qual é o maior oceano do mundo?",
                ["Atlântico", "Índico", "Ártico", "Pacífico"],
                3,
                "Geografia"
            ),
            Pergunta(
                "Em que ano o homem pisou na Lua pela primeira vez?",
                ["1965", "1967", "1969", "1971"],
                2,
                "História"
            ),
        ]
    
    def obter_pergunta_aleatoria(self) -> Pergunta:
        """Obtém uma pergunta aleatória de trivia"""
        return random.choice(self.perguntas)
    
    def obter_pergunta_por_categoria(self, categoria: str) -> Pergunta:
        """Obtém uma pergunta aleatória de uma categoria"""
        correspondentes = [p for p in self.perguntas if p.categoria.lower() == categoria.lower()]
        if correspondentes:
            return random.choice(correspondentes)
        return self.obter_pergunta_aleatoria()
    
    def obter_categorias(self) -> List[str]:
        """Obtém todas as categorias disponíveis"""
        return list(set(p.categoria for p in self.perguntas))
