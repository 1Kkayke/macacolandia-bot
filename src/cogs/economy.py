"""Economy commands cog"""

import discord
from discord.ext import commands
from datetime import datetime
from src.database.db_manager import DatabaseManager
from src.economy.economy_manager import EconomyManager
from src.core.achievements import AchievementManager
from src.config import PREFIX


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseManager()
        self.economy = EconomyManager(self.db)
        self.achievements = AchievementManager(self.db)
    
    @commands.command(name='balance', aliases=['bal', 'coins'])
    async def balance(self, ctx, member: discord.Member = None):
        """Show coin balance"""
        member = member or ctx.author
        user = self.db.get_user(str(member.id), member.name)
        
        is_broke = user["coins"] < 1000
        is_negative = user["coins"] < 0
        
        if is_negative:
            title = f'🚨 {member.name} is in DEBT!'
            description = 'Negative balance detected!'
            color = discord.Color.dark_red()
        elif is_broke:
            title = f'🚫 {member.name} is broke!'
            description = 'Low on coins!'
            color = discord.Color.red()
        else:
            title = f'💰 {member.name}\'s Balance'
            description = 'Current stats'
            color = discord.Color.gold()
        
        embed = discord.Embed(title=title, description=description, color=color)
        
        coins_text = f'🪙 {user["coins"]:,}'
        if is_negative:
            coins_text += ' ⚠️ **NEGATIVE BALANCE**'
        
        embed.add_field(name='Coins', value=coins_text, inline=True)
        embed.add_field(name='Games Played', value=f'🎮 {user["games_played"]}', inline=True)
        embed.add_field(name='Daily Streak', value=f'🔥 {user["streak"]} days', inline=True)
        embed.add_field(name='Total Won', value=f'✅ {user["total_won"]:,}', inline=True)
        embed.add_field(name='Total Lost', value=f'❌ {user["total_lost"]:,}', inline=True)
        
        net = user["total_won"] - user["total_lost"]
        net_symbol = '📈' if net >= 0 else '📉'
        embed.add_field(name='Net Profit', value=f'{net_symbol} {net:,}', inline=True)
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f'Member since {user["created_at"][:10]}')
        
        await ctx.send(embed=embed)
    
    @commands.command(name='transfer', aliases=['give', 'send'])
    async def transfer(self, ctx, member: discord.Member, amount: int):
        """Transfer coins to another user"""
        if member.bot:
            await ctx.send('❌ Cannot send coins to bots!')
            return
        
        if member.id == ctx.author.id:
            await ctx.send('❌ Cannot send coins to yourself!')
            return
        
        if amount <= 0:
            await ctx.send('❌ Amount must be greater than 0!')
            return
        
        self.db.get_user(str(member.id), member.name)
        success, message = self.economy.transfer_coins(str(ctx.author.id), str(member.id), amount)
        
        if success:
            embed = discord.Embed(
                title='💸 Transfer Complete!',
                description=f'{ctx.author.mention} sent **{amount:,}** 🪙 to {member.mention}',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'❌ Transfer failed: {message}')
    
    @commands.command(name='daily')
    async def daily(self, ctx):
        """Claim daily reward"""
        success, coins_earned, streak = self.db.claim_daily_reward(str(ctx.author.id))
        
        if not success:
            await ctx.send('❌ Already claimed today! Come back tomorrow.')
            return
        
        embed = discord.Embed(
            title='🎁 Daily Reward!',
            description=f'You received **{coins_earned:,}** 🪙!',
            color=discord.Color.green()
        )
        
        embed.add_field(name='Streak', value=f'🔥 {streak} consecutive days', inline=True)
        
        if streak >= 7:
            embed.add_field(name='🌟 Streak Bonus', value='Keep coming back for more!', inline=False)
        
        embed.set_footer(text='Come back tomorrow for more!')
        
        new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
        if new_achievements:
            achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
            embed.add_field(name='🏆 Achievements Unlocked!', value=achievement_text, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='history', aliases=['hist', 'transactions'])
    async def history(self, ctx):
        """Show transaction history"""
        transactions = self.db.get_transaction_history(str(ctx.author.id), limit=10)
        
        if not transactions:
            await ctx.send('📋 No transactions yet!')
            return
        
        embed = discord.Embed(
            title=f'📋 {ctx.author.name}\'s History',
            description='Recent transactions:',
            color=discord.Color.blue()
        )
        
        for trans in transactions:
            timestamp = datetime.fromisoformat(trans['timestamp']).strftime('%d/%m %H:%M')
            amount_str = f"+{trans['amount']}" if trans['amount'] > 0 else str(trans['amount'])
            emoji = '💰' if trans['amount'] > 0 else '💸'
            description = trans['description'] or trans['transaction_type']
            embed.add_field(name=f'{emoji} {amount_str} 🪙', value=f'{description}\n*{timestamp}*', inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='ranking', aliases=['leaderboard', 'top', 'rank'])
    async def leaderboard(self, ctx):
        """Show player ranking"""
        leaders = self.db.get_leaderboard(limit=10)
        
        if not leaders:
            await ctx.send('📊 No players on the leaderboard yet!')
            return
        
        embed = discord.Embed(
            title='🏆 Leaderboard - Top 10',
            description='The richest players!',
            color=discord.Color.gold()
        )
        
        medals = ['🥇', '🥈', '🥉']
        
        for i, leader in enumerate(leaders):
            medal = medals[i] if i < 3 else f'{i+1}.'
            embed.add_field(
                name=f'{medal} {leader["username"]}',
                value=f'💰 {leader["coins"]:,} 🪙 | 🎮 {leader["games_played"]} games',
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='achievements', aliases=['ach'])
    async def achievements_cmd(self, ctx, member: discord.Member = None):
        """Show player achievements"""
        member = member or ctx.author
        user_achievements = self.db.get_user_achievements(str(member.id))
        all_achievements = self.achievements.get_all_achievements()
        
        unlocked_names = {a['achievement_name'] for a in user_achievements}
        
        achievements_list = []
        for achievement in all_achievements:
            if achievement.name in unlocked_names:
                status = '✅'
                unlock_info = next((a for a in user_achievements if a['achievement_name'] == achievement.name), None)
                date = datetime.fromisoformat(unlock_info['unlocked_at']).strftime('%d/%m/%Y') if unlock_info else ''
                value = f'{achievement.description}\n*Unlocked on {date}*'
            else:
                status = '🔒'
                value = f'{achievement.description}\nReward: {achievement.reward} 🪙'
            
            achievements_list.append({'name': f'{status} {achievement.emoji} {achievement.title}', 'value': value})
        
        items_per_page = 10
        total_pages = (len(achievements_list) + items_per_page - 1) // items_per_page
        
        def create_embed(page):
            total_unlocked = len(user_achievements)
            total_achievements = len(all_achievements)
            percentage = int((total_unlocked / total_achievements) * 100) if total_achievements > 0 else 0
            
            embed = discord.Embed(
                title=f'🏆 {member.name}\'s Achievements',
                description=f'{total_unlocked}/{total_achievements} unlocked ({percentage}%)',
                color=discord.Color.purple()
            )
            
            start = page * items_per_page
            end = min(start + items_per_page, len(achievements_list))
            
            for ach in achievements_list[start:end]:
                embed.add_field(name=ach['name'], value=ach['value'], inline=False)
            
            embed.set_footer(text=f'Page {page + 1}/{total_pages}')
            return embed
        
        class AchievementView(discord.ui.View):
            def __init__(self, timeout=180):
                super().__init__(timeout=timeout)
                self.page = 0
            
            @discord.ui.button(label='◀️ Previous', style=discord.ButtonStyle.gray)
            async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message('Not your pagination!', ephemeral=True)
                self.page = (self.page - 1) % total_pages
                await interaction.response.edit_message(embed=create_embed(self.page), view=self)
            
            @discord.ui.button(label='▶️ Next', style=discord.ButtonStyle.gray)
            async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message('Not your pagination!', ephemeral=True)
                self.page = (self.page + 1) % total_pages
                await interaction.response.edit_message(embed=create_embed(self.page), view=self)
        
        if total_pages > 1:
            view = AchievementView()
            await ctx.send(embed=create_embed(0), view=view)
        else:
            await ctx.send(embed=create_embed(0))


async def setup(bot):
    await bot.add_cog(Economy(bot))
