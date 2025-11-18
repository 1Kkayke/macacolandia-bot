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
            # Perguntas Originais
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
            
            # 🔥 100 PERGUNTAS ENGRAÇADAS E MEMES 🔥
            
            # Memes BR
            Question(
                "Qual foi o prêmio que o Davi Brito ganhou no BBB?",
                ["R$ 1 milhão", "R$ 2,92 milhões", "R$ 500 mil", "Um Fiat Uno"],
                1,
                "Memes BR"
            ),
            Question(
                "Complete: 'Calma...'",
                ["Bebê", "Calabreso", "Calma", "Relaxa"],
                1,
                "Memes BR"
            ),
            Question(
                "O que significa 'Vish kk'?",
                ["Risada", "Bumbum na porta do carro", "Erro de digitação", "Zueira"],
                1,
                "Memes BR"
            ),
            Question(
                "Quanto é 'Se vira nos 30'?",
                ["R$ 30", "30 dias", "30 anos", "30 reais e você se vira"],
                3,
                "Memes BR"
            ),
            Question(
                "Complete: 'Eitaaaa...'",
                ["Preula", "Biuriful", "Mainhaaa", "Todas as anteriores"],
                3,
                "Memes BR"
            ),
            Question(
                "O que significa 'BIRL'?",
                ["Bodybuilder I Really Love", "Bora Its Real Life", "Bodybuilding Is Real Life", "É só um som aleatório"],
                3,
                "Memes BR"
            ),
            Question(
                "Complete: 'Caiu na vila...'",
                ["O samba começou", "O peixe fuzila", "Todo mundo dança", "É hora do show"],
                1,
                "Memes BR"
            ),
            Question(
                "O que é 'Ordem e Progresso'?",
                ["Lema da bandeira do Brasil", "Nome de um meme", "Música", "Todas as anteriores"],
                3,
                "Memes BR"
            ),
            Question(
                "Qual ano virou meme por causa do Zika Vírus?",
                ["2014", "2015", "2016", "2017"],
                2,
                "Memes BR"
            ),
            Question(
                "O que é 'Maizena'?",
                ["Uma comida", "Um meme de 99", "Uma dança", "Um jogo"],
                1,
                "Memes BR"
            ),
            
            # Brainrot / Gen Z
            Question(
                "O que é 'Skibidi Toilet'?",
                ["Um meme absurdo", "Uma música", "Um jogo", "Um vídeo viral"],
                0,
                "Brainrot"
            ),
            Question(
                "O que significa 'Rizz'?",
                ["Carisma", "Dinheiro", "Comida", "Música"],
                0,
                "Brainrot"
            ),
            Question(
                "Quem é o 'Sigma Male'?",
                ["Um macho alfa", "Um macho independente", "Um meme", "Todas as anteriores"],
                3,
                "Brainrot"
            ),
            Question(
                "O que significa 'No Cap'?",
                ["Sem mentira", "Sem boné", "Sem limite", "Sem problema"],
                0,
                "Brainrot"
            ),
            Question(
                "O que é ser 'Based'?",
                ["Ser autêntico", "Ser falso", "Ser engraçado", "Ser triste"],
                0,
                "Brainrot"
            ),
            Question(
                "Quem é o 'Gigachad'?",
                ["Um cara musculoso meme", "Um super-herói", "Um jogador", "Um ator"],
                0,
                "Brainrot"
            ),
            Question(
                "O que significa 'Slay'?",
                ["Matar", "Arrasar", "Dormir", "Comer"],
                1,
                "Brainrot"
            ),
            Question(
                "O que é 'Its Giving'?",
                ["Está dando vibe de", "Está dando dinheiro", "Está dando certo", "Está dando errado"],
                0,
                "Brainrot"
            ),
            Question(
                "O que significa 'Lowkey'?",
                ["Discretamente", "Alto", "Baixo", "Música"],
                0,
                "Brainrot"
            ),
            Question(
                "Quem é o 'Alpha Male'?",
                ["O líder", "O seguidor", "O engraçado", "O tímido"],
                0,
                "Brainrot"
            ),
            
            # Internet/Memes Clássicos
            Question(
                "Quanto é 'Over 9000'?",
                ["Mais de 9000", "Exatamente 9000", "Menos de 9000", "9001"],
                0,
                "Memes Clássicos"
            ),
            Question(
                "O que significa 'GG EZ'?",
                ["Good Game Easy", "Grande Guerreiro", "Ganhou Geral", "Gol do Empate"],
                0,
                "Memes Clássicos"
            ),
            Question(
                "O que é 'Stonks'?",
                ["Ações subindo (errado de propósito)", "Ações caindo", "Um jogo", "Uma música"],
                0,
                "Memes Clássicos"
            ),
            Question(
                "Complete: 'Not...'",
                ["Good", "Bad", "Stonks", "Cool"],
                2,
                "Memes Clássicos"
            ),
            Question(
                "O que é um 'Noob'?",
                ["Novato", "Expert", "Profissional", "Hacker"],
                0,
                "Memes Clássicos"
            ),
            Question(
                "O que significa 'F' no chat?",
                ["Pagar respeitos", "Fracasso", "Foda", "Feliz"],
                0,
                "Memes Clássicos"
            ),
            Question(
                "Qual é o número meme mais famoso?",
                ["42", "69", "666", "Todos"],
                3,
                "Memes Clássicos"
            ),
            Question(
                "O que é 'Respawn'?",
                ["Renascer", "Morrer", "Ganhar", "Perder"],
                0,
                "Memes Clássicos"
            ),
            Question(
                "Complete: 'Press F to...'",
                ["Pay respects", "Fight", "Flee", "Fire"],
                0,
                "Memes Clássicos"
            ),
            Question(
                "O que é um 'Hacker'?",
                ["Alguém muito bom (ou trapaceiro)", "Um programador", "Um jogador", "Todas"],
                3,
                "Memes Clássicos"
            ),
            
            # Zueiras Aleatórias
            Question(
                "Qual é a resposta para tudo?",
                ["42", "69", "420", "Depende"],
                0,
                "Filosofia Meme"
            ),
            Question(
                "O que é melhor?",
                ["Pizza", "Hambúrguer", "Taco", "Todas estão erradas, é miojo"],
                3,
                "Comida"
            ),
            Question(
                "Quantas horas tem um dia?",
                ["24", "12", "48", "Depende se é segunda-feira"],
                3,
                "Humor"
            ),
            Question(
                "O que fazer quando cai a internet?",
                ["Esperar", "Reiniciar o modem", "Chorar", "Todas as anteriores"],
                3,
                "Tecnologia"
            ),
            Question(
                "Qual é o melhor emoji?",
                ["😂", "🤣", "💀", "🗿"],
                3,
                "Memes"
            ),
            Question(
                "O que é 'Perdemo'?",
                ["Perdemos", "Ganhamos de trás pra frente", "Um meme", "Um time"],
                2,
                "Memes BR"
            ),
            Question(
                "Complete: 'É o...'",
                ["Fim", "Início", "Meio", "Bolovo"],
                3,
                "Memes BR"
            ),
            Question(
                "Qual é o pior dia da semana?",
                ["Segunda", "Terça", "Quarta", "Todos exceto sexta"],
                3,
                "Vida"
            ),
            Question(
                "O que fazer às 3h da manhã?",
                ["Dormir", "Estudar", "Jogar", "Questionar a vida"],
                3,
                "Humor"
            ),
            Question(
                "Qual é a melhor desculpa?",
                ["'Desculpa, não vi'", "'Internet caiu'", "'Cachorro comeu'", "'Estava ocupado'"],
                1,
                "Humor"
            ),
            
            # Gaming
            Question(
                "O que fazer quando está perdendo?",
                ["Jogar melhor", "Culpar o time", "Culpar o lag", "Opção 2 e 3"],
                3,
                "Gaming"
            ),
            Question(
                "Qual é o melhor rank?",
                ["Bronze", "Prata", "Ouro", "ELO Hell"],
                3,
                "Gaming"
            ),
            Question(
                "O que é 'Tiltar'?",
                ["Ficar nervoso perdendo", "Ganhar muito", "Jogar bem", "Desistir"],
                0,
                "Gaming"
            ),
            Question(
                "O que significa 'AFK'?",
                ["Away From Keyboard", "Always Focused Killing", "All Friends Know", "A Fila Kaiu"],
                0,
                "Gaming"
            ),
            Question(
                "O que é um 'Tryhard'?",
                ["Alguém que se esforça demais", "Um casual", "Um noob", "Um hacker"],
                0,
                "Gaming"
            ),
            Question(
                "Complete: 'Git...'",
                ["Commit", "Push", "Good", "Todas"],
                3,
                "Programação"
            ),
            Question(
                "O que fazer quando o código não funciona?",
                ["Debug", "Reescrever", "Chorar", "Todas as anteriores"],
                3,
                "Programação"
            ),
            Question(
                "Qual é o melhor editor?",
                ["VS Code", "Vim", "Notepad", "Depende da treta"],
                3,
                "Programação"
            ),
            Question(
                "O que é um 'Bug'?",
                ["Erro", "Feature", "Surpresa", "Todas dependendo do contexto"],
                3,
                "Programação"
            ),
            Question(
                "Quantos monitores precisa um programador?",
                ["1", "2", "3", "Nunca é suficiente"],
                3,
                "Programação"
            ),
            
            # Cultura Pop
            Question(
                "Qual é o melhor filme?",
                ["Shrek", "Shrek 2", "Bee Movie", "Todas as anteriores"],
                3,
                "Filmes"
            ),
            Question(
                "Complete: 'Why so...'",
                ["Sad", "Happy", "Serious", "Bad"],
                2,
                "Filmes"
            ),
            Question(
                "Qual é a melhor série?",
                ["Breaking Bad", "Game of Thrones S1-S7", "The Office", "Depende"],
                3,
                "Séries"
            ),
            Question(
                "O que aconteceu na Ordem 66?",
                ["Jedi foram eliminados", "Império venceu", "Anakin se tornou Darth Vader", "Todas"],
                3,
                "Star Wars"
            ),
            Question(
                "Quantos anéis existem?",
                ["1", "3", "Um anel para todos governar", "9 + 7 + 3 + 1"],
                3,
                "LOTR"
            ),
            Question(
                "O que é 'Simplesmente'?",
                ["Uma palavra", "Um meme", "Modo de falar", "Todas"],
                3,
                "Memes BR"
            ),
            Question(
                "Complete: 'Choquei...'",
                ["De verdade", "Demais", "Totalmente", "Todas servem"],
                3,
                "Memes BR"
            ),
            Question(
                "O que é 'RECEBA'?",
                ["Uma comemoração", "Um ataque", "Um meme", "Todas"],
                3,
                "Memes BR"
            ),
            Question(
                "Complete: 'Vapo...'",
                ["Vapo", "Vapor", "Vape", "Vaporizou"],
                0,
                "Memes BR"
            ),
            Question(
                "O que é 'Paia'?",
                ["Ruim", "Chato", "Sem graça", "Todas as anteriores"],
                3,
                "Memes BR"
            ),
            
            # Conhecimento Inútil
            Question(
                "Quantos lados tem um círculo?",
                ["0", "1", "Infinitos", "Depende da definição"],
                3,
                "Filosofia"
            ),
            Question(
                "Se um vegano come animais, ele ainda é vegano?",
                ["Não", "Sim", "Depende", "Pergunta inválida"],
                3,
                "Filosofia"
            ),
            Question(
                "O que veio primeiro?",
                ["O ovo", "A galinha", "O meme", "Ninguém sabe"],
                3,
                "Filosofia"
            ),
            Question(
                "Quantos pixels tem 1080p?",
                ["1080", "1920x1080", "2.073.600", "Muitos"],
                2,
                "Tecnologia"
            ),
            Question(
                "O que é mais pesado, 1kg de ferro ou 1kg de algodão?",
                ["Ferro", "Algodão", "São iguais", "É uma pegadinha"],
                2,
                "Física"
            ),
            Question(
                "Se você está em segundo lugar e passa o primeiro, em que posição fica?",
                ["Primeiro", "Segundo", "Terceiro", "Confuso"],
                0,
                "Lógica"
            ),
            Question(
                "Quantas pessoas falam português no mundo?",
                ["100 milhões", "200 milhões", "260 milhões", "Muita gente"],
                3,
                "Curiosidade"
            ),
            Question(
                "Qual é a capital do Brasil?",
                ["São Paulo", "Rio", "Brasília", "Acre não existe"],
                2,
                "Geografia"
            ),
            Question(
                "O Acre existe?",
                ["Sim", "Não", "É uma lenda", "Ninguém sabe"],
                2,
                "Memes BR"
            ),
            Question(
                "O que é um 'Bolovo'?",
                ["Bolo no ovo", "Ovo no bolo", "Um meme de 17", "Uma comida estranha"],
                0,
                "Memes BR"
            ),
            
            # Zoeira Total
            Question(
                "Quantas bananas cabem em um elefante?",
                ["42", "Nenhuma", "Depende do tamanho", "Pergunta errada"],
                3,
                "Nonsense"
            ),
            Question(
                "Se um pato nada, ele é nadador?",
                ["Sim", "Não", "Depende", "É um pato"],
                3,
                "Nonsense"
            ),
            Question(
                "Qual é a cor do cavalo branco do Napoleão?",
                ["Branco", "Preto", "Marrom", "É uma pegadinha"],
                0,
                "Pegadinha"
            ),
            Question(
                "O que é um unicórnio sem chifre?",
                ["Um cavalo", "Nada", "Triste", "Todas"],
                3,
                "Nonsense"
            ),
            Question(
                "Quantos dedos tem duas mãos?",
                ["10", "8", "Depende de quem", "20 se contar os pés"],
                0,
                "Matemática"
            ),
            Question(
                "Se você tem 10 bananas e come 3, quantas você tem?",
                ["7", "3", "10 (no estômago)", "Depende"],
                0,
                "Matemática"
            ),
            Question(
                "O que acontece quando você divide por zero?",
                ["Erro", "Infinito", "O universo explode", "Todas"],
                3,
                "Matemática"
            ),
            Question(
                "Qual é melhor: pizza ou pizza?",
                ["Pizza", "Pizza", "Pizza", "Todas as anteriores"],
                3,
                "Filosofia"
            ),
            Question(
                "O que fazer quando não sabe a resposta?",
                ["Chutar A", "Chutar C", "Pular", "Esta aqui"],
                3,
                "Meta"
            ),
            Question(
                "Esta é a última pergunta?",
                ["Sim", "Não", "Talvez", "Você que sabe"],
                1,
                "Meta"
            ),
            Question(
                "O que é 'Toin'?",
                ["Dinheiro", "Som", "Palavra aleatória", "Um meme"],
                0,
                "Memes BR"
            ),
            Question(
                "Complete: 'Não tankei...'",
                ["O bene", "A responsa", "O corre", "Todas"],
                3,
                "Memes BR"
            ),
            Question(
                "O que significa 'Brabo'?",
                ["Bravo", "Incrível", "Zangado", "Todas"],
                3,
                "Memes BR"
            ),
            Question(
                "Qual é o melhor horário para jogar?",
                ["Manhã", "Tarde", "Noite", "Madrugada (3h)"],
                3,
                "Gaming"
            ),
            Question(
                "O que é 'Ovo'?",
                ["Um alimento", "Um meme", "Uma palavra", "Todas"],
                3,
                "Memes BR"
            ),
            Question(
                "Complete: 'Todo dia...'",
                ["A mesma coisa", "Isso", "O mesmo", "Todas servem"],
                1,
                "Memes BR"
            ),
            Question(
                "O que é 'Paciência de Jó'?",
                ["Muita paciência", "Personagem bíblico", "Um meme", "Todas"],
                3,
                "Expressões"
            ),
            Question(
                "Quantas vezes você já perdeu tudo no cassino?",
                ["0", "1-5", "Muitas", "Prefiro não contar"],
                3,
                "Cassino"
            ),
            Question(
                "Qual é a melhor estratégia no cassino?",
                ["Apostar tudo", "Apostar pouco", "Não jogar", "YOLO"],
                3,
                "Cassino"
            ),
            Question(
                "O que fazer quando ganha muito?",
                ["Parar", "Continuar", "Apostar tudo de novo", "Opção 3"],
                2,
                "Cassino"
            ),
            Question(
                "Qual é o número da sorte?",
                ["7", "13", "69", "420"],
                2,
                "Sorte"
            ),
            Question(
                "O que é 'Confusion'?",
                ["Confusão", "Um estado mental", "Quando você não entende nada", "Todas"],
                3,
                "Humor"
            ),
            Question(
                "Complete: 'Tanto...'",
                ["Faz", "Fez", "Vai", "Vem"],
                0,
                "Expressões"
            ),
            Question(
                "O que significa 'Apenas'?",
                ["Somente", "Um meme", "Uma palavra", "Todas"],
                3,
                "Memes"
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
