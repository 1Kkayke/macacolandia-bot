"""Trivia/Quiz system"""

import random
from typing import Dict, List


class Question:
    def __init__(self, question: str, options: List[str], correct: int, category: str):
        self.question = question
        self.options = options
        self.correct = correct
        self.category = category


class TriviaManager:
    def __init__(self):
        self.questions = self._load_questions()
    
    def _load_questions(self) -> List[Question]:
        return [
            Question("Which programming language was created by Guido van Rossum?", ["Java", "Python", "Ruby", "JavaScript"], 1, "Programming"),
            Question("In what year was Discord founded?", ["2013", "2014", "2015", "2016"], 2, "Technology"),
            Question("Which is the smartest primate?", ["Gorilla", "Chimpanzee", "Orangutan", "Baboon"], 1, "Animals"),
            Question("How many bits are in a byte?", ["4", "8", "16", "32"], 1, "Computing"),
            Question("Which of these is NOT a programming language?", ["Python", "JavaScript", "HTML", "Ruby"], 2, "Programming"),
            Question("What does CPU stand for?", ["Central Processing Unit", "Computer Personal Unit", "Central Program Unit", "Computer Processing Unit"], 0, "Hardware"),
            Question("Which open source OS is most used on servers?", ["Windows", "Linux", "macOS", "BSD"], 1, "Systems"),
            Question("Which company created React?", ["Google", "Facebook", "Microsoft", "Amazon"], 1, "Development"),
            Question("What is Git?", ["A programming language", "A text editor", "A version control system", "A browser"], 2, "Tools"),
            Question("What is the default HTTP port?", ["21", "22", "80", "443"], 2, "Networks"),
            Question("How many planets are in the Solar System?", ["7", "8", "9", "10"], 1, "Science"),
            Question("What is the speed of light?", ["300,000 km/s", "150,000 km/s", "450,000 km/s", "600,000 km/s"], 0, "Physics"),
            Question("Who painted the Mona Lisa?", ["Van Gogh", "Picasso", "Leonardo da Vinci", "Michelangelo"], 2, "Art"),
            Question("What is the largest ocean in the world?", ["Atlantic", "Indian", "Arctic", "Pacific"], 3, "Geography"),
            Question("In what year did man first walk on the Moon?", ["1965", "1967", "1969", "1971"], 2, "History"),
            Question("What is 'Skibidi Toilet'?", ["An absurd meme", "A song", "A game", "A viral video"], 0, "Memes"),
            Question("What does 'Rizz' mean?", ["Charisma", "Money", "Food", "Music"], 0, "Slang"),
            Question("What does 'No Cap' mean?", ["No lie", "No hat", "No limit", "No problem"], 0, "Slang"),
            Question("What does it mean to be 'Based'?", ["Authentic", "Fake", "Funny", "Sad"], 0, "Slang"),
            Question("Who is the 'Gigachad'?", ["A muscular meme guy", "A superhero", "A gamer", "An actor"], 0, "Memes"),
            Question("What does 'Slay' mean?", ["To kill", "To excel/impress", "To sleep", "To eat"], 1, "Slang"),
            Question("What is 'Over 9000'?", ["More than 9000", "Exactly 9000", "Less than 9000", "9001"], 0, "Memes"),
            Question("What does 'GG EZ' mean?", ["Good Game Easy", "Great Gamer", "Got Gold", "Goal Equal"], 0, "Gaming"),
            Question("What is 'Stonks'?", ["Stocks rising (misspelled)", "Stocks falling", "A game", "A song"], 0, "Memes"),
            Question("What is a 'Noob'?", ["Newbie", "Expert", "Professional", "Hacker"], 0, "Gaming"),
            Question("What does 'F' in chat mean?", ["Pay respects", "Failure", "Finish", "Fun"], 0, "Gaming"),
            Question("What is 'Respawn'?", ["To be reborn", "To die", "To win", "To lose"], 0, "Gaming"),
            Question("What does 'AFK' mean?", ["Away From Keyboard", "Always Focused Killing", "All Friends Know", "A Fake Key"], 0, "Gaming"),
            Question("What is a 'Tryhard'?", ["Someone who tries too hard", "A casual", "A noob", "A hacker"], 0, "Gaming"),
            Question("What is the answer to everything?", ["42", "69", "420", "Depends"], 0, "Philosophy"),
            Question("How many hours are in a day?", ["24", "12", "48", "Depends if it's Monday"], 3, "Humor"),
            Question("What to do when the internet goes down?", ["Wait", "Restart modem", "Cry", "All of the above"], 3, "Technology"),
            Question("What is the best emoji?", ["😂", "🤣", "💀", "🗿"], 3, "Memes"),
            Question("What is the worst day of the week?", ["Monday", "Tuesday", "Wednesday", "All except Friday"], 3, "Life"),
            Question("What to do at 3am?", ["Sleep", "Study", "Game", "Question life"], 3, "Humor"),
            Question("What to do when losing?", ["Play better", "Blame team", "Blame lag", "Options 2 and 3"], 3, "Gaming"),
            Question("What is the best rank?", ["Bronze", "Silver", "Gold", "ELO Hell"], 3, "Gaming"),
            Question("What does 'Tilting' mean?", ["Getting angry while losing", "Winning a lot", "Playing well", "Giving up"], 0, "Gaming"),
            Question("What is the best movie?", ["Shrek", "Shrek 2", "Bee Movie", "All of the above"], 3, "Movies"),
            Question("Complete: 'Why so...'", ["Sad", "Happy", "Serious", "Bad"], 2, "Movies"),
            Question("What happens when you divide by zero?", ["Error", "Infinity", "Universe explodes", "All of them"], 3, "Math"),
            Question("Which is better: pizza or pizza?", ["Pizza", "Pizza", "Pizza", "All of the above"], 3, "Philosophy"),
            Question("What to do when you don't know the answer?", ["Guess A", "Guess C", "Skip", "This one"], 3, "Meta"),
            Question("Is this the last question?", ["Yes", "No", "Maybe", "You decide"], 1, "Meta"),
            Question("What is the best casino strategy?", ["Bet everything", "Bet little", "Don't play", "YOLO"], 3, "Casino"),
            Question("What to do when winning big?", ["Stop", "Continue", "Bet it all again", "Option 3"], 2, "Casino"),
            Question("What is the lucky number?", ["7", "13", "69", "420"], 2, "Luck"),
        ]
    
    def get_random_question(self) -> Question:
        return random.choice(self.questions)
    
    def get_random_question_excluding(self, used_indices: list) -> tuple:
        available = [(i, q) for i, q in enumerate(self.questions) if i not in used_indices]
        
        if not available:
            return (None, None)
        
        index, question = random.choice(available)
        return (question, index)
    
    def get_question_by_category(self, category: str) -> Question:
        matching = [q for q in self.questions if q.category.lower() == category.lower()]
        if matching:
            return random.choice(matching)
        return self.get_random_question()
    
    def get_categories(self) -> List[str]:
        return list(set(q.category for q in self.questions))
