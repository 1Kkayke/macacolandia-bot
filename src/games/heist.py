"""Heist/Robbery game implementation"""

import random
import time
from typing import Tuple


class HeistGame:
    """Robbery minigame with defense mechanics"""
    
    # Success rates based on target's balance
    BASE_SUCCESS_RATE = 0.6  # 60% base success
    
    # Defense minigame types
    DEFENSE_TYPES = [
        {
            'type': 'math',
            'emoji': '🧮',
            'name': 'Matemática Rápida',
            'difficulty': 'fácil'
        },
        {
            'type': 'emoji',
            'emoji': '🎯',
            'name': 'Encontre o Emoji',
            'difficulty': 'médio'
        },
        {
            'type': 'sequence',
            'emoji': '🔢',
            'name': 'Sequência',
            'difficulty': 'médio'
        },
        {
            'type': 'word',
            'emoji': '📝',
            'name': 'Palavra Embaralhada',
            'difficulty': 'difícil'
        }
    ]
    
    # Cooldown entre roubos (em segundos)
    COOLDOWN = 300  # 5 minutos
    DEFENSE_TIME = 15  # 15 segundos para defender
    
    # Porcentagem do saldo que pode ser roubada
    MIN_STEAL_PERCENT = 0.05  # 5%
    MAX_STEAL_PERCENT = 0.15  # 15%
    
    # Penalidades
    FAIL_PENALTY_PERCENT = 0.10  # 10% de penalidade se falhar
    
    @staticmethod
    def calculate_steal_amount(target_balance: int) -> int:
        """Calculate how much can be stolen"""
        percent = random.uniform(HeistGame.MIN_STEAL_PERCENT, HeistGame.MAX_STEAL_PERCENT)
        amount = int(target_balance * percent)
        return max(100, amount)  # Mínimo 100 moedas
    
    @staticmethod
    def can_rob(robber_balance: int, target_balance: int) -> Tuple[bool, str]:
        """Check if robbery is possible"""
        if target_balance < 500:
            return False, "O alvo precisa ter pelo menos 500 moedas!"
        
        if robber_balance < 100:
            return False, "Você precisa ter pelo menos 100 moedas para tentar roubar!"
        
        return True, ""
    
    @staticmethod
    def generate_math_challenge() -> Tuple[str, str]:
        """Generate a simple math problem"""
        operations = [
            lambda: (f"{random.randint(10, 50)} + {random.randint(10, 50)}", 
                    str(eval(f"{random.randint(10, 50)} + {random.randint(10, 50)}"))),
            lambda: (f"{random.randint(10, 30)} × {random.randint(2, 9)}", 
                    str(eval(f"{random.randint(10, 30)} * {random.randint(2, 9)}"))),
            lambda: (f"{random.randint(50, 100)} - {random.randint(10, 40)}", 
                    str(eval(f"{random.randint(50, 100)} - {random.randint(10, 40)}"))),
        ]
        
        operation = random.choice(operations)
        question, answer = operation()
        return f"Quanto é: **{question}**?", answer
    
    @staticmethod
    def generate_emoji_challenge() -> Tuple[str, str]:
        """Generate emoji finding challenge"""
        emojis = ['🍎', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍒', '🍑', '🥝', 
                  '🥑', '🍆', '🥕', '🌽', '🥦', '🥒', '🌶️', '🥔', '🍄', '🥜']
        
        target = random.choice(emojis)
        other_emojis = random.sample([e for e in emojis if e != target], 8)
        
        # Mix them up
        all_emojis = other_emojis + [target]
        random.shuffle(all_emojis)
        
        position = all_emojis.index(target) + 1
        emoji_line = ' '.join(all_emojis)
        
        return f"Encontre a posição do {target}:\n{emoji_line}\n(Digite 1-9)", str(position)
    
    @staticmethod
    def generate_sequence_challenge() -> Tuple[str, str]:
        """Generate number sequence challenge"""
        patterns = [
            # Arithmetic progression
            lambda: (start := random.randint(5, 20), step := random.randint(3, 7), 
                    [start, start+step, start+2*step, start+3*step], start+4*step),
            # Multiply by 2
            lambda: (start := random.randint(2, 8), 
                    [start, start*2, start*4, start*8], start*16),
            # Add increasing
            lambda: (start := random.randint(10, 20), 
                    [start, start+2, start+5, start+9], start+14),
        ]
        
        pattern = random.choice(patterns)()
        if len(pattern) == 2:
            sequence, answer = pattern
        else:
            start, step, sequence, answer = pattern
        
        seq_str = ' → '.join(map(str, sequence))
        return f"Complete a sequência:\n**{seq_str} → ?**", str(answer)
    
    @staticmethod
    def generate_word_challenge() -> Tuple[str, str]:
        """Generate scrambled word challenge"""
        words = {
            'ROUBO': '💰', 'MOEDA': '🪙', 'JOGO': '🎮', 'SORTE': '🍀',
            'CASSINO': '🎰', 'APOSTA': '🎲', 'BANCO': '🏦', 'CRIME': '🚔',
            'DEFESA': '🛡️', 'ATAQUE': '⚔️', 'FUGIR': '🏃', 'SEGURO': '🔒'
        }
        
        word = random.choice(list(words.keys()))
        emoji = words[word]
        
        # Scramble the word
        scrambled = list(word)
        random.shuffle(scrambled)
        scrambled_word = ''.join(scrambled)
        
        # Make sure it's actually scrambled
        while scrambled_word == word and len(word) > 3:
            random.shuffle(scrambled)
            scrambled_word = ''.join(scrambled)
        
        return f"Desembaralhe a palavra {emoji}:\n**{scrambled_word}**", word
    
    @staticmethod
    def generate_challenge() -> Tuple[dict, str, str]:
        """Generate a random challenge for defense"""
        challenge_type = random.choice(HeistGame.DEFENSE_TYPES)
        
        if challenge_type['type'] == 'math':
            question, answer = HeistGame.generate_math_challenge()
        elif challenge_type['type'] == 'emoji':
            question, answer = HeistGame.generate_emoji_challenge()
        elif challenge_type['type'] == 'sequence':
            question, answer = HeistGame.generate_sequence_challenge()
        else:  # word
            question, answer = HeistGame.generate_word_challenge()
        
        return challenge_type, question, answer
    
    @staticmethod
    def check_answer(user_answer: str, correct_answer: str, challenge_type: str) -> bool:
        """Check if the defense answer is correct"""
        user_answer = user_answer.strip().upper()
        correct_answer = correct_answer.strip().upper()
        
        return user_answer == correct_answer
    
    @staticmethod
    def get_loot_description(amount: int) -> str:
        """Get descriptive text for loot amount"""
        if amount < 500:
            return "migalhas"
        elif amount < 1000:
            return "um trocado"
        elif amount < 5000:
            return "uma boa grana"
        elif amount < 10000:
            return "uma fortuna"
        else:
            return "o JACKPOT"
    
    @staticmethod
    def get_success_messages() -> list:
        """Get random success messages"""
        return [
            "conseguiu roubar",
            "furtou",
            "surrupiou",
            "levou na malandragem",
            "passou a perna e levou",
            "roubou descaradamente",
            "deu um golpe e pegou"
        ]
    
    @staticmethod
    def get_fail_messages() -> list:
        """Get random fail messages"""
        return [
            "foi pego tentando roubar",
            "se deu mal na tentativa de roubo",
            "foi flagrado roubando",
            "pisou na bola e foi pego",
            "falhou miseravelmente ao tentar roubar",
            "foi interceptado tentando furtar",
            "tomou na cabeça tentando roubar"
        ]
    
    @staticmethod
    def get_defense_messages() -> list:
        """Get random defense success messages"""
        return [
            "defendeu com sucesso",
            "protegeu suas moedas",
            "impediu o roubo",
            "deu uma surra no ladrão",
            "botou o ladrão pra correr",
            "meteu o dedo na cara do ladrão",
            "salvou suas moedas"
        ]
