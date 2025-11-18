"""Joke system"""

import random


class JokeManager:
    """Manages jokes"""
    
    def __init__(self):
        self.jokes = self._load_jokes()
    
    def _load_jokes(self) -> list:
        """Load jokes database"""
        return [
            "Por que o JavaScript foi no psicólogo? Porque tinha problema de 'callback' pra caralho!",
            "Como chama um macaco que programa? Um code-monkey filho da puta! 🐵",
            "Qual é o animal mais antigo? A zebra, porque é preto e branco que nem TV de pobre!",
            "Por que os programador prefere o escuro? Porque a luz atrai bug, igual merda atrai mosca!",
            "O que o zero disse pro oito? Que cinto maneiro da porra!",
            "Por que o HTML foi no terapeuta? Porque tinha tag issue pra caralho!",
            "Como o mar se despede? Ele dá tchauzinho com as onda seu otário! 🌊",
            "Qual é a fruta preferida dos programador? Java, mas café também serve porra!",
            "Por que o SQL foi no bar? Pra fazer JOIN com os parça!",
            "O que é um ponteiro em C++? É um cara que aponta teus erro fdp!",
            "Por que Python é tão popular? Porque não morde que nem cobra de verdade! 🐍",
            "Como se chama um grupo de dev? Um array de problema!",
            "O que é um loop infinito? While(true) { console.log('VAI TOMAR NO CU!') }",
            "Por que o Git foi expulso da escola? Por fazer commit sem sentido igual criança!",
            "Qual é o esporte favorito dos dev? Debugging até cansar!",
            "Como você chama um erro que ninguém resolve? Feature, porra!",
            "Por que os macaco são bom em matemática? Porque adora problema de lógica! 🐒",
            "O que o Java disse pro C? Tu é muito ponteiro mano!",
            "Por que o CSS foi no teatro? Pra ver as classe se apresentar!",
            "Como chama um programador com sono? Um dev em sleep mode caralho! 😴",
            "Qual o navegador dos pobre? Internet Explorer, porque é grátis e uma bosta!",
            "Por que o PHP chorou? Porque todo mundo fala mal dele porra!",
            "Como chama desenvolvedor que não testa código? Desempregado!",
            "O que o Linux disse pro Windows? Pelo menos eu não trava toda hora fdp!",
            "Por que o React é tão complicado? Porque os dev gosta de sofrer!",
            "Como se chama bug que ninguém acha? Ghost bug filho da puta!",
            "Qual a linguagem mais sincera? Assembly, porque não esconde nada!",
            "Por que o MongoDB foi preso? Por não ter schema nenhum!",
            "O que é um Full Stack? Um cara que faz tudo mal feito!",
            "Como chama dev que não usa Git? Corajoso ou burro, tu decide!",
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
