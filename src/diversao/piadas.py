"""Sistema de piadas"""

import random


class GerenciadorPiadas:
    """Gerencia piadas"""
    
    def __init__(self):
        self.piadas = self._carregar_piadas()
    
    def _carregar_piadas(self) -> list:
        """Carrega banco de dados de piadas"""
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
    
    def obter_piada_aleatoria(self) -> str:
        """Obtém uma piada aleatória"""
        return random.choice(self.piadas)
    
    def obter_piada_por_indice(self, indice: int) -> str:
        """Obtém uma piada específica"""
        if 0 <= indice < len(self.piadas):
            return self.piadas[indice]
        return self.obter_piada_aleatoria()
    
    def obter_total_piadas(self) -> int:
        """Obtém o número total de piadas"""
        return len(self.piadas)
