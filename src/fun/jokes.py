"""Joke system"""

import random


class JokeManager:
    def __init__(self):
        self.jokes = self._load_jokes()
    
    def _load_jokes(self) -> list:
        return [
            "Why did JavaScript go to therapy? Too many callback issues!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "What did zero say to eight? Nice belt!",
            "Why did the developer go broke? Because he used up all his cache!",
            "How does the ocean say hello? It waves! 🌊",
            "Why is Python so popular? Because it doesn't bite! 🐍",
            "What's a group of developers called? An array of problems!",
            "What's an infinite loop? while(true) { console.log('Still running!') }",
            "Why was Git expelled from school? Too many bad commits!",
            "What's a programmer's favorite sport? Debugging!",
            "What do you call a bug no one fixes? A feature!",
            "Why did the CSS go to theater? To see classes perform!",
            "What do you call a sleepy programmer? In sleep mode! 😴",
            "Why did PHP cry? Everyone talks bad about it!",
            "What do you call a dev who doesn't test code? Unemployed!",
            "What did Linux say to Windows? At least I don't crash every hour!",
            "Why is React so complicated? Developers love to suffer!",
            "What's a bug no one finds? Ghost bug!",
            "Which language is the most honest? Assembly, hides nothing!",
            "Why was MongoDB arrested? No schema at all!",
            "What's a Full Stack dev? Someone who does everything poorly!",
            "What do you call a dev without Git? Brave or dumb, you decide!",
        ]
    
    def get_random_joke(self) -> str:
        return random.choice(self.jokes)
    
    def get_joke_by_index(self, index: int) -> str:
        if 0 <= index < len(self.jokes):
            return self.jokes[index]
        return self.get_random_joke()
    
    def get_total_jokes(self) -> int:
        return len(self.jokes)
