"""Music commands cog - All music playback and queue management commands"""

import discord
from discord.ext import commands
import asyncio
from src.music.source import YTDLSource
from src.music.queue import MusicQueue
from src.config import PREFIX


# Dictionary to store music queues for each guild
music_queues = {}


def get_queue(guild_id):
    """Get or create a music queue for a guild"""
    if guild_id not in music_queues:
        music_queues[guild_id] = MusicQueue()
    return music_queues[guild_id]


class Music(commands.Cog):
    """Music playback commands"""
    
    def __init__(self, bot):
        self.bot = bot

    async def play_next(self, ctx):
        """Play the next song in the queue"""
        queue = get_queue(ctx.guild.id)
        
        if queue.is_empty():
            await ctx.send(f'🎵 A fila acabou! Use `{PREFIX}play` para adicionar mais músicas.')
            return

        next_song = queue.get_next()
        if next_song:
            voice_client = ctx.voice_client
            if voice_client and voice_client.is_connected():
                def after_playing(error):
                    if error:
                        print(f'Erro ao reproduzir: {error}')
                    asyncio.run_coroutine_threadsafe(self.play_next(ctx), asyncio.get_event_loop())
                
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

    @commands.command(name='play', aliases=['p', 'tocar'])
    async def play(self, ctx, *, url_or_search: str):
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
                
                player = await YTDLSource.from_url(url_or_search, loop=self.bot.loop, stream=True)
                player.requester = ctx.author.name
                
                queue = get_queue(ctx.guild.id)
                
                # If nothing is playing, play immediately
                if not ctx.voice_client.is_playing():
                    queue.current = player
                    player.volume = queue.volume
                    
                    def after_playing(error):
                        if error:
                            print(f'Erro ao reproduzir: {error}')
                        asyncio.run_coroutine_threadsafe(self.play_next(ctx), asyncio.get_event_loop())
                    
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

    @commands.command(name='pause', aliases=['pausar'])
    async def pause(self, ctx):
        """Pausa a música atual"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('⏸️ Música pausada!')
        else:
            await ctx.send('❌ Nenhuma música está tocando no momento.')

    @commands.command(name='resume', aliases=['retomar', 'continuar'])
    async def resume(self, ctx):
        """Retoma a música pausada"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('▶️ Música retomada!')
        else:
            await ctx.send('❌ Nenhuma música está pausada.')

    @commands.command(name='stop', aliases=['parar'])
    async def stop(self, ctx):
        """Para a música e limpa a fila"""
        if ctx.voice_client:
            queue = get_queue(ctx.guild.id)
            queue.clear()
            ctx.voice_client.stop()
            await ctx.send('⏹️ Música parada e fila limpa!')
        else:
            await ctx.send('❌ O bot não está em um canal de voz.')

    @commands.command(name='skip', aliases=['pular', 's'])
    async def skip(self, ctx):
        """Pula para a próxima música"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('⏭️ Música pulada!')
        else:
            await ctx.send('❌ Nenhuma música está tocando no momento.')

    @commands.command(name='volume', aliases=['vol', 'v'])
    async def volume(self, ctx, volume: int):
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

    @commands.command(name='volumeup', aliases=['volup', 'v+', 'aumentar'])
    async def volume_up(self, ctx):
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

    @commands.command(name='volumedown', aliases=['voldown', 'v-', 'diminuir'])
    async def volume_down(self, ctx):
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

    @commands.command(name='queue', aliases=['q', 'fila'])
    async def queue_command(self, ctx):
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

    @commands.command(name='nowplaying', aliases=['np', 'tocando', 'atual'])
    async def now_playing(self, ctx):
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

    @commands.command(name='clear', aliases=['limpar', 'clearqueue'])
    async def clear_queue(self, ctx):
        """Limpa a fila de músicas"""
        queue = get_queue(ctx.guild.id)
        queue.clear()
        await ctx.send('🗑️ Fila limpa!')

    @commands.command(name='shuffle', aliases=['embaralhar', 'misturar'])
    async def shuffle_queue(self, ctx):
        """Embaralha a fila de músicas"""
        queue = get_queue(ctx.guild.id)
        
        if queue.is_empty():
            await ctx.send('❌ A fila está vazia!')
            return

        queue.shuffle()
        await ctx.send('🔀 Fila embaralhada!')

    @commands.command(name='leave', aliases=['disconnect', 'sair', 'desconectar'])
    async def leave(self, ctx):
        """Desconecta o bot do canal de voz"""
        if ctx.voice_client:
            queue = get_queue(ctx.guild.id)
            queue.clear()
            await ctx.voice_client.disconnect()
            await ctx.send('👋 Desconectado do canal de voz!')
        else:
            await ctx.send('❌ O bot não está em um canal de voz.')


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(Music(bot))
