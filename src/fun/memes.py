"""Meme system with image fetching from internet"""

import aiohttp
import random
from typing import Optional, Dict
from datetime import datetime


class MemeManager:
    def __init__(self):
        self.reddit_meme_subs = [
            'memes',
            'dankmemes',
            'funny',
            'me_irl',
            'wholesomememes',
            'AdviceAnimals',
        ]
        
        self.meme_categories = {
            'sucesso': ['GetMotivated', 'wholesomememes'],
            'fracasso': ['me_irl', 'funny'],
            'troll': ['dankmemes', 'memes'],
            'zoacao': ['funny', 'memes'],
            '2025': ['memes', 'dankmemes'],
        }
        
        self.daily_meme = None
        self.daily_meme_date = None
        
        self.funny_facts = [
            "🦆 Ducks have a corkscrew... anatomical structure. Yes, it's weird.",
            "🐌 Snails can sleep for up to 3 years. Jealous?",
            "🦈 Sharks have existed longer than trees. Mind blown!",
            "🐙 Octopuses have 3 hearts and blue blood. Are they aliens?",
            "🦒 Giraffes have the same number of neck vertebrae as humans: 7!",
            "🐝 Bees can recognize human faces.",
            "🦘 Kangaroos can't walk backwards.",
            "🐧 Penguins propose marriage with rocks.",
            "🦇 Bats always turn left when exiting a cave.",
            "🐨 Koalas sleep up to 22 hours a day. Life goals!",
            "🐘 Elephants are the only animals that can't jump.",
            "🦉 Owls can't move their eyes.",
            "🐻 Polar bears have black skin under their white fur.",
            "🐊 Crocodiles can't stick their tongues out.",
            "🦀 Crabs have teeth in their stomachs.",
            "💻 The first computer bug was literally a moth stuck in components.",
            "🎮 Tetris can help reduce trauma and flashbacks.",
            "🍕 The Hawaiian who invented Hawaiian pizza was Canadian.",
            "☕ Coffee is the second most traded commodity (after oil).",
            "🎵 'Happy Birthday' was copyrighted until 2016.",
            "🎬 The Lion King is basically Hamlet with lions.",
            "🎨 The Mona Lisa has no eyebrows.",
            "🗿 The Statue of Liberty was a gift from France.",
            "🏰 The Great Wall of China can't be seen from space.",
            "⚡ Lightning is 5 times hotter than the sun's surface.",
            "🌙 The moon is moving away from Earth 3.8 cm per year.",
            "☀️ 1 million Earths fit inside the Sun.",
            "🪐 Saturn would float if there was a giant bathtub.",
            "🎯 Honey never spoils. 3000-year-old honey is still edible!",
            "🧀 Cheese is the most stolen food in the world.",
            "🍌 Bananas are slightly radioactive.",
            "🍓 Strawberries aren't berries, but bananas are!",
            "🍅 Tomatoes are fruits, not vegetables.",
            "😂 'LOL' was added to the Oxford dictionary in 2011.",
            "📧 The first email was sent in 1971.",
            "🌐 The first website is still online: info.cern.ch",
            "💾 The first hard drive had only 5MB and weighed 1 ton.",
            "🖱️ The mouse was invented in 1964.",
            "📱 More people have phones than toothbrushes.",
            "🎮 Mario was originally called 'Jumpman'.",
            "👾 Pac-Man was inspired by a pizza missing a slice.",
            "🏃 The average sneeze speed is 100 mph.",
            "👂 Your ears never stop growing.",
            "💪 The strongest muscle in the body is the tongue.",
            "🧠 The human brain is 75% water.",
            "❤️ The heart beats 100,000 times per day.",
            "👁️ Your eyes have 576 megapixels.",
        ]
        
        self.roasts = [
            "{username} is so slow, they use Internet Explorer.",
            "{username}'s code has more bugs than a rainforest.",
            "{username} has less followers than a private account.",
            "{username} is like a cloud - when they disappear, it's a beautiful day.",
            "{username} puts the 'error' in 'trial and error'.",
            "{username} searched for 'how to be interesting' - no results found.",
            "{username}'s WiFi signal is stronger than their personality.",
            "{username} is proof that evolution can go in reverse.",
            "{username} is like a software update - everyone ignores them.",
            "{username} is the reason aliens won't visit Earth.",
            "{username} has the charisma of a 404 error page.",
            "{username} is why we can't have nice things.",
            "{username}'s IQ is lower than their battery percentage.",
            "{username} is living proof that zombies exist.",
            "{username} is about as useful as a screen door on a submarine.",
            "{username} brings nothing to the table, not even the table.",
            "{username} is like Monday - nobody likes them.",
            "{username} has the personality of a loading screen.",
            "{username} is the human equivalent of 'Error 404'.",
            "{username} is what happens when you don't read the documentation.",
        ]
    
    async def fetch_reddit_meme(self, subreddit: str = None, max_attempts: int = 5) -> Optional[Dict]:
        if subreddit is None:
            subreddit = random.choice(self.reddit_meme_subs)
        
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={'User-Agent': 'CasinoBot/1.0'}) as response:
                    if response.status != 200:
                        return None
                    
                    data = await response.json()
                    posts = data['data']['children']
                    
                    image_posts = []
                    for post in posts:
                        post_data = post['data']
                        url = post_data.get('url', '')
                        
                        if any(url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                            image_posts.append({
                                'title': post_data['title'],
                                'url': url,
                                'subreddit': post_data['subreddit'],
                                'score': post_data.get('score', 0),
                                'nsfw': post_data.get('over_18', False)
                            })
                        elif 'i.redd.it' in url or 'i.imgur.com' in url:
                            image_posts.append({
                                'title': post_data['title'],
                                'url': url,
                                'subreddit': post_data['subreddit'],
                                'score': post_data.get('score', 0),
                                'nsfw': post_data.get('over_18', False)
                            })
                    
                    image_posts = [p for p in image_posts if not p['nsfw']]
                    
                    if image_posts:
                        return random.choice(image_posts)
                    
                    return None
                    
        except Exception as e:
            print(f"Error fetching Reddit meme: {e}")
            return None
    
    async def get_meme_by_category(self, category: str) -> Optional[Dict]:
        subreddits = self.meme_categories.get(category.lower(), self.reddit_meme_subs)
        subreddit = random.choice(subreddits)
        return await self.fetch_reddit_meme(subreddit)
    
    async def get_daily_meme(self) -> Optional[Dict]:
        today = datetime.now().date()
        
        if self.daily_meme and self.daily_meme_date == today:
            return self.daily_meme
        
        meme = await self.fetch_reddit_meme()
        if meme:
            self.daily_meme = meme
            self.daily_meme_date = today
        
        return meme
    
    def get_random_fact(self) -> str:
        return random.choice(self.funny_facts)
    
    def get_random_roast(self, username: str) -> str:
        roast = random.choice(self.roasts)
        return roast.format(username=username)
    
    async def get_brazilian_meme(self) -> Optional[Dict]:
        subreddit = random.choice(self.reddit_meme_subs)
        return await self.fetch_reddit_meme(subreddit)
    
    async def get_top_meme(self, subreddit: str = None) -> Optional[Dict]:
        if subreddit is None:
            subreddit = random.choice(self.reddit_meme_subs)
        
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit=50"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={'User-Agent': 'CasinoBot/1.0'}) as response:
                    if response.status != 200:
                        return await self.fetch_reddit_meme(subreddit)
                    
                    data = await response.json()
                    posts = data['data']['children']
                    
                    image_posts = []
                    for post in posts:
                        post_data = post['data']
                        url = post_data.get('url', '')
                        
                        if any(url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']) or \
                           'i.redd.it' in url or 'i.imgur.com' in url:
                            if not post_data.get('over_18', False):
                                image_posts.append({
                                    'title': post_data['title'],
                                    'url': url,
                                    'subreddit': post_data['subreddit'],
                                    'score': post_data.get('score', 0),
                                    'nsfw': False
                                })
                    
                    if image_posts:
                        image_posts.sort(key=lambda x: x['score'], reverse=True)
                        return random.choice(image_posts[:10])
                    
                    return await self.fetch_reddit_meme(subreddit)
                    
        except Exception as e:
            print(f"Error fetching top meme: {e}")
            return await self.fetch_reddit_meme(subreddit)
