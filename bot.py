import discord
from discord.ext import commands
import asyncio
import yt_dlp as youtube_dl
import os
from dotenv import load_dotenv
from collections import deque
import random

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '!')

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Bot instance
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# YouTube DL options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'extract_flat': False,
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')
        self.thumbnail = data.get('thumbnail')
        self.requester = None

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        try:
            data = await asyncio.wait_for(
                loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream)),
                timeout=60.0  # 60 second timeout
            )
        except asyncio.TimeoutError:
            raise Exception("A busca demorou muito tempo. Tente novamente.")

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class MusicQueue:
    def __init__(self):
        self.queue = deque()
        self.current = None
        self.volume = 0.5

    def add(self, song):
        self.queue.append(song)

    def get_next(self):
        if self.queue:
            self.current = self.queue.popleft()
            return self.current
        return None

    def clear(self):
        self.queue.clear()
        self.current = None

    def shuffle(self):
        temp_list = list(self.queue)
        random.shuffle(temp_list)
        self.queue = deque(temp_list)

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


# Dictionary to store music queues for each guild
music_queues = {}


def get_queue(guild_id):
    if guild_id not in music_queues:
        music_queues[guild_id] = MusicQueue()
    return music_queues[guild_id]


async def play_next(ctx):
    """Play the next song in the queue"""
    queue = get_queue(ctx.guild.id)
    
    if queue.is_empty():
        await ctx.send('🎵 A fila acabou! Use `!play` para adicionar mais músicas.')
        return

    next_song = queue.get_next()
    if next_song:
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_connected():
            def after_playing(error):
                if error:
                    print(f'Erro ao reproduzir: {error}')
                asyncio.run_coroutine_threadsafe(play_next(ctx), asyncio.get_event_loop())
            
            voice_client.play(next_song, after=after_playing)
            next_song.volume = queue.volume
            
            embed = discord.Embed(
                title='🎵 Tocando Agora',
                description=f'[{next_song.title}]({next_song.data.get("webpage_url", "")})',
                color=discord.Color.green()
            )
            if next_song.thumbnail:
                embed.set_thumbnail(url=next_song.thumbnail)
            if next_song.duration:
                minutes, seconds = divmod(next_song.duration, 60)
                embed.add_field(name='Duração', value=f'{int(minutes)}:{int(seconds):02d}')
            embed.add_field(name='Volume', value=f'{int(queue.volume * 100)}%')
            if next_song.requester:
                embed.set_footer(text=f'Pedido por {next_song.requester}')
            
            await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f'🤖 Bot conectado como {bot.user.name}')
    print(f'📊 ID: {bot.user.id}')
    print(f'🎵 Bot de música Macacolândia está online!')
    print('------')
    await bot.change_presence(activity=discord.Game(name=f'{PREFIX}help | Música 🎵'))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'❌ Argumento faltando! Use `{PREFIX}help` para ver os comandos.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f'❌ Comando não encontrado! Use `{PREFIX}help` para ver os comandos disponíveis.')
    else:
        await ctx.send(f'❌ Ocorreu um erro: {str(error)}')


@bot.command(name='help', aliases=['ajuda', 'h'])
async def help_command(ctx):
    """Mostra todos os comandos disponíveis"""
    embed = discord.Embed(
        title='🎵 Bot de Música Macacolândia - Comandos',
        description='Aqui estão todos os comandos disponíveis:',
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name='🎵 Reprodução',
        value=(
            f'`{PREFIX}play <url/busca>` - Toca uma música\n'
            f'`{PREFIX}pause` - Pausa a música atual\n'
            f'`{PREFIX}resume` - Retoma a música pausada\n'
            f'`{PREFIX}stop` - Para a música e limpa a fila\n'
            f'`{PREFIX}skip` - Pula para a próxima música\n'
            f'`{PREFIX}leave` - Desconecta o bot do canal'
        ),
        inline=False
    )
    
    embed.add_field(
        name='🔊 Volume',
        value=(
            f'`{PREFIX}volume <0-100>` - Define o volume\n'
            f'`{PREFIX}volumeup` - Aumenta o volume em 10%\n'
            f'`{PREFIX}volumedown` - Diminui o volume em 10%'
        ),
        inline=False
    )
    
    embed.add_field(
        name='📋 Fila',
        value=(
            f'`{PREFIX}queue` - Mostra a fila de músicas\n'
            f'`{PREFIX}nowplaying` - Mostra a música atual\n'
            f'`{PREFIX}clear` - Limpa a fila\n'
            f'`{PREFIX}shuffle` - Embaralha a fila'
        ),
        inline=False
    )
    
    embed.set_footer(text=f'Use {PREFIX}comando para executar um comando')
    await ctx.send(embed=embed)


@bot.command(name='play', aliases=['p', 'tocar'])
async def play(ctx, *, url_or_search: str):
    """Toca uma música a partir de uma URL ou busca"""
    
    # Check if user is in a voice channel
    if not ctx.author.voice:
        await ctx.send('❌ Você precisa estar em um canal de voz!')
        return

    # Connect to voice channel if not connected
    if not ctx.voice_client:
        channel = ctx.author.voice.channel
        await channel.connect()
    elif ctx.voice_client.channel != ctx.author.voice.channel:
        await ctx.voice_client.move_to(ctx.author.voice.channel)

    async with ctx.typing():
        try:
            # Add 'ytsearch:' prefix if it's not a URL
            if not url_or_search.startswith('http'):
                url_or_search = f'ytsearch:{url_or_search}'
            
            player = await YTDLSource.from_url(url_or_search, loop=bot.loop, stream=True)
            player.requester = ctx.author.name
            
            queue = get_queue(ctx.guild.id)
            
            # If nothing is playing, play immediately
            if not ctx.voice_client.is_playing():
                queue.current = player
                player.volume = queue.volume
                
                def after_playing(error):
                    if error:
                        print(f'Erro ao reproduzir: {error}')
                    asyncio.run_coroutine_threadsafe(play_next(ctx), asyncio.get_event_loop())
                
                ctx.voice_client.play(player, after=after_playing)
                
                embed = discord.Embed(
                    title='🎵 Tocando Agora',
                    description=f'[{player.title}]({player.data.get("webpage_url", "")})',
                    color=discord.Color.green()
                )
                if player.thumbnail:
                    embed.set_thumbnail(url=player.thumbnail)
                if player.duration:
                    minutes, seconds = divmod(player.duration, 60)
                    embed.add_field(name='Duração', value=f'{int(minutes)}:{int(seconds):02d}')
                embed.add_field(name='Volume', value=f'{int(queue.volume * 100)}%')
                embed.set_footer(text=f'Pedido por {ctx.author.name}')
                
                await ctx.send(embed=embed)
            else:
                # Add to queue
                queue.add(player)
                embed = discord.Embed(
                    title='📋 Adicionado à Fila',
                    description=f'[{player.title}]({player.data.get("webpage_url", "")})',
                    color=discord.Color.orange()
                )
                if player.thumbnail:
                    embed.set_thumbnail(url=player.thumbnail)
                embed.add_field(name='Posição na fila', value=f'#{queue.size()}')
                embed.set_footer(text=f'Pedido por {ctx.author.name}')
                
                await ctx.send(embed=embed)
                
        except asyncio.TimeoutError:
            await ctx.send('❌ A busca demorou muito tempo. Tente novamente.')
        except Exception as e:
            print(f'Erro ao carregar música: {str(e)}')
            await ctx.send('❌ Não foi possível carregar a música. Verifique a URL ou tente outra busca.')


@bot.command(name='pause', aliases=['pausar'])
async def pause(ctx):
    """Pausa a música atual"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send('⏸️ Música pausada!')
    else:
        await ctx.send('❌ Nenhuma música está tocando no momento.')


@bot.command(name='resume', aliases=['retomar', 'continuar'])
async def resume(ctx):
    """Retoma a música pausada"""
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send('▶️ Música retomada!')
    else:
        await ctx.send('❌ Nenhuma música está pausada.')


@bot.command(name='stop', aliases=['parar'])
async def stop(ctx):
    """Para a música e limpa a fila"""
    if ctx.voice_client:
        queue = get_queue(ctx.guild.id)
        queue.clear()
        ctx.voice_client.stop()
        await ctx.send('⏹️ Música parada e fila limpa!')
    else:
        await ctx.send('❌ O bot não está em um canal de voz.')


@bot.command(name='skip', aliases=['pular', 's'])
async def skip(ctx):
    """Pula para a próxima música"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send('⏭️ Música pulada!')
    else:
        await ctx.send('❌ Nenhuma música está tocando no momento.')


@bot.command(name='volume', aliases=['vol', 'v'])
async def volume(ctx, volume: int):
    """Define o volume (0-100)"""
    if not ctx.voice_client:
        await ctx.send('❌ O bot não está em um canal de voz.')
        return

    if not 0 <= volume <= 100:
        await ctx.send('❌ O volume deve estar entre 0 e 100!')
        return

    queue = get_queue(ctx.guild.id)
    queue.volume = volume / 100
    
    if ctx.voice_client.source:
        ctx.voice_client.source.volume = queue.volume

    await ctx.send(f'🔊 Volume definido para {volume}%!')


@bot.command(name='volumeup', aliases=['volup', 'v+', 'aumentar'])
async def volume_up(ctx):
    """Aumenta o volume em 10%"""
    if not ctx.voice_client:
        await ctx.send('❌ O bot não está em um canal de voz.')
        return

    queue = get_queue(ctx.guild.id)
    new_volume = min(1.0, queue.volume + 0.1)
    queue.volume = new_volume
    
    if ctx.voice_client.source:
        ctx.voice_client.source.volume = queue.volume

    await ctx.send(f'🔊 Volume aumentado para {int(new_volume * 100)}%!')


@bot.command(name='volumedown', aliases=['voldown', 'v-', 'diminuir'])
async def volume_down(ctx):
    """Diminui o volume em 10%"""
    if not ctx.voice_client:
        await ctx.send('❌ O bot não está em um canal de voz.')
        return

    queue = get_queue(ctx.guild.id)
    new_volume = max(0.0, queue.volume - 0.1)
    queue.volume = new_volume
    
    if ctx.voice_client.source:
        ctx.voice_client.source.volume = queue.volume

    await ctx.send(f'🔊 Volume diminuído para {int(new_volume * 100)}%!')


@bot.command(name='queue', aliases=['q', 'fila'])
async def queue_command(ctx):
    """Mostra a fila de músicas"""
    queue = get_queue(ctx.guild.id)
    
    if queue.current is None and queue.is_empty():
        await ctx.send('📋 A fila está vazia!')
        return

    embed = discord.Embed(
        title='📋 Fila de Músicas',
        color=discord.Color.purple()
    )

    if queue.current:
        embed.add_field(
            name='🎵 Tocando Agora',
            value=f'[{queue.current.title}]({queue.current.data.get("webpage_url", "")})',
            inline=False
        )

    if not queue.is_empty():
        queue_list = []
        for i, song in enumerate(list(queue.queue)[:10], 1):
            queue_list.append(f'{i}. [{song.title}]({song.data.get("webpage_url", "")})')
        
        embed.add_field(
            name=f'🎼 Próximas ({queue.size()} músicas)',
            value='\n'.join(queue_list) if queue_list else 'Nenhuma música na fila',
            inline=False
        )
        
        if queue.size() > 10:
            embed.set_footer(text=f'E mais {queue.size() - 10} músicas...')

    await ctx.send(embed=embed)


@bot.command(name='nowplaying', aliases=['np', 'tocando', 'atual'])
async def now_playing(ctx):
    """Mostra a música que está tocando agora"""
    queue = get_queue(ctx.guild.id)
    
    if queue.current is None:
        await ctx.send('❌ Nenhuma música está tocando no momento.')
        return

    song = queue.current
    embed = discord.Embed(
        title='🎵 Tocando Agora',
        description=f'[{song.title}]({song.data.get("webpage_url", "")})',
        color=discord.Color.green()
    )
    
    if song.thumbnail:
        embed.set_thumbnail(url=song.thumbnail)
    
    if song.duration:
        minutes, seconds = divmod(song.duration, 60)
        embed.add_field(name='Duração', value=f'{int(minutes)}:{int(seconds):02d}')
    
    embed.add_field(name='Volume', value=f'{int(queue.volume * 100)}%')
    
    if song.requester:
        embed.set_footer(text=f'Pedido por {song.requester}')

    await ctx.send(embed=embed)


@bot.command(name='clear', aliases=['limpar', 'clearqueue'])
async def clear_queue(ctx):
    """Limpa a fila de músicas"""
    queue = get_queue(ctx.guild.id)
    queue.clear()
    await ctx.send('🗑️ Fila limpa!')


@bot.command(name='shuffle', aliases=['embaralhar', 'misturar'])
async def shuffle_queue(ctx):
    """Embaralha a fila de músicas"""
    queue = get_queue(ctx.guild.id)
    
    if queue.is_empty():
        await ctx.send('❌ A fila está vazia!')
        return

    queue.shuffle()
    await ctx.send('🔀 Fila embaralhada!')


@bot.command(name='leave', aliases=['disconnect', 'sair', 'desconectar'])
async def leave(ctx):
    """Desconecta o bot do canal de voz"""
    if ctx.voice_client:
        queue = get_queue(ctx.guild.id)
        queue.clear()
        await ctx.voice_client.disconnect()
        await ctx.send('👋 Desconectado do canal de voz!')
    else:
        await ctx.send('❌ O bot não está em um canal de voz.')


# Run the bot
if __name__ == '__main__':
    if not TOKEN:
        print('❌ ERRO: Token do Discord não encontrado!')
        print('Por favor, crie um arquivo .env com seu DISCORD_TOKEN')
    else:
        bot.run(TOKEN)
