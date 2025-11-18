"""Fun and interactive commands cog"""

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
    """Fun and interactive commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.jokes = JokeManager()
        self.trivia = TriviaManager()
        self.polls = PollManager()
        self.db = DatabaseManager()
        self.economy = EconomyManager(self.db)
        # Track used questions per user to avoid repeats
        self.used_questions = {}  # {user_id: [question_indices]}
    
    @commands.command(name='piada', aliases=['joke', 'piadas'])
    async def joke(self, ctx):
        """Conta uma piada aleatória"""
        joke = self.jokes.get_random_joke()
        
        embed = discord.Embed(
            title='😄 Piada do Dia',
            description=joke,
            color=discord.Color.blue()
        )
        
        embed.set_footer(text='Espero que tenha gostado! 🤣')
        await ctx.send(embed=embed)
    
    @commands.command(name='trivia', aliases=['quiz', 'pergunta'])
    async def trivia(self, ctx):
        """Inicia um quiz com recompensa"""
        user_id = str(ctx.author.id)
        
        # Initialize user's used questions list if not exists
        if user_id not in self.used_questions:
            self.used_questions[user_id] = []
        
        # Get a question that hasn't been used by this user
        question, question_index = self.trivia.get_random_question_excluding(self.used_questions[user_id])
        
        # If all questions were used, reset the user's history
        if question is None:
            self.used_questions[user_id] = []
            question, question_index = self.trivia.get_random_question_excluding([])
        
        # Mark this question as used
        self.used_questions[user_id].append(question_index)
        
        # Format options
        options_text = '\n'.join([
            f'{i+1}️⃣ {option}' 
            for i, option in enumerate(question.options)
        ])
        
        embed = discord.Embed(
            title=f'❓ Trivia - {question.category}',
            description=question.question,
            color=discord.Color.blue()
        )
        
        embed.add_field(name='Opções', value=options_text, inline=False)
        embed.add_field(name='Prêmio', value='🏆 50 🪙', inline=True)
        embed.add_field(name='Tempo', value='⏰ 15 segundos', inline=True)
        embed.set_footer(text=f'Pergunta para: {ctx.author.name}')
        
        msg = await ctx.send(embed=embed)
        
        # Add number reactions
        number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        for i in range(len(question.options)):
            await msg.add_reaction(number_emojis[i])
        
        def check(reaction, user):
            # Apenas o autor pode responder
            return (user == ctx.author and 
                   str(reaction.emoji) in number_emojis[:len(question.options)] and
                   reaction.message.id == msg.id)
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
            
            # Get answer
            answer_index = number_emojis.index(str(reaction.emoji))
            
            if answer_index == question.correct:
                # Correct!
                self.economy.add_coins(str(ctx.author.id), 50, 'Trivia correta')
                
                embed = discord.Embed(
                    title=f'✅ Resposta Correta!',
                    description=f'**{ctx.author.display_name}** ganhou **50 🪙**',
                    color=discord.Color.green()
                )
                
                embed.add_field(
                    name='Resposta',
                    value=question.options[question.correct],
                    inline=False
                )
            else:
                # Wrong
                embed = discord.Embed(
                    title=f'❌ Resposta Incorreta',
                    description=f'**{ctx.author.display_name}**, mais sorte na próxima vez!',
                    color=discord.Color.red()
                )
                
                embed.add_field(
                    name='Resposta Correta',
                    value=question.options[question.correct],
                    inline=False
                )
            
            user_data = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Saldo de {ctx.author.name}: {user_data["coins"]:,} 🪙')
            
            await msg.edit(embed=embed)
        
        except asyncio.TimeoutError:
            embed = discord.Embed(
                title='⏰ Tempo Esgotado',
                description=f'**{ctx.author.display_name}** não respondeu a tempo!',
                color=discord.Color.orange()
            )
            
            embed.add_field(
                name='Resposta Correta',
                value=question.options[question.correct],
                inline=False
            )
            
            await msg.edit(embed=embed)
    
    @commands.command(name='enquete', aliases=['poll', 'votacao'])
    async def poll(self, ctx, duration: int, question: str, *options):
        """
        Cria uma enquete
        Uso: /enquete <minutos> "pergunta" "opção1" "opção2" ...
        """
        if not question:
            await ctx.send(f'❌ Uso: `{PREFIX}enquete <minutos> "pergunta" "opção1" "opção2" ...`')
            return
        
        if len(options) < 2:
            await ctx.send('❌ Você precisa fornecer pelo menos 2 opções!')
            return
        
        if len(options) > 10:
            await ctx.send('❌ Máximo de 10 opções!')
            return
        
        if duration < 1 or duration > 60:
            await ctx.send('❌ A duração deve ser entre 1 e 60 minutos!')
            return
        
        # Create poll
        poll_id = self.polls.create_poll(question, list(options), str(ctx.author.id), duration)
        poll = self.polls.get_poll(poll_id)
        
        # Format options
        number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        options_text = '\n'.join([
            f'{number_emojis[i]} {option}' 
            for i, option in enumerate(options)
        ])
        
        embed = discord.Embed(
            title='📊 Enquete',
            description=question,
            color=discord.Color.blue()
        )
        
        embed.add_field(name='Opções', value=options_text, inline=False)
        embed.add_field(name='Duração', value=f'⏰ {duration} minutos', inline=True)
        embed.set_footer(text=f'Criada por {ctx.author.name}')
        
        msg = await ctx.send(embed=embed)
        
        # Add reactions
        for i in range(len(options)):
            await msg.add_reaction(number_emojis[i])
        
        # Store message ID
        poll_message_id = msg.id
        
        # Wait for duration
        await asyncio.sleep(duration * 60)
        
        # Get results
        # Fetch message again to get updated reactions
        try:
            msg = await ctx.channel.fetch_message(poll_message_id)
            
            results = {}
            for i, reaction in enumerate(msg.reactions):
                if str(reaction.emoji) in number_emojis[:len(options)]:
                    # Subtract 1 for bot's own reaction
                    count = reaction.count - 1
                    results[i] = count
            
            # Format results
            total_votes = sum(results.values())
            results_text = []
            
            for i, option in enumerate(options):
                votes = results.get(i, 0)
                percentage = (votes / total_votes * 100) if total_votes > 0 else 0
                bar_length = int(percentage / 10)
                bar = '█' * bar_length + '░' * (10 - bar_length)
                results_text.append(f'{number_emojis[i]} **{option}**\n{bar} {votes} votos ({percentage:.1f}%)')
            
            embed = discord.Embed(
                title='📊 Enquete Encerrada',
                description=question,
                color=discord.Color.green()
            )
            
            embed.add_field(
                name=f'Resultados ({total_votes} votos)',
                value='\n\n'.join(results_text),
                inline=False
            )
            
            embed.set_footer(text=f'Criada por {ctx.author.name}')
            
            await msg.edit(embed=embed)
        
        except discord.NotFound:
            pass
        
        # Clean up
        self.polls.close_poll(poll_id)
    
    @commands.command(name='8ball', aliases=['bola8', 'magica'])
    async def magic_8ball(self, ctx, *, question: str = None):
        """Pergunta à bola mágica 8"""
        if not question:
            await ctx.send(f'❌ Faça uma pergunta! Exemplo: `{PREFIX}8ball Vou ganhar no cassino hoje?`')
            return
        
        import random
        responses = [
            '🟢 Com certeza!',
            '🟢 É certo.',
            '🟢 Sem dúvida.',
            '🟢 Sim, definitivamente.',
            '🟢 Pode contar com isso.',
            '🟡 As perspectivas são boas.',
            '🟡 Provavelmente sim.',
            '🟡 Sinais apontam que sim.',
            '🟡 Sim.',
            '🟡 Parece que sim.',
            '🟠 Resposta incerta, tente novamente.',
            '🟠 Pergunte novamente mais tarde.',
            '🟠 Melhor não te dizer agora.',
            '🟠 Não posso prever agora.',
            '🟠 Concentre-se e pergunte novamente.',
            '🔴 Não conte com isso.',
            '🔴 Minha resposta é não.',
            '🔴 Minhas fontes dizem que não.',
            '🔴 As perspectivas não são boas.',
            '🔴 Muito duvidoso.',
        ]
        
        answer = random.choice(responses)
        
        embed = discord.Embed(
            title='🎱 Bola Mágica 8',
            color=discord.Color.purple()
        )
        
        embed.add_field(name='Pergunta', value=question, inline=False)
        embed.add_field(name='Resposta', value=answer, inline=False)
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(Fun(bot))
