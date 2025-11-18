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
        
        is_broke = user["coins"] < 1000
        title = f'💰 Grana do {member.name}' if not is_broke else f'🚫 {member.name} tá liso!'
        
        embed = discord.Embed(
            title=title,
            description='Vamo vê se tu é rico ou se tá fudido...' if not is_broke else 'Caralho mano, tu tá duro memo hein!',
            color=discord.Color.gold() if not is_broke else discord.Color.red()
        )
        
        coins_text = f'🪙 {user["coins"]:,}'
        if user["coins"] < 100:
            coins_text += ' (pobre do caralho)'
        elif user["coins"] > 100000:
            coins_text += ' (rico filho da puta!)'
        
        embed.add_field(name='Moedas (a grana)', value=coins_text, inline=True)
        embed.add_field(name='Jogos (qtos jogo tu jogou)', value=f'🎮 {user["games_played"]}', inline=True)
        embed.add_field(name='Sequência (qtos dias seguidos)', value=f'🔥 {user["streak"]} dias', inline=True)
        embed.add_field(name='Total Ganho (oq tu já ganhou)', value=f'✅ {user["total_won"]:,}', inline=True)
        embed.add_field(name='Total Perdido (oq tu perdeu fdp)', value=f'❌ {user["total_lost"]:,}', inline=True)
        
        net = user["total_won"] - user["total_lost"]
        if net >= 0:
            net_symbol = '📈'
            net_text = f'{net:,} (no lucro mano!)'
        else:
            net_symbol = '📉'
            net_text = f'{net:,} (tu tá no prejuízo caralho!)'
        
        embed.add_field(name='Lucro Líquido (se tá ganhando ou perdendo)', value=f'{net_symbol} {net_text}', inline=True)
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f'Membro desde {user["created_at"][:10]} | Tá ligado?')
        
        await ctx.send(embed=embed)
    
    @commands.command(name='transferir', aliases=['transfer', 'dar', 'give'])
    async def transfer(self, ctx, member: discord.Member, amount: int):
        """Transfere moedas para outro usuário"""
        if member.bot:
            await ctx.send('❌ Porra mano, não manda grana pra bot não caralho!')
            return
        
        if member.id == ctx.author.id:
            await ctx.send('❌ Tu é burro? Não dá pra mandar grana pra tu mesmo não fdp!')
            return
        
        if amount <= 0:
            await ctx.send('❌ Que porra é essa? Manda um valor maior que 0 caralho!')
            return
        
        # Get or create target user
        self.db.get_user(str(member.id), member.name)
        
        success, message = self.economy.transfer_coins(str(ctx.author.id), str(member.id), amount)
        
        if success:
            embed = discord.Embed(
                title='💸 Transferência feita porra!',
                description=f'{ctx.author.mention} mandou **{amount:,}** 🪙 pra {member.mention}. Camarada!',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'❌ Deu ruim caralho: {message}')
    
    @commands.command(name='diario', aliases=['daily', 'diária'])
    async def daily(self, ctx):
        """Reivindica sua recompensa diária"""
        success, coins_earned, streak = self.db.claim_daily_reward(str(ctx.author.id))
        
        if not success:
            await ctx.send('❌ Já pegou teu diário hoje né safado! Volta amanhã pra pegar mais.')
            return
        
        embed = discord.Embed(
            title='🎁 Aqui teu migalho diário!',
            description=f'Pegou **{coins_earned:,}** 🪙! Agora some daqui.',
            color=discord.Color.green()
        )
        
        embed.add_field(name='Sequência (qtos dias seguidos)', value=f'🔥 {streak} dias consecutivos caralho', inline=True)
        
        if streak >= 7:
            embed.add_field(
                name='🌟 Bônus de Sequência porra!',
                value='Continua voltando todo dia que tu vai ganhando mais!',
                inline=False
            )
        
        embed.set_footer(text='Volta amanhã pra pegar mais grana seu fdp!')
        
        # Check for achievements
        new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
        if new_achievements:
            achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
            embed.add_field(name='🏆 Conquistas Desbloqueadas caralho!', value=achievement_text, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='historico', aliases=['history', 'hist', 'transacoes'])
    async def history(self, ctx):
        """Mostra seu histórico de transações"""
        transactions = self.db.get_transaction_history(str(ctx.author.id), limit=10)
        
        if not transactions:
            await ctx.send('📋 Tu não fez nada ainda né vagabundo! Vai jogar alguma coisa.')
            return
        
        embed = discord.Embed(
            title=f'📋 Histórico do {ctx.author.name} (onde tu gastou tua grana)',
            description='Olha só as cagada que tu fez:',
            color=discord.Color.blue()
        )
        
        for trans in transactions:
            timestamp = datetime.fromisoformat(trans['timestamp']).strftime('%d/%m %H:%M')
            amount_str = f"+{trans['amount']}" if trans['amount'] > 0 else str(trans['amount'])
            emoji = '💰' if trans['amount'] > 0 else '💸'
            
            description = trans['description'] or trans['transaction_type']
            embed.add_field(
                name=f'{emoji} {amount_str} 🪙',
                value=f'{description}\n*{timestamp}* - Tá ligado?',
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='ranking', aliases=['leaderboard', 'top', 'rank'])
    async def leaderboard(self, ctx):
        """Mostra o ranking de jogadores"""
        leaders = self.db.get_leaderboard(limit=10)
        
        if not leaders:
            await ctx.send('📊 Não tem ninguém no ranking ainda não caralho! Vai lá jogar porra.')
            return
        
        embed = discord.Embed(
            title='🏆 Ranking - Top 10 dos Rico',
            description='Os filho da puta mais rico do servidor! Tu tá aí? Provavelmente não kkkk',
            color=discord.Color.gold()
        )
        
        medals = ['🥇', '🥈', '🥉']
        
        for i, leader in enumerate(leaders):
            medal = medals[i] if i < 3 else f'{i+1}.'
            username = leader['username']
            coins = leader['coins']
            games = leader['games_played']
            
            suffix = ''
            if i == 0:
                suffix = ' (o mais rico, respeita!)'
            elif i >= 7:
                suffix = ' (meio pobre mas tá aí)'
            
            embed.add_field(
                name=f'{medal} {username}{suffix}',
                value=f'💰 {coins:,} 🪙 | 🎮 {games} jogos jogado',
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
                value = f'{achievement.description}\n*Desbloqueou essa porra em {date}*'
            else:
                status = '🔒'
                value = f'{achievement.description}\nRecompensa: {achievement.reward} 🪙 (tá trancada ainda)'
            
            achievements_list.append({
                'name': f'{status} {achievement.emoji} {achievement.title}',
                'value': value
            })
        
        # Pagination - 10 per page
        items_per_page = 10
        total_pages = (len(achievements_list) + items_per_page - 1) // items_per_page
        current_page = 0
        
        def create_embed(page):
            total_unlocked = len(user_achievements)
            total_achievements = len(all_achievements)
            percentage = int((total_unlocked / total_achievements) * 100) if total_achievements > 0 else 0
            
            if percentage < 30:
                desc_suffix = '(meio fraco hein)'
            elif percentage > 70:
                desc_suffix = '(mandou bem porra!)'
            else:
                desc_suffix = '(tá indo)'
            
            embed = discord.Embed(
                title=f'🏆 Conquistas do {member.name}',
                description=f'{total_unlocked}/{total_achievements} desbloqueadas {desc_suffix}',
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
                    return await interaction.response.send_message('Essa paginação não é tua não caralho!', ephemeral=True)
                
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
