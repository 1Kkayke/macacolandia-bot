"""Economy commands cog"""

import discord
from discord.ext import commands
from datetime import datetime
from src.database.db_manager import DatabaseManager
from src.economy.economy_manager import EconomyManager
from src.core.achievements import AchievementManager
from src.config import PREFIX


class Economy(commands.Cog):
    """Economy and currency management commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseManager()
        self.economy = EconomyManager(self.db)
        self.achievements = AchievementManager(self.db)
    
    @commands.command(name='saldo', aliases=['balance', 'bal', 'coins', 'moedas'])
    async def balance(self, ctx, member: discord.Member = None):
        """Mostra o saldo de moedas"""
        member = member or ctx.author
        user = self.db.get_user(str(member.id), member.name)
        
        embed = discord.Embed(
            title=f'💰 Saldo de {member.name}',
            color=discord.Color.gold()
        )
        
        embed.add_field(name='Moedas', value=f'🪙 {user["coins"]:,}', inline=True)
        embed.add_field(name='Jogos', value=f'🎮 {user["games_played"]}', inline=True)
        embed.add_field(name='Sequência', value=f'🔥 {user["streak"]} dias', inline=True)
        embed.add_field(name='Total Ganho', value=f'✅ {user["total_won"]:,}', inline=True)
        embed.add_field(name='Total Perdido', value=f'❌ {user["total_lost"]:,}', inline=True)
        
        net = user["total_won"] - user["total_lost"]
        net_symbol = '📈' if net >= 0 else '📉'
        embed.add_field(name='Lucro Líquido', value=f'{net_symbol} {net:,}', inline=True)
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f'Membro desde {user["created_at"][:10]}')
        
        await ctx.send(embed=embed)
    
    @commands.command(name='transferir', aliases=['transfer', 'dar', 'give'])
    async def transfer(self, ctx, member: discord.Member, amount: int):
        """Transfere moedas para outro usuário"""
        if member.bot:
            await ctx.send('❌ Você não pode transferir moedas para bots!')
            return
        
        if member.id == ctx.author.id:
            await ctx.send('❌ Você não pode transferir moedas para si mesmo!')
            return
        
        if amount <= 0:
            await ctx.send('❌ O valor deve ser maior que 0!')
            return
        
        # Get or create target user
        self.db.get_user(str(member.id), member.name)
        
        success, message = self.economy.transfer_coins(str(ctx.author.id), str(member.id), amount)
        
        if success:
            embed = discord.Embed(
                title='💸 Transferência Realizada',
                description=f'{ctx.author.mention} transferiu **{amount:,}** 🪙 para {member.mention}',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'❌ {message}')
    
    @commands.command(name='diario', aliases=['daily', 'diária'])
    async def daily(self, ctx):
        """Reivindica sua recompensa diária"""
        success, coins_earned, streak = self.db.claim_daily_reward(str(ctx.author.id))
        
        if not success:
            await ctx.send('❌ Você já reivindicou sua recompensa diária hoje! Volte amanhã.')
            return
        
        embed = discord.Embed(
            title='🎁 Recompensa Diária',
            description=f'Você recebeu **{coins_earned:,}** 🪙!',
            color=discord.Color.green()
        )
        
        embed.add_field(name='Sequência', value=f'🔥 {streak} dias', inline=True)
        
        if streak >= 7:
            embed.add_field(
                name='🌟 Bônus de Sequência!',
                value='Continue voltando para aumentar sua recompensa!',
                inline=False
            )
        
        embed.set_footer(text='Volte amanhã para continuar sua sequência!')
        
        # Check for achievements
        new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
        if new_achievements:
            achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
            embed.add_field(name='🏆 Conquistas Desbloqueadas!', value=achievement_text, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='historico', aliases=['history', 'hist', 'transacoes'])
    async def history(self, ctx):
        """Mostra seu histórico de transações"""
        transactions = self.db.get_transaction_history(str(ctx.author.id), limit=10)
        
        if not transactions:
            await ctx.send('📋 Você ainda não tem histórico de transações.')
            return
        
        embed = discord.Embed(
            title=f'📋 Histórico de Transações - {ctx.author.name}',
            color=discord.Color.blue()
        )
        
        for trans in transactions:
            timestamp = datetime.fromisoformat(trans['timestamp']).strftime('%d/%m %H:%M')
            amount_str = f"+{trans['amount']}" if trans['amount'] > 0 else str(trans['amount'])
            emoji = '💰' if trans['amount'] > 0 else '💸'
            
            description = trans['description'] or trans['transaction_type']
            embed.add_field(
                name=f'{emoji} {amount_str} 🪙',
                value=f'{description}\n*{timestamp}*',
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='ranking', aliases=['leaderboard', 'top', 'rank'])
    async def leaderboard(self, ctx):
        """Mostra o ranking de jogadores"""
        leaders = self.db.get_leaderboard(limit=10)
        
        if not leaders:
            await ctx.send('📊 Ainda não há jogadores no ranking.')
            return
        
        embed = discord.Embed(
            title='🏆 Ranking - Top 10 Jogadores',
            description='Os jogadores mais ricos do servidor!',
            color=discord.Color.gold()
        )
        
        medals = ['🥇', '🥈', '🥉']
        
        for i, leader in enumerate(leaders):
            medal = medals[i] if i < 3 else f'{i+1}.'
            username = leader['username']
            coins = leader['coins']
            games = leader['games_played']
            
            embed.add_field(
                name=f'{medal} {username}',
                value=f'💰 {coins:,} 🪙 | 🎮 {games} jogos',
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='conquistas', aliases=['achievements', 'ach'])
    async def achievements_cmd(self, ctx, member: discord.Member = None):
        """Mostra as conquistas de um jogador (paginado)"""
        member = member or ctx.author
        user_achievements = self.db.get_user_achievements(str(member.id))
        all_achievements = self.achievements.get_all_achievements()
        
        unlocked_names = {a['achievement_name'] for a in user_achievements}
        
        # Prepare achievement list
        achievements_list = []
        for achievement in all_achievements:
            if achievement.name in unlocked_names:
                status = '✅'
                unlock_info = next((a for a in user_achievements if a['achievement_name'] == achievement.name), None)
                date = datetime.fromisoformat(unlock_info['unlocked_at']).strftime('%d/%m/%Y') if unlock_info else ''
                value = f'{achievement.description}\n*Desbloqueada em {date}*'
            else:
                status = '🔒'
                value = f'{achievement.description}\nRecompensa: {achievement.reward} 🪙'
            
            achievements_list.append({
                'name': f'{status} {achievement.emoji} {achievement.title}',
                'value': value
            })
        
        # Pagination - 10 per page
        items_per_page = 10
        total_pages = (len(achievements_list) + items_per_page - 1) // items_per_page
        current_page = 0
        
        def create_embed(page):
            embed = discord.Embed(
                title=f'🏆 Conquistas de {member.name}',
                description=f'{len(user_achievements)}/{len(all_achievements)} desbloqueadas',
                color=discord.Color.purple()
            )
            
            start = page * items_per_page
            end = min(start + items_per_page, len(achievements_list))
            
            for ach in achievements_list[start:end]:
                embed.add_field(name=ach['name'], value=ach['value'], inline=False)
            
            embed.set_footer(text=f'Página {page + 1}/{total_pages}')
            return embed
        
        # Create view with buttons
        class AchievementView(discord.ui.View):
            def __init__(self, timeout=180):
                super().__init__(timeout=timeout)
                self.page = 0
            
            @discord.ui.button(label='◀️ Anterior', style=discord.ButtonStyle.gray)
            async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message('Esta paginação não é sua!', ephemeral=True)
                
                self.page = (self.page - 1) % total_pages
                await interaction.response.edit_message(embed=create_embed(self.page), view=self)
            
            @discord.ui.button(label='▶️ Próxima', style=discord.ButtonStyle.gray)
            async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message('Esta paginação não é sua!', ephemeral=True)
                
                self.page = (self.page + 1) % total_pages
                await interaction.response.edit_message(embed=create_embed(self.page), view=self)
        
        if total_pages > 1:
            view = AchievementView()
            await ctx.send(embed=create_embed(0), view=view)
        else:
            await ctx.send(embed=create_embed(0))


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(Economy(bot))
