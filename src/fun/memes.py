"""Meme system with image fetching from internet"""

import aiohttp
import random
from typing import Optional, Dict, List
from datetime import datetime


class MemeManager:
    """Manages meme fetching and selection"""
    
    def __init__(self):
        self.reddit_meme_subs = [
            'memes',
            'dankmemes', 
            'me_irl',
            'wholesomememes',
            'AdviceAnimals',
            'terriblefacebookmemes',
            'ComedyCemetery'
        ]
        
        self.brazilian_meme_subs = [
            'brasilmemes',
            'brasil',
            'circojeca',
            'DiretoDoZapZap'
        ]
        
        # Categorias de memes
        self.meme_categories = {
            'sucesso': ['GetMotivated', 'wholesomememes', 'MadeMeSmile'],
            'fracasso': ['Wellthatsucks', 'facepalm', 'therewasanattempt'],
            'troll': ['trollface', 'memes', 'dankmemes'],
            'zoacao': ['ComedyCemetery', 'terriblefacebookmemes', 'shitposting'],
            '2025': ['memes', 'dankmemes', 'GenZ'],
        }
        
        # Cache do meme do dia
        self.daily_meme = None
        self.daily_meme_date = None
        
        # Facts engraçados
        self.funny_facts = [
            "🦆 Patos têm uma corkscrew... estrutura anatômica. Sim, é estranho.",
            "🐌 Caracóis podem dormir por até 3 anos. Inveja?",
            "🦈 Tubarões existem há mais tempo que árvores. Mind blown!",
            "🐙 Polvos têm 3 corações e sangue azul. São alienígenas?",
            "🦒 Girafas têm a mesma quantidade de vértebras no pescoço que humanos: 7!",
            "🐝 Abelhas podem reconhecer rostos humanos.",
            "🦘 Cangurus não conseguem andar para trás.",
            "🐧 Pinguins propõem casamento com pedras.",
            "🦇 Morcegos sempre viram à esquerda ao sair de uma caverna.",
            "🐨 Coalas dormem até 22 horas por dia. Vida goals!",
            "🦎 Lagartixas podem correr na água.",
            "🐘 Elefantes são os únicos animais que não conseguem pular.",
            "🦉 Corujas não conseguem mover os olhos.",
            "🐻 Ursos polares têm pele preta sob o pelo branco.",
            "🦆 Ornitorrincos não têm estômago.",
            "🐊 Crocodilos não conseguem colocar a língua para fora.",
            "🦀 Caranguejos têm dentes no estômago.",
            "🐙 Polvos podem provar com os tentáculos.",
            "🐨 Impressões digitais de coalas são quase idênticas às humanas.",
            "🦈 Tubarões têm medo de golfinhos.",
            "💻 O primeiro computador bug foi literalmente um inseto preso nos componentes.",
            "🎮 O jogo Tetris pode ajudar a reduzir traumas e flashbacks.",
            "📱 A primeira câmera fotográfica precisava de 8 horas de exposição.",
            "🍕 O havaiano que inventou a pizza havaiana era canadense.",
            "🍔 O McDonald's vende 75 hamburgueres por segundo.",
            "☕ Café é a segunda commodity mais negociada no mundo (depois do petróleo).",
            "🎵 A música 'Happy Birthday' estava protegida por copyright até 2016.",
            "🎬 O filme 'O Rei Leão' é basicamente 'Hamlet' com leões.",
            "📺 O controle remoto foi inventado em 1950, mas sem baterias.",
            "🎪 O circo Ringling Bros começou em 1884.",
            "🎨 A Mona Lisa não tem sobrancelhas.",
            "🗿 A Estátua da Liberdade foi um presente da França.",
            "🏰 A Grande Muralha da China não pode ser vista do espaço.",
            "🌍 A Antártida é o único continente sem formigas.",
            "🌊 O oceano tem mais história que todos os museus juntos.",
            "⚡ Um raio é 5 vezes mais quente que a superfície do sol.",
            "🌙 A lua está se afastando da Terra 3,8 cm por ano.",
            "☀️ 1 milhão de Terras cabem dentro do Sol.",
            "🪐 Saturno flutuaria se houvesse uma banheira gigante.",
            "🌟 Vemos o passado quando olhamos para as estrelas.",
            "🎯 Honey nunca estraga. Mel de 3000 anos ainda é comestível!",
            "🧀 Queijo é o alimento mais roubado do mundo.",
            "🥑 Abacates são frutas, não vegetais.",
            "🍌 Bananas são radioativas (levemente).",
            "🥜 Amendoins não são nozes, são legumes.",
            "🍓 Morangos não são frutas, são flores comestíveis.",
            "🍅 Tomates são frutas, não vegetais.",
            "🥥 Cocos são frutas, nozes E sementes ao mesmo tempo.",
            "🫘 Feijão pode ser usado como bateria (experimento de ciência).",
            "🌽 Milho de pipoca pode pular até 1 metro de altura.",
            "😂 'LOL' foi adicionado ao dicionário Oxford em 2011.",
            "🤳 A palavra 'selfie' foi adicionada ao dicionário em 2013.",
            "📧 O primeiro email foi enviado em 1971.",
            "🌐 O primeiro site ainda está online: info.cern.ch",
            "💾 O primeiro HD tinha apenas 5MB e pesava 1 tonelada.",
            "🖱️ O mouse foi inventado em 1964.",
            "⌨️ O teclado QWERTY foi feito para desacelerar a digitação.",
            "📱 Mais pessoas têm celular do que escova de dentes.",
            "🎮 O Mario foi originalmente chamado de 'Jumpman'.",
            "👾 Pac-Man foi inspirado em uma pizza sem uma fatia.",
            "🎯 O nome completo do Mario é 'Mario Mario'.",
            "🦔 Sonic foi criado para competir com o Mario.",
            "🎪 Pokémon significa 'Pocket Monsters'.",
            "🎭 Pikachu é baseado em um esquilo, não em um rato.",
            "🏃 A velocidade média de um espirro é 160 km/h.",
            "👃 Humanos conseguem cheirar mais de 1 trilhão de odores diferentes.",
            "👂 Suas orelhas nunca param de crescer.",
            "💪 O músculo mais forte do corpo é a língua.",
            "🧠 O cérebro humano é 75% água.",
            "❤️ O coração bate 100.000 vezes por dia.",
            "👁️ Seus olhos têm 576 megapixels.",
            "🦷 O esmalte dos dentes é a substância mais dura do corpo.",
            "💀 Bebês nascem com 300 ossos, adultos têm 206.",
            "🎂 Você compartilha seu aniversário com 20 milhões de pessoas.",
            "🎰 As chances de ganhar na loteria são menores que ser atingido por um raio.",
            "🎲 As chances de embaralhar um baralho na mesma ordem duas vezes são quase zero.",
            "🎪 'Hora do Rush' no trânsito foi inventada para organizar o caos.",
            "🚗 O carro médio tem mais poder de processamento que a Apollo 11.",
            "✈️ Você tem mais chances de morrer indo ao aeroporto do que voando.",
            "🚀 Astronautas crescem até 5cm no espaço.",
            "🌌 Existem mais estrelas no universo do que grãos de areia na Terra.",
            "🎵 A música mais tocada no Spotify é 'Shape of You' do Ed Sheeran.",
            "📺 O episódio mais assistido da TV foi o final de M*A*S*H (1983).",
            "🎬 Avatar é o filme mais lucrativo de todos os tempos.",
            "📚 A Bíblia é o livro mais vendido de todos os tempos.",
            "🎨 A pintura mais cara já vendida é 'Salvator Mundi' por $450 milhões.",
            "🏛️ A pirâmide de Gizé foi a estrutura mais alta por 3.800 anos.",
            "🗼 A Torre Eiffel foi temporária (ia ser demolida em 20 anos).",
            "🗽 A Estátua da Liberdade já foi cobre brilhante.",
            "🏰 O Coliseu de Roma tinha capacidade para 80.000 pessoas.",
            "⚔️ A Guerra dos 100 Anos durou 116 anos.",
            "🎭 Shakespeare inventou mais de 1.700 palavras em inglês.",
            "📖 A primeira novela foi escrita no Japão no ano 1007.",
            "✍️ Canhotos representam apenas 10% da população.",
            "🎨 Leonardo da Vinci escrevia de trás para frente.",
            "🎵 Mozart compôs sua primeira sinfonia aos 8 anos.",
            "🎹 Beethoven era surdo quando compôs a 9ª Sinfonia.",
            "🎪 O circo romano tinha até batalhas navais reais.",
            "🎭 O teatro de Shakespeare tinha chão de terra.",
            "🎬 O primeiro filme com som foi 'The Jazz Singer' (1927).",
            "📺 A primeira transmissão de TV foi em 1927.",
            "📻 O rádio atingiu 50 milhões de usuários em 38 anos.",
            "📱 O Facebook atingiu 50 milhões de usuários em 2 anos.",
        ]
    
    async def fetch_reddit_meme(self, subreddit: str = None, max_attempts: int = 5) -> Optional[Dict]:
        """Fetch a random meme from Reddit
        
        Args:
            subreddit: Specific subreddit to fetch from (optional)
            max_attempts: Number of attempts to find a valid meme
            
        Returns:
            Dict with 'title', 'url', 'subreddit' or None if failed
        """
        if subreddit is None:
            subreddit = random.choice(self.reddit_meme_subs + self.brazilian_meme_subs)
        
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={'User-Agent': 'MacacolandiaBot/1.0'}) as response:
                    if response.status != 200:
                        return None
                    
                    data = await response.json()
                    posts = data['data']['children']
                    
                    # Filter for image posts
                    image_posts = []
                    for post in posts:
                        post_data = post['data']
                        url = post_data.get('url', '')
                        
                        # Check if it's an image
                        if any(url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                            image_posts.append({
                                'title': post_data['title'],
                                'url': url,
                                'subreddit': post_data['subreddit'],
                                'score': post_data.get('score', 0),
                                'nsfw': post_data.get('over_18', False)
                            })
                        # Also support i.redd.it links
                        elif 'i.redd.it' in url or 'i.imgur.com' in url:
                            image_posts.append({
                                'title': post_data['title'],
                                'url': url,
                                'subreddit': post_data['subreddit'],
                                'score': post_data.get('score', 0),
                                'nsfw': post_data.get('over_18', False)
                            })
                    
                    # Filter out NSFW
                    image_posts = [p for p in image_posts if not p['nsfw']]
                    
                    if image_posts:
                        return random.choice(image_posts)
                    
                    return None
                    
        except Exception as e:
            print(f"Error fetching Reddit meme: {e}")
            return None
    
    async def get_meme_by_category(self, category: str) -> Optional[Dict]:
        """Get a meme from a specific category"""
        subreddits = self.meme_categories.get(category.lower(), self.reddit_meme_subs)
        subreddit = random.choice(subreddits)
        return await self.fetch_reddit_meme(subreddit)
    
    async def get_daily_meme(self) -> Optional[Dict]:
        """Get the meme of the day (cached)"""
        today = datetime.now().date()
        
        # Check if we have today's meme cached
        if self.daily_meme and self.daily_meme_date == today:
            return self.daily_meme
        
        # Fetch new daily meme
        meme = await self.fetch_reddit_meme()
        if meme:
            self.daily_meme = meme
            self.daily_meme_date = today
        
        return meme
    
    def get_random_fact(self) -> str:
        """Get a random funny fact"""
        return random.choice(self.funny_facts)
    
    async def get_brazilian_meme(self) -> Optional[Dict]:
        """Get a Brazilian meme"""
        subreddit = random.choice(self.brazilian_meme_subs)
        return await self.fetch_reddit_meme(subreddit)
    
    async def get_top_meme(self, subreddit: str = None) -> Optional[Dict]:
        """Get a top-rated meme from today"""
        if subreddit is None:
            subreddit = random.choice(self.reddit_meme_subs)
        
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit=50"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={'User-Agent': 'MacacolandiaBot/1.0'}) as response:
                    if response.status != 200:
                        return await self.fetch_reddit_meme(subreddit)
                    
                    data = await response.json()
                    posts = data['data']['children']
                    
                    # Filter for image posts
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
                        # Sort by score and pick from top 10
                        image_posts.sort(key=lambda x: x['score'], reverse=True)
                        return random.choice(image_posts[:10])
                    
                    return await self.fetch_reddit_meme(subreddit)
                    
        except Exception as e:
            print(f"Error fetching top meme: {e}")
            return await self.fetch_reddit_meme(subreddit)
