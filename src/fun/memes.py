"""Meme system with image fetching from internet"""

import aiohttp
import random
from typing import Optional, Dict, List
from datetime import datetime


class MemeManager:
    """Manages meme fetching and selection"""
    
    def __init__(self):
        # Apenas subreddits de shitpost e memes pesados
        self.reddit_meme_subs = [
            'circojeca',           # Shitpost BR pesado
            'DiretoDoZapZap',      # Memes pesados do ZapZap
            'botecodoreddit',      # Memes pesados variados
            'brasilivre',          # Memes sem censura
            'orochinho',           # Shitpost pesado
            'nhaa',                # Memes da comunidade
            'HUEstation',          # Memes pesados BR
            'semtcholas',          # Shitpost BR
            'clubedosaas',         # Memes de humor negro
        ]
        
        # Categorias de memes (todos shitpost/pesados)
        self.meme_categories = {
            'sucesso': ['circojeca', 'DiretoDoZapZap', 'botecodoreddit'],
            'fracasso': ['DiretoDoZapZap', 'circojeca', 'orochinho'],
            'troll': ['circojeca', 'botecodoreddit', 'brasilivre'],
            'zoacao': ['DiretoDoZapZap', 'circojeca', 'botecodoreddit'],
            '2025': ['circojeca', 'DiretoDoZapZap', 'HUEstation'],
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
            subreddit = random.choice(self.reddit_meme_subs)
        
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
    
    def get_random_roast(self, username: str) -> str:
        """Get a random roast/fact about a user"""
        roasts = [
            # Inteligência/Burrice
            f"{username} é tão burro que acha que PDF é o primo do PCC.",
            f"{username} tentou hackear o WiFi do vizinho... desligando o roteador dele.",
            f"{username} é tipo Internet Explorer: todo mundo já desistiu dele.",
            f"{username} colocou um espelho na frente para se ver em HD.",
            f"{username} tentou baixar RAM no computador.",
            f"{username} é tão lento que o loading do GTA V parece rápido perto dele.",
            f"{username} achou que Ubuntu era uma dança africana.",
            f"{username} tentou ligar o computador pelo botão do monitor.",
            f"{username} é tão lerdo que perdeu uma corrida pro Faustão.",
            f"{username} tentou jogar Minecraft na calculadora da escola.",
            f"{username} é tipo Windows Vista: ninguém pediu, mas veio.",
            f"{username} acha que Python é só cobra.",
            f"{username} formatou o PC e perdeu tudo... inclusive a dignidade.",
            f"{username} é tão devagar que usa dial-up em 2025.",
            f"{username} tentou instalar Fortnite no microondas.",
            
            # Aparência/Feiúra
            f"{username} é tão feio que o espelho pediu desculpas.",
            f"{username} quebrou a câmera do Zoom.",
            f"{username} é tão feio que assustou o Jump Scare.",
            f"{username} colocou foto de perfil e o Discord crashou.",
            f"{username} é tipo CAPTCHA: difícil de olhar.",
            f"{username} tem cara de foto 3x4 tirada no poste.",
            f"{username} é tão feio que o Picasso olhou e disse 'tá muito abstrato'.",
            f"{username} tentou tirar selfie e o celular pediu para parar.",
            f"{username} tem cara de NPC de jogo de PS2.",
            f"{username} é tão feio que o Shrek virou modelo perto dele.",
            
            # Peso/Gordura
            f"{username} é tão gordo que usa Google Earth para tirar selfie.",
            f"{username} quebrou a balança... e a academia.",
            f"{username} é tipo Thanos: equilibrado? Não. Pesado? Sim.",
            f"{username} pesa tanto que tem CEP próprio.",
            f"{username} entrou na piscina e virou tsunami.",
            f"{username} é tão gordo que joga Subway Surfers na vida real fugindo da diet.",
            f"{username} pisou na balança e apareceu 'Error: overflow'.",
            f"{username} comeu tanto que virou um planador.",
            f"{username} é tão gordo que quando pula, é terremoto.",
            f"{username} tem foto de satélite, não de perfil.",
            
            # Magreza
            f"{username} é tão magro que usa cinto na cabeça.",
            f"{username} sumiu de perfil.",
            f"{username} é tipo fone de ouvido: fino e quebra fácil.",
            f"{username} tomou banho e escorreu pelo ralo.",
            f"{username} é tão magro que parece barra de busca.",
            f"{username} usa corda de varal como cinto.",
            f"{username} escorregou no McDonald's e saiu pelo ventilador.",
            f"{username} é tão magro que vira pilão quando toma soco.",
            
            # Cheiro/Higiene  
            f"{username} fede tanto que o sabonete desviou dele.",
            f"{username} tomou banho e a água ficou preta.",
            f"{username} é tão fedido que o perfume pediu demissão.",
            f"{username} entrou no ônibus e todo mundo desceu.",
            f"{username} passou perto e o desodorante venceu.",
            f"{username} toma banho uma vez por ano... se lembrar.",
            f"{username} fede tanto que o nariz pediu férias.",
            f"{username} passou e as moscas desmaiaram.",
            
            # Pobreza
            f"{username} é tão pobre que paga conta de luz com vela.",
            f"{username} comeu miojo cru porque não tinha gás.",
            f"{username} tem Wi-Fi do vizinho do vizinho.",
            f"{username} é tão pobre que joga Minecraft pirata no celular da mãe.",
            f"{username} roubou cabo de internet para usar de corda de varal.",
            f"{username} tem cartão de crédito de papelão.",
            f"{username} pediu Uber e veio a pé.",
            f"{username} usa celular de flip em 2025.",
            f"{username} tem iPhone 3 e acha que é rico.",
            f"{username} comprou PC Gamer na Shopee... de mentirinha.",
            
            # Falta de habilidade/Noob
            f"{username} é tão ruim no LoL que o Bronze pediu downgrade.",
            f"{username} morre no tutorial dos jogos.",
            f"{username} é tipo lag: atrapalha todo mundo.",
            f"{username} foi kickado do Easy Mode.",
            f"{username} é tão ruim que o AFK joga melhor.",
            f"{username} perde até no Candy Crush.",
            f"{username} foi banido do Free Fire por ser ruim demais.",
            f"{username} perdeu pro bot em Easy.",
            f"{username} é tipo cheater invertido: ajuda o inimigo.",
            f"{username} tem 0% de win rate... impressionante.",
            
            # Solidão
            f"{username} tem menos amigos que o Tom do MySpace.",
            f"{username} foi adicionado no grupo 'só eu'.",
            f"{username} joga multiplayer sozinho.",
            f"{username} comemora aniversário pelo Google Meet... sem ninguém.",
            f"{username} tem mais bots que amigos na lista.",
            f"{username} foi bloqueado até pela mãe.",
            f"{username} tem 0 seguidores no Instagram... incluindo ele mesmo.",
            f"{username} mandou 'oi' no grupo e todo mundo saiu.",
            f"{username} cria contas fake pra ter amigos.",
            
            # Azar/Sortudo reverso
            f"{username} é tão azarado que ganhou na loteria... do boleto.",
            f"{username} nasceu no loading da vida.",
            f"{username} apostou no Brasil e o Brasil perdeu de 7x1.",
            f"{username} encontrou trevo de 4 folhas... murcho.",
            f"{username} é tipo 404: erro não encontrado.",
            f"{username} abriu caixa misteriosa e veio conta pra pagar.",
            f"{username} pisou em merda... duas vezes no mesmo dia.",
            f"{username} é tão azarado que foi atropelado por bicicleta.",
            
            # Preguiça
            f"{username} é tão preguiçoso que cansa de respirar.",
            f"{username} terceirizou até a preguiça dele.",
            f"{username} tá no modo avião da vida.",
            f"{username} é tipo Snorlax: sempre dormindo.",
            f"{username} tem preguiça de ter preguiça.",
            f"{username} nunca viu o sol nascer... nem o pôr.",
            f"{username} tira soneca entre as sonecas.",
            f"{username} mandou mensagem de voz porque digitar cansa.",
            
            # Família
            f"{username} foi adotado... e devolvido.",
            f"A mãe de {username} pediu reembolso no hospital.",
            f"{username} nasceu e o médico disse 'meus pêsames'.",
            f"O pai de {username} saiu pra comprar cigarro em 2005.",
            f"{username} tem árvore genealógica de bambu: fraca.",
            f"A família de {username} faz rifa pra ver quem fica com ele no Natal.",
            
            # Relacionamento
            f"{username} tem namorada... no Roblox.",
            f"{username} foi friendzonado pela mão direita.",
            f"{username} mandou 'oi' e levou ghost do próprio reflexo.",
            f"{username} namora faz 5 anos... no The Sims.",
            f"{username} foi bloqueado até pela crushzinha do orkut.",
            f"{username} tem foto de casal... ele e o travesseiro.",
            f"{username} foi rejeitado no Tinder... pela mãe dele.",
            
            # Trabalho/Estudo
            f"{username} foi demitido do estágio não-remunerado.",
            f"{username} reprovou em EAD.",
            f"{username} tem diploma de palhaço... e usa no dia a dia.",
            f"{username} foi expulso do curso de Como Ser Expulso.",
            f"{username} trabalha de segunda a domingo... no Habbo Hotel.",
            f"{username} tem currículo em Comic Sans.",
            f"{username} fez MBA... de Memes Bons pra Assim.",
            
            # Mentiras/Fanfarronice
            f"{username} disse que tem PC Gamer... é um notebook de 2010.",
            f"{username} mente até pra si mesmo.",
            f"{username} tem Ferrari... no GTA San Andreas.",
            f"{username} disse que é hacker... usa a senha '123456'.",
            f"{username} tem Mercedes... de brinquedo.",
            f"{username} fala que tem crypto... são moedas do Tibia.",
            
            # Estilo/Moda
            f"{username} se veste como NPC de Minecraft.",
            f"{username} usa Crocs com meia... e acha bonito.",
            f"{username} tem drip negativo.",
            f"{username} compra roupa na reciclagem.",
            f"{username} usa camisa do Corinthians... mas torce pro Vasco.",
            f"{username} tem estilo de mendigo estiloso... sem o estiloso.",
            
            # Bebida/Festa
            f"{username} fica bêbado com Yakult.",
            f"{username} vai pra festa... pela transmissão ao vivo.",
            f"{username} bebeu energético e dormiu.",
            f"{username} tomou vodka e chorou pela ex... que nunca existiu.",
            f"{username} dança pior que o tio bêbado no churrasco.",
            
            # Altura
            f"{username} é tão baixo que usa escada pra subir no meio-fio.",
            f"{username} tem altura de NPC do Habbo.",
            f"{username} é tipo hobbit: baixo e come muito.",
            f"{username} precisa de banquinho pra ver o horizonte.",
            f"{username} é tão baixo que usa booster de criança no carro.",
            
            # Idade
            f"{username} é tão velho que conheceu o Acre antes de sumir.",
            f"{username} jogou Tibia quando lançou... no beta.",
            f"{username} tem idade de árvore: muita e ninguém conta.",
            f"{username} lembra da época que Orkut era popular.",
            f"{username} é tão velho que tem RG em hieróglifo.",
            
            # Gaming específico
            f"{username} comprou skin no Free Fire... e continua ruim.",
            f"{username} joga LoL desde 2010... ainda tá no ferro.",
            f"{username} tem PC de 30k e joga no low.",
            f"{username} tem 5000 horas de CS:GO... no casual.",
            f"{username} tem todas as skins do Valorant... mas 0% de mira.",
            f"{username} comprou battle pass... e não passou da página 1.",
            f"{username} joga Fortnite sem build... porque não sabe.",
            f"{username} morreu no Among Us sendo impostor.",
            
            # Internet/Redes sociais
            f"{username} tem TikTok... com 3 seguidores (ele, a mãe e um bot).",
            f"{username} faz tweet e ninguém curte... nem ele.",
            f"{username} tem canal no YouTube... 2 inscritos (contas fake dele).",
            f"{username} foi cancelado antes de ser relevante.",
            f"{username} postou no Instagram e perdeu seguidor.",
            f"{username} faz live... pra 0 pessoas assistindo.",
            f"{username} comentou no YouTube e tomou 50 dislikes.",
            
            # Música/Gosto
            f"{username} ouve música ruim... tipo, MUITO ruim.",
            f"{username} curte funk de 2010 e acha inovador.",
            f"{username} tem Spotify... só pra ouvir propaganda.",
            f"{username} canta no chuveiro... e o chuveiro desliga.",
            f"{username} foi num show... e a banda parou de tocar.",
            
            # Tecnologia
            f"{username} usa Internet Explorer... voluntariamente.",
            f"{username} tem celular Android 4.0 e roda pubg mobile.",
            f"{username} baixa APK de site russo.",
            f"{username} clica em 'Você ganhou um iPhone!'... todo dia.",
            f"{username} tem vírus no celular... e no PC... e na geladeira.",
            f"{username} usa Yahoo ainda.",
            f"{username} tem blog no Blogger em 2025.",
            
            # Habilidades/Talentos
            f"{username} não tem talento nem pra ser ruim.",
            f"{username} tem QI de temperatura ambiente... no Alasca.",
            f"{username} perdeu debate pra uma parede.",
            f"{username} tentou aprender algo... e desistiu do desistir.",
            f"{username} tem menos habilidade que o Aquaman em terra.",
            
            # Memes/Cultura pop
            f"{username} é tipo a 4ª temporada de uma série: ninguém pediu.",
            f"{username} é tipo episódio filler: dá pra pular.",
            f"{username} é o Jared Leto dos amigos: ninguém gosta.",
            f"{username} é tipo Minions: todo mundo odeia mas continua aparecendo.",
            f"{username} é tipo Resident Evil live-action: decepcionante.",
            
            # Zueiras gerais pesadas
            f"{username} é tipo mosquito: incomoda e ninguém quer por perto.",
            f"{username} foi a pior ideia desde 'vamos fazer Cyberpunk 2077 pra PS4'.",
            f"{username} tem cara de quem pega manga no pé com vara.",
            f"{username} é o tipo de pessoa que estraga o churrasco.",
            f"{username} come pizza de garfo e faca.",
            f"{username} morde picolé.",
            f"{username} coloca ketchup na pizza.",
            f"{username} assiste novela mexicana dublada... e chora.",
            f"{username} usa Havaianas no casamento.",
            f"{username} come pastel de feira com guardanapo.",
            f"{username} toma café requentado do dia anterior.",
            f"{username} come bolo de pote na rua.",
            f"{username} compra água no estádio.",
            f"{username} paga meia entrada mas tem 35 anos.",
            f"{username} fura fila do SUS.",
            f"{username} é tipo câmbio automático: ninguém pediu opinião.",
            f"{username} dorme de meia.",
            f"{username} acorda e não escova os dentes.",
            f"{username} usa cueca/calcinha furada.",
            f"{username} esquenta pizza no microondas.",
            f"{username} come miojo com colher.",
            f"{username} toma refrigerante quente.",
            f"{username} come macarrão instantâneo sem cozinhar.",
            f"{username} coloca leite antes do cereal.",
            f"{username} molha a escova antes da pasta.",
            f"{username} deixa a tampa da privada aberta.",
            f"{username} não lava a mão depois do banheiro.",
            f"{username} usa papel higiênico do lado errado.",
            f"{username} limpa bunda em pé.",
            f"{username} espirra sem cobrir a boca.",
            f"{username} tosse na comida.",
            f"{username} fala alto no cinema.",
            f"{username} usa celular no cinema com brilho 100%.",
            f"{username} mastiga de boca aberta.",
            f"{username} arrota sem pedir desculpas.",
            f"{username} solta pum no elevador.",
            f"{username} não dá descarga.",
            f"{username} cuspiu chiclete no chão.",
            f"{username} joga lixo pela janela do carro.",
            f"{username} buzina no trânsito sem motivo.",
            f"{username} para em fila dupla.",
            f"{username} não usa seta pra virar.",
            f"{username} dirige devagar na faixa da esquerda.",
            f"{username} solta rojão 6h da manhã.",
            f"{username} coloca som alto no carro.",
            f"{username} faz crossfit e conta pra todo mundo.",
            f"{username} é vegano e não para de falar.",
            f"{username} fala que é de humanas/exatas toda hora.",
            f"{username} posta foto de comida antes de comer.",
            f"{username} posta quote motivacional todo dia.",
            f"{username} compartilha corrente no WhatsApp.",
            f"{username} acredita em fake news.",
            f"{username} envia áudio de 5 minutos.",
            f"{username} responde 'kkkk' sem rir.",
            f"{username} dá bom dia em grupo de 200 pessoas.",
            f"{username} marca todo mundo no grupo sem motivo.",
            f"{username} sai do grupo e volta 5 minutos depois.",
            f"{username} liga ao invés de mandar mensagem.",
            f"{username} fala 'alô' por mensagem de voz.",
            f"{username} digita com caixa alta o tempo todo.",
            f"{username} usa emoji de amendoim dançando sem contexto.",
            f"{username} manda corrente de 'repasse ou algo ruim acontece'.",
            f"{username} comenta 'primeiro' em todo vídeo do YouTube.",
            f"{username} escreve 'parabéns' sem acento.",
            f"{username} confunde 'mais' com 'mas'.",
            f"{username} escreve 'vc' ao invés de 'você'.",
            f"{username} usa 'hahaha' ao invés de 'kkkkk'.",
            f"{username} manda meme de 2015 achando que é novo.",
            f"{username} ri de piada do Tiririca.",
            f"{username} ainda usa 'trollface' em 2025.",
            f"{username} fala 'owned' sem ironia.",
            f"{username} diz 'épico' pra tudo.",
            f"{username} ainda joga Clash of Clans.",
            f"{username} tem perfil no Badoo.",
            f"{username} usa ringtone de Charlie Brown Jr.",
            f"{username} tem papel de parede do Coringa.",
            f"{username} se acha vilão mas é só bobo.",
            f"{username} posta frase de Naruto no status.",
            f"{username} tem foto de anime de perfil... e não é irônico.",
            f"{username} usa ':v' sem vergonha.",
            f"{username} ainda acha Minions engraçado.",
            f"{username} manda sticker de bom dia todo santo dia.",
            f"{username} compartilha vídeo motivacional com música de fundo ruim.",
            f"{username} posta reflexão no Facebook.",
            f"{username} tem foto de carro que não é dele como capa.",
            f"{username} usa filtro de cachorrinho... aos 40 anos.",
            f"{username} posta indireta no Instagram Stories.",
            f"{username} finge que tá bem mas tá chorando.",
            f"{username} tá sempre online mas ignora mensagem.",
            f"{username} visualiza mas não responde.",
            f"{username} bloqueia sem motivo.",
            f"{username} stalkeia ex todo dia.",
            f"{username} curte foto antiga da crush... de 2012.",
            f"{username} comenta 'gata' em foto aleatória.",
            f"{username} manda 'oi sumida' pra todo mundo.",
            f"{username} puxa assunto com 'e ai, beleza?'.",
            f"{username} manda 'aceitou?' depois de adicionar.",
            f"{username} fica online mas não conversa.",
            f"{username} envia mensagem apagada mas todo mundo viu.",
            f"{username} grava áudio chorando.",
            f"{username} liga bêbado 3h da manhã.",
            f"{username} manda mensagem pro ex às 2h.",
            f"{username} dá unfollow e follow todo dia.",
            f"{username} pediu dinheiro emprestado e sumiu.",
            f"{username} deve todo mundo do grupo.",
            f"{username} prometeu pagar 'semana que vem' em 2019.",
            f"{username} usa 'depois eu pago' como lema de vida.",
            f"{username} come no rodízio e não paga.",
            f"{username} pede pra dividir a conta mas comeu mais.",
            f"{username} fura compromisso em cima da hora.",
            f"{username} chega atrasado e não avisa.",
            f"{username} marca rolê e não aparece.",
            f"{username} deixa todo mundo esperando.",
            f"{username} some quando é pra ajudar.",
            f"{username} só aparece quando precisa.",
            f"{username} é tipo Free Fire: ninguém gosta mas tá aí.",
            f"{username} tem personalidade de porta: todo mundo passa por cima.",
            f"{username} é tipo anúncio do YouTube: todo mundo pula.",
            f"{username} tem carisma de papel higiênico usado.",
            f"{username} é tipo lag: só atrapalha.",
            f"{username} tem QI negativo.",
            f"{username} deve tá pagando pau pro Elon Musk.",
            f"{username} é tipo NFT: ninguém entende pra que serve.",
            f"{username} tem habilidade social de pedra.",
            f"{username} dança pior que o tio no casamento.",
            f"{username} canta pior que gato no cio.",
            f"{username} dirige pior que minha vó.",
            f"{username} cozinha pior que miojo queimado.",
            f"{username} joga bola pior que o Gabigol no Mundial.",
            f"{username} tem timing de piada do Faustão.",
            f"{username} conta piada e ninguém ri.",
            f"{username} é tipo episódio recap de anime: ninguém quer.",
            f"{username} tem menos conteúdo que capítulo de One Piece com flashback.",
            f"{username} é tipo DLC de jogo: cobra caro e entrega nada.",
            f"{username} comprou skin de jogo e continua morrendo.",
            f"{username} tem skill de bot no recruit.",
            f"{username} é pior que time de bronze no Valorant.",
            f"{username} toma headshot até de costas.",
            f"{username} joga support e deixa o ADC morrer.",
            f"{username} compra vantagem no jogo e continua perdendo.",
            f"{username} morre pro primeiro boss do Dark Souls... no tutorial.",
            f"{username} leva dano de queda no Minecraft.",
            f"{username} morre no Fall Guys... na primeira fase.",
            f"{username} perde corrida no Mario Kart com item hack.",
            f"{username} tá travado no GTA San Andreas até hoje.",
            f"{username} não sabe fazer parkour no Assassin's Creed.",
            f"{username} tem menos aim que Stormtrooper.",
            f"{username} atira no chão no FPS.",
            f"{username} usa escudo no CS:GO... competitivo.",
            f"{username} recarrega arma no meio da troca de tiro.",
            f"{username} joga ranked e sai no meio da partida.",
            f"{username} é tipo feeder: só alimenta o inimigo.",
            f"{username} é AFK até na vida real.",
            f"{username} tem ping mental de 999.",
            f"{username} lagga até pensando.",
            f"{username} carrega mais que GTA V.",
            f"{username} bufa mais que placa de vídeo sem cooler.",
            f"{username} tem FPS negativo na vida.",
            f"{username} tem resolução de Atari 2600.",
            f"{username} roda a vida em 144p.",
            f"{username} tem gráfico pior que Minecraft.",
            f"{username} parece NPC sem textura.",
            f"{username} tem AI de pombo.",
            f"{username} bug mais que Cyberpunk no lançamento.",
            f"{username} é tipo save corrompido: perdeu tudo.",
            f"{username} precisa de patch urgente.",
            f"{username} é tipo server offline: não funciona.",
            f"{username} tem uptime pior que site da Receita.",
            f"{username} crasha mais que Windows 98.",
            f"{username} tem estabilidade de cadeira de plástico.",
            f"{username} é tipo lixeira cheia: ninguém quer esvaziar.",
            f"{username} tem backup... mas deu ruim também.",
            f"{username} foi hackeado pela própria senha.",
            f"{username} usa '123456' em tudo.",
            f"{username} salva senha no navegador... do trabalho.",
            f"{username} clica em phishing toda semana.",
            f"{username} baixa vírus achando que é hack.",
            f"{username} tem mais malware que funcionalidade.",
            f"{username} é rootkit ambulante.",
            f"{username} instalou trojan... voluntariamente.",
            f"{username} é tipo zero-day exploit: só problema.",
            f"{username} tem menos proteção que Windows XP sem firewall.",
            f"{username} é tipo backdoor: todo mundo entra.",
            f"{username} vazou os próprios dados.",
            f"{username} tem privacidade de Facebook.",
            f"{username} posta tudo no Instagram... até CPF.",
            f"{username} compartilha localização em tempo real... com hackers.",
            f"{username} é tipo cookies: todo mundo rastreia.",
            f"{username} aceita todos os termos sem ler.",
            f"{username} vende dados sem saber.",
            f"{username} usa VPN grátis e acha seguro.",
            f"{username} tem antivírus pirata cheio de vírus.",
            f"{username} clica em 'aceitar cookies' sem pensar.",
            f"{username} logou no WiFi público do aeroporto pra acessar banco.",
            f"{username} mandou nude por e-mail corporativo.",
            f"{username} gravou vídeo comprometedor e perdeu o celular.",
            f"{username} é tipo vazamento de dados: todo mundo viu.",
            f"{username} postou áudio privado no grupo de 500 pessoas.",
            f"{username} mandou mensagem pro chefe achando que era amigo.",
            f"{username} deu unfollow na mãe.",
            f"{username} brigou com o pai por mensagem.",
            f"{username} terminou namoro por WhatsApp.",
            f"{username} pediu demissão por e-mail.",
            f"{username} xingou o professor no grupo da sala.",
            f"{username} discutiu com desconhecido na internet.",
            f"{username} levou rage em jogo de criança.",
            f"{username} levou ban permanente... 5 vezes.",
            f"{username} reportou o próprio time.",
            f"{username} é tipo chat tóxico: ninguém quer ver.",
            f"{username} xinga no all chat e perde.",
            f"{username} é motivo de int do time.",
            f"{username} trollou tanto que virou lenda... negativa.",
            f"{username} tá na blacklist de todo servidor.",
            f"{username} foi kickado antes de começar.",
            f"{username} foi mutado no Discord da vida.",
            f"{username} tem mute permanente... e merecido.",
            f"{username} é tipo spammer: só incomoda.",
            f"{username} floda chat com besteira.",
            f"{username} manda corrente até no servidor de jogo.",
            f"{username} é tipo AFK permanente: não serve pra nada.",
            f"Se a idiotice gerasse energia, {username} resolveria a crise energética mundial.",
            f"A NASA está estudando {username} para entender como alguém pode ter QI negativo.",
            f"{username} é a prova viva de que a evolução às vezes dá ré.",
            f"Cientistas descobriram que {username} usa apenas 3% do cérebro... nos melhores dias.",
            f"{username} é tão especial que foi convidado a sair do grupo de WhatsApp da família.",
        ]
        
        return random.choice(roasts)
    
    async def get_brazilian_meme(self) -> Optional[Dict]:
        """Get a Brazilian meme"""
        subreddit = random.choice(self.reddit_meme_subs)
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
