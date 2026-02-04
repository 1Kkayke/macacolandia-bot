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
            'name': 'Quick Math',
            'difficulty': 'easy'
        },
        {
            'type': 'emoji',
            'emoji': '🎯',
            'name': 'Find the Emoji',
            'difficulty': 'medium'
        },
        {
            'type': 'sequence',
            'emoji': '🔢',
            'name': 'Sequence',
            'difficulty': 'medium'
        },
        {
            'type': 'word',
            'emoji': '📝',
            'name': 'Scrambled Word',
            'difficulty': 'hard'
        }
    ]
    
    # Cooldown between heists (in seconds)
    COOLDOWN = 300  # 5 minutos
    DEFENSE_TIME = 15  # 15 segundos para defender
    
    # Percentage that can be stolen
    MIN_STEAL_PERCENT = 0.05  # 5%
    MAX_STEAL_PERCENT = 0.15  # 15%
    
    # Penalties
    FAIL_PENALTY_PERCENT = 0.10  # 10% de penalidade se falhar
    
    @staticmethod
    def calculate_steal_amount(target_balance: int) -> int:
        """Calculate how much can be stolen"""
        # Calculate random percentage between 5% and 15%
        percent = random.uniform(HeistGame.MIN_STEAL_PERCENT, HeistGame.MAX_STEAL_PERCENT)
        amount = int(target_balance * percent)
        
        # Ensure minimum based on victim balance
        if target_balance < 2000:
            min_amount = 100  # For low balances
        elif target_balance < 10000:
            min_amount = int(target_balance * 0.08)  # 8% for medium
        else:
            min_amount = int(target_balance * 0.05)  # 5% for high
        
        # Return the larger of calculated and minimum
        final_amount = max(min_amount, amount)
        print(f"[HEIST] Victim balance: {target_balance:,} | Percent: {percent:.1%} | Calculated: {amount:,} | Minimum: {min_amount:,} | Final: {final_amount:,}")
        return final_amount
    
    @staticmethod
    def can_rob(robber_balance: int, target_balance: int) -> Tuple[bool, str]:
        """Check if robbery is possible"""
        if target_balance < 500:
            return False, "Target must have at least 500 coins!"
        
        if robber_balance < 100:
            return False, "You need at least 100 coins to attempt a heist!"
        
        return True, ""
    
    @staticmethod
    def generate_math_challenge() -> Tuple[str, str]:
        """Generate a simple math problem"""
        operation_type = random.randint(1, 3)
        
        if operation_type == 1:
            # Addition
            a = random.randint(10, 50)
            b = random.randint(10, 50)
            question = f"{a} + {b}"
            answer = str(a + b)
        elif operation_type == 2:
            # Multiplication
            a = random.randint(10, 30)
            b = random.randint(2, 9)
            question = f"{a} × {b}"
            answer = str(a * b)
        else:
            # Subtraction
            a = random.randint(50, 100)
            b = random.randint(10, 40)
            question = f"{a} - {b}"
            answer = str(a - b)
        
        return f"What is: **{question}**?", answer
    
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
        
        return f"Find the position of {target}:\n{emoji_line}\n(Type 1-9)", str(position)
    
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
        return f"Complete the sequence:\n**{seq_str} → ?**", str(answer)
    
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
        
        return f"Unscramble the word {emoji}:\n**{scrambled_word}**", word
    
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
            return "scraps"
        elif amount < 1000:
            return "pocket change"
        elif amount < 5000:
            return "good money"
        elif amount < 10000:
            return "a fortune"
        else:
            return "the JACKPOT"
    
    @staticmethod
    def get_success_messages() -> list:
        """Get random success messages"""
        return [
            "managed to steal",
            "stole",
            "snatched",
            "cleverly took",
            "tricked and took",
            "brazenly robbed",
            "pulled a heist and got"
        ]
    
    @staticmethod
    def get_fail_messages() -> list:
        """Get random fail messages"""
        return [
            "was caught trying to steal",
            "failed the heist attempt",
            "was caught stealing",
            "messed up and got caught",
            "miserably failed to steal",
            "was intercepted trying to steal",
            "got busted trying to steal"
        ]
    
    @staticmethod
    def get_defense_messages() -> list:
        """Get random defense success messages"""
        return [
            "successfully defended",
            "protected their coins",
            "stopped the robbery",
            "beat up the thief",
            "made the thief run",
            "confronted the thief",
            "saved their coins"
        ]
