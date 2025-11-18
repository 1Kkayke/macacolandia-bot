"""Memes and fun image commands cog"""

import discord
from discord.ext import commands
from src.fun.memes import MemeManager


class Memes(commands.Cog):
    """Meme commands - funny images from the internet"""
    
    def __init__(self, bot):
        self.bot = bot
        self.memes = MemeManager()
    
    @commands.command(name='fato', aliases=['fact', 'curiosidade', 'fatos'])
    async def fact(self, ctx, user: discord.Member = None):
        """Compartilha uma curiosidade engraçada ou fato sobre um usuário"""
        
        if user is None:
            # Fato aleatório normal
            fact = self.memes.get_random_fact()
            
            embed = discord.Embed(
                title='💡 Fato Aleatório (será?)',
                description=fact,
                color=discord.Color.blue()
            )
            embed.set_footer(text='Será que é verdade? Vai saber né kkk 🤔')
        else:
            # Fato engraçado/pesado sobre o usuário
            roast = self.memes.get_random_roast(user.display_name)
            
            embed = discord.Embed(
                title=f'🔥 Fato sobre o {user.display_name}',
                description=roast,
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.set_footer(text='É zueira caralho, relaxa! 😂')
        
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
            embed.set_footer(text=f'r/{meme["subreddit"]} • {meme["score"]} ⬆️ | Pegado da net')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não achei meme agora não caralho! Tenta de novo.')
    
    @commands.command(name='memede2025', aliases=['meme2025', 'meme-2025', 'meme_2025'])
    async def meme_2025(self, ctx):
        """Envia um meme da moda em 2025"""
        await ctx.typing()
        
        meme = await self.memes.get_meme_by_category('2025')
        
        if meme:
            embed = discord.Embed(
                title=f'🔥 Meme 2025: {meme["title"][:180]}',
                description='Meme atualizado pra 2025 caralho!',
                color=discord.Color.orange()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • Trending 2025 🚀')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não achei meme de 2025 não! Tenta /meme mano.')
    
    @commands.command(name='memedodia', aliases=['meme-do-dia', 'meme_do_dia', 'dailymeme'])
    async def meme_do_dia(self, ctx):
        """Mostra o meme do dia"""
        await ctx.typing()
        
        meme = await self.memes.get_daily_meme()
        
        if meme:
            embed = discord.Embed(
                title=f'📅 Meme do Dia: {meme["title"][:180]}',
                description='O meme oficial de hoje caralho!',
                color=discord.Color.purple()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • Meme do dia porra!')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não achei o meme do dia não! Tenta /meme mano.')
    
    @commands.command(name='memedesucesso', aliases=['meme-sucesso', 'memesucesso'])
    async def meme_sucesso(self, ctx):
        """Mostra um meme de sucesso do momento"""
        await ctx.typing()
        
        meme = await self.memes.get_meme_by_category('sucesso')
        
        if meme:
            embed = discord.Embed(
                title=f'✨ Sucesso: {meme["title"][:180]}',
                description='Meme motivacional pra tu se sentir bem!',
                color=discord.Color.green()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • Motivação fdp! 💪')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não achei meme de sucesso não! Tenta /meme.')
    
    @commands.command(name='memedefracasso', aliases=['meme-fracasso', 'memefracasso'])
    async def meme_fracasso(self, ctx):
        """Mostra um meme de fracasso do momento"""
        await ctx.typing()
        
        meme = await self.memes.get_meme_by_category('fracasso')
        
        if meme:
            embed = discord.Embed(
                title=f'💀 Fracasso: {meme["title"][:180]}',
                description='Quando tudo dá errado porra!',
                color=discord.Color.red()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • F no chat caralho 😅')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não achei meme de fracasso! Tenta /meme.')
    
    @commands.command(name='memedetroll', aliases=['meme-troll', 'troll'])
    async def meme_troll(self, ctx):
        """Envia um meme de troll"""
        await ctx.typing()
        
        meme = await self.memes.get_meme_by_category('troll')
        
        if meme:
            embed = discord.Embed(
                title=f'😈 Troll: {meme["title"][:180]}',
                description='Trollagem pesada fdp!',
                color=discord.Color.dark_red()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • Problemão? 😏')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não achei meme de troll! Tenta /meme.')
    
    @commands.command(name='memedezoacao', aliases=['meme-zoacao', 'zoacao', 'zoeira'])
    async def meme_zoacao(self, ctx):
        """Envia um meme de zoação"""
        await ctx.typing()
        
        meme = await self.memes.get_meme_by_category('zoacao')
        
        if meme:
            embed = discord.Embed(
                title=f'🤪 Zoação: {meme["title"][:180]}',
                description='Zoeira não tem limites caralho!',
                color=discord.Color.gold()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • É zueira porra! 😂')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não achei meme de zoação! Tenta /meme.')
    
    @commands.command(name='memebr', aliases=['meme-br', 'memebrasil'])
    async def meme_brasileiro(self, ctx):
        """Envia um meme brasileiro"""
        await ctx.typing()
        
        meme = await self.memes.get_brazilian_meme()
        
        if meme:
            embed = discord.Embed(
                title=f'🇧🇷 {meme["title"][:200]}',
                description='Meme brasileiro raiz caralho!',
                color=discord.Color.green()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • Meme BR puro sangue porra!')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não achei meme BR não! Tenta /meme.')
    
    @commands.command(name='topmeme', aliases=['top-meme', 'memetop'])
    async def top_meme(self, ctx):
        """Envia um dos memes mais votados de hoje"""
        await ctx.typing()
        
        meme = await self.memes.get_top_meme()
        
        if meme:
            embed = discord.Embed(
                title=f'🏆 Top Meme: {meme["title"][:180]}',
                description='Um dos memes mais votado de hoje porra!',
                color=discord.Color.gold()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • {meme["score"]:,} ⬆️ • Top de hj caralho!')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Não consegui buscar top meme não! Tenta /meme.')


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(Memes(bot))
