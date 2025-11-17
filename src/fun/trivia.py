"""Trivia/Quiz system"""

import random
from typing import Dict, List


class Question:
    """Trivia question"""
    
    def __init__(self, question: str, options: List[str], correct: int, category: str):
        self.question = question
        self.options = options
        self.correct = correct
        self.category = category


class TriviaManager:
    """Manages trivia questions"""
    
    def __init__(self):
        self.questions = self._load_questions()
    
    def _load_questions(self) -> List[Question]:
        """Load trivia questions"""
        return [
            Question(
                "Qual é a linguagem de programação criada por Guido van Rossum?",
                ["Java", "Python", "Ruby", "JavaScript"],
                1,
                "Programação"
            ),
            Question(
                "Em que ano foi fundado o Discord?",
                ["2013", "2014", "2015", "2016"],
                2,
                "Tecnologia"
            ),
            Question(
                "Qual é o nome do macaco mais inteligente?",
                ["Gorila", "Chimpanzé", "Orangotango", "Babuíno"],
                1,
                "Animais"
            ),
            Question(
                "Quantos bits tem um byte?",
                ["4", "8", "16", "32"],
                1,
                "Computação"
            ),
            Question(
                "Qual destas NÃO é uma linguagem de programação?",
                ["Python", "JavaScript", "HTML", "Ruby"],
                2,
                "Programação"
            ),
            Question(
                "O que significa CPU?",
                ["Central Processing Unit", "Computer Personal Unit", "Central Program Unit", "Computer Processing Unit"],
                0,
                "Hardware"
            ),
            Question(
                "Qual é o sistema operacional de código aberto mais usado em servidores?",
                ["Windows", "Linux", "macOS", "BSD"],
                1,
                "Sistemas"
            ),
            Question(
                "Qual empresa criou o React?",
                ["Google", "Facebook", "Microsoft", "Amazon"],
                1,
                "Desenvolvimento"
            ),
            Question(
                "O que é Git?",
                ["Uma linguagem de programação", "Um editor de texto", "Um sistema de controle de versão", "Um navegador"],
                2,
                "Ferramentas"
            ),
            Question(
                "Qual é a porta padrão do HTTP?",
                ["21", "22", "80", "443"],
                2,
                "Redes"
            ),
            Question(
                "Quantos planetas existem no Sistema Solar?",
                ["7", "8", "9", "10"],
                1,
                "Ciência"
            ),
            Question(
                "Qual é a velocidade da luz?",
                ["300.000 km/s", "150.000 km/s", "450.000 km/s", "600.000 km/s"],
                0,
                "Física"
            ),
            Question(
                "Quem pintou a Mona Lisa?",
                ["Van Gogh", "Picasso", "Leonardo da Vinci", "Michelangelo"],
                2,
                "Arte"
            ),
            Question(
                "Qual é o maior oceano do mundo?",
                ["Atlântico", "Índico", "Ártico", "Pacífico"],
                3,
                "Geografia"
            ),
            Question(
                "Em que ano o homem pisou na Lua pela primeira vez?",
                ["1965", "1967", "1969", "1971"],
                2,
                "História"
            ),
        ]
    
    def get_random_question(self) -> Question:
        """Get a random trivia question"""
        return random.choice(self.questions)
    
    def get_question_by_category(self, category: str) -> Question:
        """Get a random question from a category"""
        matching = [q for q in self.questions if q.category.lower() == category.lower()]
        if matching:
            return random.choice(matching)
        return self.get_random_question()
    
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        return list(set(q.category for q in self.questions))
