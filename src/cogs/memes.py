"""Memes and fun image commands cog"""

import discord
from discord.ext import commands
from src.fun.memes import MemeManager


class Memes(commands.Cog):
    """Meme commands - funny images from the internet"""
    
    def __init__(self, bot):
        self.bot = bot
        self.memes = MemeManager()
    
    @commands.command(name='fato', aliases=['fact', 'curiosidade'])
    async def fact(self, ctx):
        """Compartilha uma curiosidade engraçada"""
        fact = self.memes.get_random_fact()
        
        embed = discord.Embed(
            title='💡 Curiosidade Aleatória',
            description=fact,
            color=discord.Color.blue()
        )
        
        embed.set_footer(text='Será que é verdade? 🤔')
        await ctx.send(embed=embed)
    
    @commands.command(name='meme', aliases=['randommeme', 'memealeatório', 'memealeat'])
    async def random_meme(self, ctx):
        """Envia um meme aleatório"""
        await ctx.typing()
        
        meme = await self.memes.fetch_reddit_meme()
        
        if meme:
            embed = discord.Embed(
                title=f'😂 {meme["title"][:200]}',
                color=discord.Color.gold()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • {meme["score"]} ⬆️')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não consegui encontrar um meme no momento. Tente novamente!')
    
    @commands.command(name='memede2025', aliases=['meme2025', 'meme-2025', 'meme_2025'])
    async def meme_2025(self, ctx):
        """Envia um meme da moda em 2025"""
        await ctx.typing()
        
        meme = await self.memes.get_meme_by_category('2025')
        
        if meme:
            embed = discord.Embed(
                title=f'🔥 Meme 2025: {meme["title"][:180]}',
                color=discord.Color.orange()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • Trending 2025 🚀')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não consegui encontrar um meme 2025. Tente /meme!')
    
    @commands.command(name='memedodia', aliases=['meme-do-dia', 'meme_do_dia', 'dailymeme'])
    async def meme_do_dia(self, ctx):
        """Mostra o meme do dia"""
        await ctx.typing()
        
        meme = await self.memes.get_daily_meme()
        
        if meme:
            embed = discord.Embed(
                title=f'📅 Meme do Dia: {meme["title"][:180]}',
                color=discord.Color.purple()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • Meme oficial do dia!')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não consegui buscar o meme do dia. Tente /randommeme!')
    
    @commands.command(name='memedesucesso', aliases=['meme-sucesso', 'memesucesso', 'memesucesso'])
    async def meme_sucesso(self, ctx):
        """Mostra um meme de sucesso do momento"""
        await ctx.typing()
        
        meme = await self.memes.get_meme_by_category('sucesso')
        
        if meme:
            embed = discord.Embed(
                title=f'✨ Sucesso: {meme["title"][:180]}',
                color=discord.Color.green()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • Motivação! 💪')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não encontrei memes de sucesso. Tente /meme!')
    
    @commands.command(name='memedefracasso', aliases=['meme-fracasso', 'memefracasso'])
    async def meme_fracasso(self, ctx):
        """Mostra um meme de fracasso do momento"""
        await ctx.typing()
        
        meme = await self.memes.get_meme_by_category('fracasso')
        
        if meme:
            embed = discord.Embed(
                title=f'💀 Fracasso: {meme["title"][:180]}',
                color=discord.Color.red()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • F no chat 😅')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não encontrei memes de fracasso. Tente /meme!')
    
    @commands.command(name='memedetroll', aliases=['meme-troll', 'troll'])
    async def meme_troll(self, ctx):
        """Envia um meme de troll"""
        await ctx.typing()
        
        meme = await self.memes.get_meme_by_category('troll')
        
        if meme:
            embed = discord.Embed(
                title=f'😈 Troll: {meme["title"][:180]}',
                color=discord.Color.dark_red()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • Problem? 😏')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não encontrei memes de troll. Tente /meme!')
    
    @commands.command(name='memedezoacao', aliases=['meme-zoacao', 'zoacao', 'zoeira'])
    async def meme_zoacao(self, ctx):
        """Envia um meme de zoação"""
        await ctx.typing()
        
        meme = await self.memes.get_meme_by_category('zoacao')
        
        if meme:
            embed = discord.Embed(
                title=f'🤪 Zoação: {meme["title"][:180]}',
                color=discord.Color.gold()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • É zueira! 😂')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não encontrei memes de zoação. Tente /meme!')
    
    @commands.command(name='memebr', aliases=['meme-br', 'memebrasil'])
    async def meme_brasileiro(self, ctx):
        """Envia um meme brasileiro"""
        await ctx.typing()
        
        meme = await self.memes.get_brazilian_meme()
        
        if meme:
            embed = discord.Embed(
                title=f'🇧🇷 {meme["title"][:200]}',
                color=discord.Color.green()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • Meme raiz BR!')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não encontrei memes BR. Tente /meme!')
    
    @commands.command(name='topmeme', aliases=['top-meme', 'memetop'])
    async def top_meme(self, ctx):
        """Envia um dos memes mais votados de hoje"""
        await ctx.typing()
        
        meme = await self.memes.get_top_meme()
        
        if meme:
            embed = discord.Embed(
                title=f'🏆 Top Meme: {meme["title"][:180]}',
                color=discord.Color.gold()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • {meme["score"]:,} ⬆️ • Top de hoje!')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não consegui buscar top memes. Tente /meme!')


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(Memes(bot))
