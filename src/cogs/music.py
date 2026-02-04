"""Music commands cog"""

import discord
from discord.ext import commands
import asyncio
from src.music.source import YTDLSource
from src.music.queue import MusicQueue
from src.config import PREFIX

music_queues = {}


def get_queue(guild_id):
    if guild_id not in music_queues:
        music_queues[guild_id] = MusicQueue()
    return music_queues[guild_id]


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def play_next(self, ctx):
        queue = get_queue(ctx.guild.id)
        
        if queue.is_empty():
            await ctx.send(f'🎵 Queue is empty! Use `{PREFIX}play` to add more songs.')
            return

        next_song = queue.get_next()
        if next_song:
            voice_client = ctx.voice_client
            if voice_client and voice_client.is_connected():
                def after_playing(error):
                    if error:
                        print(f'Playback error: {error}')
                    asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)
                
                voice_client.play(next_song, after=after_playing)
                next_song.volume = queue.volume
                
                embed = discord.Embed(
                    title='🎵 Now Playing',
                    description=f'[{next_song.title}]({next_song.data.get("webpage_url", "")})',
                    color=discord.Color.green()
                )
                if next_song.thumbnail:
                    embed.set_thumbnail(url=next_song.thumbnail)
                if next_song.duration:
                    minutes, seconds = divmod(next_song.duration, 60)
                    embed.add_field(name='Duration', value=f'{int(minutes)}:{int(seconds):02d}')
                embed.add_field(name='Volume', value=f'{int(queue.volume * 100)}%')
                if next_song.requester:
                    embed.set_footer(text=f'Requested by {next_song.requester}')
                
                await ctx.send(embed=embed)

    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx, *, url_or_search: str):
        """Play a song from URL or search"""
        if not ctx.author.voice:
            await ctx.send('❌ You need to be in a voice channel!')
            return

        if not ctx.voice_client:
            channel = ctx.author.voice.channel
            await channel.connect()
        elif ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.voice_client.move_to(ctx.author.voice.channel)

        async with ctx.typing():
            try:
                if not url_or_search.startswith('http'):
                    url_or_search = f'ytsearch:{url_or_search}'
                
                player = await YTDLSource.from_url(url_or_search, loop=self.bot.loop, stream=True)
                player.requester = ctx.author.name
                
                queue = get_queue(ctx.guild.id)
                
                if not ctx.voice_client.is_playing():
                    queue.current = player
                    player.volume = queue.volume
                    
                    def after_playing(error):
                        if error:
                            print(f'Playback error: {error}')
                        asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)
                    
                    ctx.voice_client.play(player, after=after_playing)
                    
                    embed = discord.Embed(
                        title='🎵 Now Playing',
                        description=f'[{player.title}]({player.data.get("webpage_url", "")})',
                        color=discord.Color.green()
                    )
                    if player.thumbnail:
                        embed.set_thumbnail(url=player.thumbnail)
                    if player.duration:
                        minutes, seconds = divmod(player.duration, 60)
                        embed.add_field(name='Duration', value=f'{int(minutes)}:{int(seconds):02d}')
                    embed.add_field(name='Volume', value=f'{int(queue.volume * 100)}%')
                    embed.set_footer(text=f'Requested by {ctx.author.name}')
                    
                    await ctx.send(embed=embed)
                else:
                    queue.add(player)
                    embed = discord.Embed(
                        title='📋 Added to Queue',
                        description=f'[{player.title}]({player.data.get("webpage_url", "")})',
                        color=discord.Color.orange()
                    )
                    if player.thumbnail:
                        embed.set_thumbnail(url=player.thumbnail)
                    embed.add_field(name='Position', value=f'#{queue.size()}')
                    embed.set_footer(text=f'Requested by {ctx.author.name}')
                    
                    await ctx.send(embed=embed)
                    
            except asyncio.TimeoutError:
                await ctx.send('❌ Timed out! Try again.')
            except Exception as e:
                error_msg = str(e).lower()
                print(f'Error loading song: {str(e)}')
                
                if 'sign in' in error_msg or 'login' in error_msg or 'bot' in error_msg:
                    embed = discord.Embed(
                        title='❌ YouTube Blocked!',
                        description='YouTube is requesting login or detected bot.',
                        color=discord.Color.red()
                    )
                    embed.add_field(
                        name='🔧 Solutions:',
                        value=(
                            '**1. Try searching instead of URL:**\n'
                            f'`{PREFIX}play song name`\n\n'
                            '**2. Or login to Chrome/Edge:**\n'
                            '• Open youtube.com in browser\n'
                            '• Login to your account\n'
                            '• Restart the bot\n\n'
                            '**3. Try another song**'
                        ),
                        inline=False
                    )
                    await ctx.send(embed=embed)
                elif 'unavailable' in error_msg or 'not available' in error_msg:
                    await ctx.send('❌ This song is unavailable! Try another.')
                elif 'copyright' in error_msg:
                    await ctx.send('❌ This song is blocked by copyright! Try another.')
                else:
                    await ctx.send(f'❌ Error loading song. Check the URL or try another search.\n\n**Error:** {str(e)[:150]}')

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pause current song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send('⏸️ Paused!')
        else:
            await ctx.send('❌ Nothing is playing.')

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resume paused song"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send('▶️ Resumed!')
        else:
            await ctx.send('❌ Nothing is paused.')

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stop music and clear queue"""
        if ctx.voice_client:
            queue = get_queue(ctx.guild.id)
            queue.clear()
            ctx.voice_client.stop()
            await ctx.send('⏹️ Stopped and cleared queue!')
        else:
            await ctx.send('❌ Not in a voice channel.')

    @commands.command(name='skip', aliases=['s'])
    async def skip(self, ctx):
        """Skip to next song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send('⏭️ Skipped!')
        else:
            await ctx.send('❌ Nothing is playing.')

    @commands.command(name='volume', aliases=['vol'])
    async def volume(self, ctx, volume: int):
        """Set volume (0-100)"""
        if not ctx.voice_client:
            await ctx.send('❌ Bot is not in a voice channel.')
            return

        if not 0 <= volume <= 100:
            await ctx.send('❌ Volume must be between 0 and 100!')
            return

        queue = get_queue(ctx.guild.id)
        queue.volume = volume / 100
        
        if ctx.voice_client.source:
            ctx.voice_client.source.volume = queue.volume

        await ctx.send(f'🔊 Volume set to {volume}%!')

    @commands.command(name='volumeup', aliases=['v+'])
    async def volume_up(self, ctx):
        """Increase volume by 10%"""
        if not ctx.voice_client:
            await ctx.send('❌ Bot is not in a voice channel.')
            return

        queue = get_queue(ctx.guild.id)
        new_volume = min(1.0, queue.volume + 0.1)
        queue.volume = new_volume
        
        if ctx.voice_client.source:
            ctx.voice_client.source.volume = queue.volume

        await ctx.send(f'🔊 Volume increased to {int(new_volume * 100)}%!')

    @commands.command(name='volumedown', aliases=['v-'])
    async def volume_down(self, ctx):
        """Decrease volume by 10%"""
        if not ctx.voice_client:
            await ctx.send('❌ Bot is not in a voice channel.')
            return

        queue = get_queue(ctx.guild.id)
        new_volume = max(0.0, queue.volume - 0.1)
        queue.volume = new_volume
        
        if ctx.voice_client.source:
            ctx.voice_client.source.volume = queue.volume

        await ctx.send(f'🔊 Volume decreased to {int(new_volume * 100)}%!')

    @commands.command(name='queue', aliases=['q'])
    async def queue_command(self, ctx):
        """Show music queue"""
        queue = get_queue(ctx.guild.id)
        
        if queue.current is None and queue.is_empty():
            await ctx.send('📋 Queue is empty!')
            return

        embed = discord.Embed(title='📋 Music Queue', color=discord.Color.purple())

        if queue.current:
            embed.add_field(
                name='🎵 Now Playing',
                value=f'[{queue.current.title}]({queue.current.data.get("webpage_url", "")})',
                inline=False
            )

        if not queue.is_empty():
            queue_list = []
            for i, song in enumerate(list(queue.queue)[:10], 1):
                queue_list.append(f'{i}. [{song.title}]({song.data.get("webpage_url", "")})')
            
            embed.add_field(
                name=f'🎼 Up Next ({queue.size()} songs)',
                value='\n'.join(queue_list) if queue_list else 'No songs in queue',
                inline=False
            )
            
            if queue.size() > 10:
                embed.set_footer(text=f'And {queue.size() - 10} more...')

        await ctx.send(embed=embed)

    @commands.command(name='nowplaying', aliases=['np'])
    async def now_playing(self, ctx):
        """Show currently playing song"""
        queue = get_queue(ctx.guild.id)
        
        if queue.current is None:
            await ctx.send('❌ No song is playing.')
            return

        song = queue.current
        embed = discord.Embed(
            title='🎵 Now Playing',
            description=f'[{song.title}]({song.data.get("webpage_url", "")})',
            color=discord.Color.green()
        )
        
        if song.thumbnail:
            embed.set_thumbnail(url=song.thumbnail)
        
        if song.duration:
            minutes, seconds = divmod(song.duration, 60)
            embed.add_field(name='Duration', value=f'{int(minutes)}:{int(seconds):02d}')
        
        embed.add_field(name='Volume', value=f'{int(queue.volume * 100)}%')
        
        if song.requester:
            embed.set_footer(text=f'Requested by {song.requester}')

        await ctx.send(embed=embed)

    @commands.command(name='clear')
    async def clear_queue(self, ctx):
        """Clear the queue"""
        queue = get_queue(ctx.guild.id)
        queue.clear()
        await ctx.send('🗑️ Queue cleared!')

    @commands.command(name='shuffle')
    async def shuffle_queue(self, ctx):
        """Shuffle the queue"""
        queue = get_queue(ctx.guild.id)
        
        if queue.is_empty():
            await ctx.send('❌ Queue is empty!')
            return

        queue.shuffle()
        await ctx.send('🔀 Queue shuffled!')

    @commands.command(name='leave', aliases=['disconnect'])
    async def leave(self, ctx):
        """Disconnect from voice channel"""
        if ctx.voice_client:
            queue = get_queue(ctx.guild.id)
            queue.clear()
            await ctx.voice_client.disconnect()
            await ctx.send('👋 Disconnected from voice channel!')
        else:
            await ctx.send('❌ Bot is not in a voice channel.')


async def setup(bot):
    await bot.add_cog(Music(bot))
