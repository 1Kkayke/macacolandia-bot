"""Memes commands cog"""

import discord
from discord.ext import commands
from src.fun.memes import MemeManager


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.memes = MemeManager()
    
    @commands.command(name='fact', aliases=['facts'])
    async def fact(self, ctx, user: discord.Member = None):
        """Share a random fact or roast"""
        if user is None:
            fact = self.memes.get_random_fact()
            embed = discord.Embed(
                title='💡 Random Fact',
                description=fact,
                color=discord.Color.blue()
            )
            embed.set_footer(text='Is it true? Who knows! 🤔')
        else:
            roast = self.memes.get_random_roast(user.display_name)
            embed = discord.Embed(
                title=f'🔥 Fact about {user.display_name}',
                description=roast,
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.set_footer(text='Just kidding! 😂')
        
        await ctx.send(embed=embed)
    
    @commands.command(name='meme', aliases=['randommeme'])
    async def random_meme(self, ctx):
        """Send a random meme"""
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
            await ctx.send('❌ Couldn\'t fetch meme! Try again.')
    
    @commands.command(name='meme2025', aliases=['memede2025'])
    async def meme_2025(self, ctx):
        """Send a 2025 trending meme"""
        await ctx.typing()
        meme = await self.memes.get_meme_by_category('2025')
        
        if meme:
            embed = discord.Embed(
                title=f'🔥 2025 Meme: {meme["title"][:180]}',
                description='Trending meme!',
                color=discord.Color.orange()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • Trending 2025 🚀')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Couldn\'t find 2025 meme! Try /meme.')
    
    @commands.command(name='dailymeme', aliases=['memedodia'])
    async def meme_do_dia(self, ctx):
        """Show meme of the day"""
        await ctx.typing()
        meme = await self.memes.get_daily_meme()
        
        if meme:
            embed = discord.Embed(
                title=f'📅 Meme of the Day: {meme["title"][:180]}',
                description='Today\'s meme!',
                color=discord.Color.purple()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]}')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Couldn\'t find daily meme! Try /meme.')
    
    @commands.command(name='successmeme', aliases=['memedesucesso'])
    async def meme_sucesso(self, ctx):
        """Show a success meme"""
        await ctx.typing()
        meme = await self.memes.get_meme_by_category('sucesso')
        
        if meme:
            embed = discord.Embed(
                title=f'✨ Success: {meme["title"][:180]}',
                description='Motivational meme!',
                color=discord.Color.green()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} 💪')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Couldn\'t find success meme! Try /meme.')
    
    @commands.command(name='failmeme', aliases=['memedefracasso'])
    async def meme_fracasso(self, ctx):
        """Show a fail meme"""
        await ctx.typing()
        meme = await self.memes.get_meme_by_category('fracasso')
        
        if meme:
            embed = discord.Embed(
                title=f'💀 Fail: {meme["title"][:180]}',
                description='When everything goes wrong!',
                color=discord.Color.red()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} 😅')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Couldn\'t find fail meme! Try /meme.')
    
    @commands.command(name='trollmeme', aliases=['memedetroll', 'troll'])
    async def meme_troll(self, ctx):
        """Send a troll meme"""
        await ctx.typing()
        meme = await self.memes.get_meme_by_category('troll')
        
        if meme:
            embed = discord.Embed(
                title=f'😈 Troll: {meme["title"][:180]}',
                description='Trolling time!',
                color=discord.Color.dark_red()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} 😏')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Couldn\'t find troll meme! Try /meme.')
    
    @commands.command(name='jokememe', aliases=['memedezoacao', 'zoacao'])
    async def meme_zoacao(self, ctx):
        """Send a joke meme"""
        await ctx.typing()
        meme = await self.memes.get_meme_by_category('zoacao')
        
        if meme:
            embed = discord.Embed(
                title=f'🤪 Joke: {meme["title"][:180]}',
                description='Jokes have no limits!',
                color=discord.Color.gold()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} 😂')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Couldn\'t find joke meme! Try /meme.')
    
    @commands.command(name='memebr', aliases=['brazilmeme'])
    async def meme_brasileiro(self, ctx):
        """Send a Brazilian meme"""
        await ctx.typing()
        meme = await self.memes.get_brazilian_meme()
        
        if meme:
            embed = discord.Embed(
                title=f'🇧🇷 {meme["title"][:200]}',
                description='Brazilian meme!',
                color=discord.Color.green()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]}')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Couldn\'t find Brazilian meme! Try /meme.')
    
    @commands.command(name='topmeme')
    async def top_meme(self, ctx):
        """Send a top voted meme"""
        await ctx.typing()
        meme = await self.memes.get_top_meme()
        
        if meme:
            embed = discord.Embed(
                title=f'🏆 Top Meme: {meme["title"][:180]}',
                description='One of today\'s top memes!',
                color=discord.Color.gold()
            )
            embed.set_image(url=meme['url'])
            embed.set_footer(text=f'r/{meme["subreddit"]} • {meme["score"]:,} ⬆️')
            await ctx.send(embed=embed)
        else:
            await ctx.send('❌ Couldn\'t fetch top meme! Try /meme.')


async def setup(bot):
    await bot.add_cog(Memes(bot))
