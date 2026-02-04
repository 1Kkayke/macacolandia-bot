"""Fun commands cog"""

import discord
from discord.ext import commands
import asyncio
from src.fun.jokes import JokeManager
from src.fun.trivia import TriviaManager
from src.fun.poll import PollManager
from src.database.db_manager import DatabaseManager
from src.economy.economy_manager import EconomyManager
from src.config import PREFIX


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jokes = JokeManager()
        self.trivia = TriviaManager()
        self.polls = PollManager()
        self.db = DatabaseManager()
        self.economy = EconomyManager(self.db)
        self.used_questions = {}
    
    @commands.command(name='joke', aliases=['jokes'])
    async def joke(self, ctx):
        """Tell a random joke"""
        joke = self.jokes.get_random_joke()
        
        embed = discord.Embed(
            title='😂 Random Joke',
            description=joke,
            color=discord.Color.blue()
        )
        embed.set_footer(text='Hope you laughed! 🤣')
        await ctx.send(embed=embed)
    
    @commands.command(name='trivia', aliases=['quiz'])
    async def trivia(self, ctx):
        """Start a quiz with reward"""
        user_id = str(ctx.author.id)
        
        if user_id not in self.used_questions:
            self.used_questions[user_id] = []
        
        question, question_index = self.trivia.get_random_question_excluding(self.used_questions[user_id])
        
        if question is None:
            self.used_questions[user_id] = []
            question, question_index = self.trivia.get_random_question_excluding([])
        
        self.used_questions[user_id].append(question_index)
        
        options_text = '\n'.join([f'{i+1}️⃣ {option}' for i, option in enumerate(question.options)])
        
        embed = discord.Embed(
            title=f'❓ Trivia - {question.category}',
            description=f'Answer the question:\n\n{question.question}',
            color=discord.Color.blue()
        )
        
        embed.add_field(name='Options', value=options_text, inline=False)
        embed.add_field(name='Prize', value='🏆 50 🪙', inline=True)
        embed.add_field(name='Time', value='⏰ 15 seconds', inline=True)
        embed.set_footer(text=f'Question for {ctx.author.name}')
        
        msg = await ctx.send(embed=embed)
        
        number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        for i in range(len(question.options)):
            await msg.add_reaction(number_emojis[i])
        
        def check(reaction, user):
            return (user == ctx.author and 
                   str(reaction.emoji) in number_emojis[:len(question.options)] and
                   reaction.message.id == msg.id)
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
            answer_index = number_emojis.index(str(reaction.emoji))
            
            if answer_index == question.correct:
                self.economy.add_coins(str(ctx.author.id), 50, 'Trivia correct')
                embed = discord.Embed(
                    title='✅ Correct!',
                    description=f'**{ctx.author.display_name}** won **50 🪙**!',
                    color=discord.Color.green()
                )
                embed.add_field(name='Answer', value=question.options[question.correct], inline=False)
            else:
                embed = discord.Embed(
                    title='❌ Wrong!',
                    description=f'**{ctx.author.display_name}**, better luck next time!',
                    color=discord.Color.red()
                )
                embed.add_field(name='Correct Answer', value=question.options[question.correct], inline=False)
            
            user_data = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Balance: {user_data["coins"]:,} 🪙')
            await msg.edit(embed=embed)
        
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title='⏰ Time\'s Up!',
                description=f'**{ctx.author.display_name}** ran out of time!',
                color=discord.Color.orange()
            )
            embed.add_field(name='Correct Answer', value=question.options[question.correct], inline=False)
            await msg.edit(embed=embed)
    
    @commands.command(name='poll', aliases=['vote'])
    async def poll(self, ctx, duration: int, question: str, *options):
        """Create a poll"""
        if not question:
            await ctx.send(f'❌ Usage: `{PREFIX}poll <minutes> "question" "option1" "option2" ...`')
            return
        
        if len(options) < 2:
            await ctx.send('❌ Need at least 2 options!')
            return
        
        if len(options) > 10:
            await ctx.send('❌ Maximum 10 options!')
            return
        
        if duration < 1 or duration > 60:
            await ctx.send('❌ Duration must be between 1 and 60 minutes!')
            return
        
        poll_id = self.polls.create_poll(question, list(options), str(ctx.author.id), duration)
        
        number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        options_text = '\n'.join([f'{number_emojis[i]} {option}' for i, option in enumerate(options)])
        
        embed = discord.Embed(
            title='📊 Poll',
            description=question,
            color=discord.Color.blue()
        )
        
        embed.add_field(name='Options', value=options_text, inline=False)
        embed.add_field(name='Duration', value=f'⏰ {duration} minutes', inline=True)
        embed.set_footer(text=f'Created by {ctx.author.name}')
        
        msg = await ctx.send(embed=embed)
        
        for i in range(len(options)):
            await msg.add_reaction(number_emojis[i])
        
        poll_message_id = msg.id
        await asyncio.sleep(duration * 60)
        
        try:
            msg = await ctx.channel.fetch_message(poll_message_id)
            
            results = {}
            for i, reaction in enumerate(msg.reactions):
                if str(reaction.emoji) in number_emojis[:len(options)]:
                    count = reaction.count - 1
                    results[i] = count
            
            total_votes = sum(results.values())
            results_text = []
            
            for i, option in enumerate(options):
                votes = results.get(i, 0)
                percentage = (votes / total_votes * 100) if total_votes > 0 else 0
                bar_length = int(percentage / 10)
                bar = '█' * bar_length + '░' * (10 - bar_length)
                results_text.append(f'{number_emojis[i]} **{option}**\n{bar} {votes} votes ({percentage:.1f}%)')
            
            embed = discord.Embed(
                title='📊 Poll Ended!',
                description=question,
                color=discord.Color.green()
            )
            
            embed.add_field(name=f'Results ({total_votes} votes)', value='\n\n'.join(results_text), inline=False)
            embed.set_footer(text=f'Created by {ctx.author.name}')
            
            await msg.edit(embed=embed)
        except discord.NotFound:
            pass
        
        self.polls.close_poll(poll_id)
    
    @commands.command(name='8ball', aliases=['magic8'])
    async def magic_8ball(self, ctx, *, question: str = None):
        """Ask the magic 8 ball"""
        if not question:
            await ctx.send(f'❌ Ask a question! Example: `{PREFIX}8ball Will I win today?`')
            return
        
        import random
        responses = [
            '🟢 Definitely yes!',
            '🟢 It is certain.',
            '🟢 Without a doubt.',
            '🟢 Yes, definitely.',
            '🟢 You can count on it!',
            '🟡 Outlook looks good.',
            '🟡 Probably yes.',
            '🟡 Signs point to yes.',
            '🟡 Yes.',
            '🟡 Seems like it.',
            '🟠 Reply hazy, try again.',
            '🟠 Ask again later.',
            '🟠 Better not tell you now.',
            '🟠 Cannot predict now.',
            '🟠 Concentrate and ask again.',
            '🔴 Don\'t count on it.',
            '🔴 My reply is no.',
            '🔴 My sources say no.',
            '🔴 Outlook not so good.',
            '🔴 Very doubtful.',
        ]
        
        answer = random.choice(responses)
        
        embed = discord.Embed(title='🎱 Magic 8 Ball', color=discord.Color.purple())
        embed.add_field(name='Question', value=question, inline=False)
        embed.add_field(name='Answer', value=answer, inline=False)
        embed.set_footer(text='The magic 8 ball has spoken!')
        
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
