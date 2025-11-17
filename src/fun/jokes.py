"""Joke system"""

import random


class JokeManager:
    """Manages jokes"""
    
    def __init__(self):
        self.jokes = self._load_jokes()
    
    def _load_jokes(self) -> list:
        """Load jokes database"""
        return [
            "Por que o JavaScript foi ao psicólogo? Porque tinha muitos problemas de 'callback'!",
            "Como chama um macaco que programa? Um code-monkey! 🐵",
            "Qual é o animal mais antigo? A zebra, porque é em preto e branco!",
            "Por que os programadores preferem o escuro? Porque a luz atrai bugs!",
            "O que o zero disse para o oito? Que cinto maneiro!",
            "Por que o HTML foi ao terapeuta? Porque tinha muitas tags issues!",
            "Como o mar se despede? Ele dá tchauzinho com as ondas! 🌊",
            "Qual é a fruta preferida dos programadores? Java!",
            "Por que o SQL foi ao bar? Para fazer um JOIN com os amigos!",
            "O que é um ponteiro em C++? É alguém que aponta problemas!",
            "Por que Python é tão popular? Porque não tem cobras! 🐍",
            "Como se chama um grupo de desenvolvedores? Um array de problemas!",
            "O que é um loop infinito? While(true) { console.log('Socorro!') }",
            "Por que o Git foi expulso da escola? Por fazer muitos commits sem sentido!",
            "Qual é o esporte favorito dos programadores? Debugging!",
            "Como você chama um erro que ninguém consegue resolver? Feature!",
            "Por que os macacos são bons em matemática? Porque adoram problemas de lógica! 🐒",
            "O que o Java disse para o C? Você é muito ponteiro!",
            "Por que o CSS foi ao teatro? Para ver as classes performarem!",
            "Como chama um programador sonolento? Um desenvolvedor em sleep mode! 😴",
        ]
    
    def get_random_joke(self) -> str:
        """Get a random joke"""
        return random.choice(self.jokes)
    
    def get_joke_by_index(self, index: int) -> str:
        """Get a specific joke"""
        if 0 <= index < len(self.jokes):
            return self.jokes[index]
        return self.get_random_joke()
    
    def get_total_jokes(self) -> int:
        """Get total number of jokes"""
        return len(self.jokes)
