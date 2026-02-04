"""General commands cog"""

import discord
from discord.ext import commands
import socket
from src.config import PREFIX


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['h'])
    async def help_command(self, ctx):
        """Show all available commands"""
        embed = discord.Embed(
            title='🎮 Bot Commands',
            description='All available commands',
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name='🎵 Music',
            value=(
                f'`{PREFIX}play <url/search>` - Play a song\n'
                f'`{PREFIX}pause` - Pause music\n'
                f'`{PREFIX}skip` - Skip song\n'
                f'`{PREFIX}queue` - Show queue\n'
                f'`{PREFIX}volume <0-100>` - Set volume'
            ),
            inline=False
        )
        
        embed.add_field(
            name='💰 Economy',
            value=(
                f'`{PREFIX}balance` - Check your balance\n'
                f'`{PREFIX}daily` - Claim daily reward\n'
                f'`{PREFIX}transfer <@user> <amount>` - Send coins\n'
                f'`{PREFIX}ranking` - Top 10 richest\n'
                f'`{PREFIX}achievements` - Your achievements'
            ),
            inline=False
        )
        
        embed.add_field(
            name='🎰 Casino',
            value=(
                f'`{PREFIX}slots <amount>` - Slot machine\n'
                f'`{PREFIX}roulette <amount> <type> <bet>` - Roulette\n'
                f'`{PREFIX}dice <amount> <type>` - Dice game\n'
                f'`{PREFIX}blackjack <amount>` - Blackjack\n'
                f'`{PREFIX}coinflip <amount> <heads/tails>` - Coin flip\n'
                f'`{PREFIX}games` - List all games'
            ),
            inline=False
        )
        
        embed.add_field(
            name='🎉 Fun',
            value=(
                f'`{PREFIX}joke` - Random joke\n'
                f'`{PREFIX}trivia` - Quiz with rewards\n'
                f'`{PREFIX}poll <min> "question" "opt1" "opt2"` - Create poll\n'
                f'`{PREFIX}8ball <question>` - Magic 8 ball'
            ),
            inline=False
        )
        
        embed.add_field(
            name='🎭 Memes',
            value=(
                f'`{PREFIX}fact` - Random fact\n'
                f'`{PREFIX}meme` - Random meme\n'
                f'`{PREFIX}memebr` - Brazilian meme\n'
                f'`{PREFIX}topmeme` - Top memes'
            ),
            inline=False
        )
        
        embed.add_field(
            name='📊 Info',
            value=(
                f'`{PREFIX}history` - Transaction history\n'
                f'`{PREFIX}help` - This menu'
            ),
            inline=False
        )
        
        embed.set_footer(text=f'Use {PREFIX}<command>')
        await ctx.send(embed=embed)
    
    @commands.command(name='ping', aliases=['latency'])
    async def ping(self, ctx):
        """Show bot latency and info"""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title='🏓 Pong!',
            color=discord.Color.green()
        )
        embed.add_field(name='Latency', value=f'{latency}ms', inline=True)
        embed.add_field(name='Servers', value=len(self.bot.guilds), inline=True)
        embed.add_field(name='Host', value=socket.gethostname(), inline=True)
        
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(General(bot))
