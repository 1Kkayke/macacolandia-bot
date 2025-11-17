"""Casino games commands cog"""

import discord
from discord.ext import commands
import asyncio
from src.database.db_manager import DatabaseManager
from src.economy.economy_manager import EconomyManager
from src.core.achievements import AchievementManager
from src.core.checks import ensure_not_playing, start_game, end_game
from src.games.roulette import RouletteGame
from src.games.slots import SlotsGame
from src.games.dice import DiceGame
from src.games.blackjack import BlackjackGame
from src.config import PREFIX


class Games(commands.Cog):
    """Casino game commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseManager()
        self.economy = EconomyManager(self.db)
        self.achievements = AchievementManager(self.db)
    
    async def check_balance(self, ctx, amount: int) -> bool:
        """Check if user can afford the bet"""
        if not self.economy.can_afford(str(ctx.author.id), ctx.author.name, amount):
            await ctx.send(f'❌ Saldo insuficiente! Use `{PREFIX}saldo` para ver seu saldo.')
            return False
        return True
    
    @commands.command(name='roleta', aliases=['roulette', 'rlt'])
    async def roulette(self, ctx, bet_amount: int, bet_type: str, bet_value: str):
        """
        Joga roleta
        Uso: /roleta <valor> <tipo> <aposta>
        Tipos: numero (0-36), cor (vermelho/preto), paridade (par/impar), altura (baixo/alto)
        """
        if not await ensure_not_playing(ctx):
            return
        
        if bet_amount < 10:
            await ctx.send('❌ A aposta mínima é 10 🪙!')
            return
        
        if not await self.check_balance(ctx, bet_amount):
            return
        
        start_game(ctx.author.id, 'roulette')
        
        try:
            # Spin the wheel
            number = RouletteGame.spin()
            color = RouletteGame.get_color(number)
            
            # Check if bet won
            won, multiplier = RouletteGame.check_bet(number, bet_type, bet_value)
            
            # Process bet
            success, net_change = self.economy.process_bet(
                str(ctx.author.id),
                ctx.author.name,
                bet_amount,
                'roleta',
                won,
                multiplier
            )
            
            if not success:
                await ctx.send('❌ Erro ao processar aposta!')
                return
            
            # Create result embed
            embed = discord.Embed(
                title='🎰 Roleta Europeia',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            color_emoji = {'vermelho': '🔴', 'preto': '⚫', 'verde': '🟢'}
            embed.add_field(
                name='Resultado',
                value=f'{color_emoji.get(color, "⚪")} **{number}** ({color})',
                inline=False
            )
            
            embed.add_field(name='Sua Aposta', value=f'{bet_type}: {bet_value}', inline=True)
            embed.add_field(name='Valor', value=f'{bet_amount:,} 🪙', inline=True)
            
            if won:
                embed.add_field(
                    name='🎉 GANHOU!',
                    value=f'+{net_change:,} 🪙 (multiplicador: {multiplier}x)',
                    inline=False
                )
            else:
                embed.add_field(
                    name='❌ Perdeu',
                    value=f'{net_change:,} 🪙',
                    inline=False
                )
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Saldo atual: {user["coins"]:,} 🪙')
            
            await ctx.send(embed=embed)
            
            # Check achievements
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n{achievement_text}')
        
        finally:
            end_game(ctx.author.id)
    
    @commands.command(name='slots', aliases=['slot', 'caça', 'cacaniquel'])
    async def slots(self, ctx, bet_amount: int):
        """Joga no caça-níqueis"""
        if not await ensure_not_playing(ctx):
            return
        
        if bet_amount < 10:
            await ctx.send('❌ A aposta mínima é 10 🪙!')
            return
        
        if not await self.check_balance(ctx, bet_amount):
            return
        
        start_game(ctx.author.id, 'slots')
        
        try:
            # Spin the slots
            reels = SlotsGame.spin()
            won, multiplier, description = SlotsGame.calculate_win(reels)
            
            # Process bet
            success, net_change = self.economy.process_bet(
                str(ctx.author.id),
                ctx.author.name,
                bet_amount,
                'slots',
                won,
                multiplier
            )
            
            if not success:
                await ctx.send('❌ Erro ao processar aposta!')
                return
            
            # Create result embed
            embed = discord.Embed(
                title='🎰 Caça-Níqueis',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            embed.add_field(
                name='Resultado',
                value=f'**{SlotsGame.format_reels(reels)}**',
                inline=False
            )
            
            embed.add_field(name='Aposta', value=f'{bet_amount:,} 🪙', inline=True)
            
            if won:
                embed.add_field(
                    name='✨ ' + description,
                    value=f'+{net_change:,} 🪙 ({multiplier}x)',
                    inline=False
                )
            else:
                embed.add_field(
                    name='❌ ' + description,
                    value=f'{net_change:,} 🪙',
                    inline=False
                )
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Saldo atual: {user["coins"]:,} 🪙')
            
            await ctx.send(embed=embed)
            
            # Check achievements
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n{achievement_text}')
        
        finally:
            end_game(ctx.author.id)
    
    @commands.command(name='dados', aliases=['dice', 'dado'])
    async def dice(self, ctx, bet_amount: int, bet_type: str):
        """
        Joga dados
        Uso: /dados <valor> <tipo>
        Tipos: acima, abaixo, sete, alto, baixo, 1-6
        """
        if not await ensure_not_playing(ctx):
            return
        
        if bet_amount < 10:
            await ctx.send('❌ A aposta mínima é 10 🪙!')
            return
        
        if not await self.check_balance(ctx, bet_amount):
            return
        
        start_game(ctx.author.id, 'dice')
        
        try:
            bet_type_lower = bet_type.lower()
            
            # Determine game type and play
            if bet_type_lower in ['acima', 'abaixo', 'sete', 'seven']:
                won, dice, total, multiplier = DiceGame.play_over_under(bet_type_lower)
                result_text = f'{DiceGame.format_dice(dice)}\nTotal: **{total}**'
            elif bet_type_lower in ['alto', 'baixo', 'high', 'low']:
                won, roll, multiplier = DiceGame.play_high_low(bet_type_lower)
                dice_emoji = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
                result_text = f'{dice_emoji[roll-1]} **{roll}**'
            else:
                # Try specific number
                try:
                    bet_number = int(bet_type)
                    if 1 <= bet_number <= 6:
                        won, roll, multiplier = DiceGame.play_specific_number(bet_number)
                        dice_emoji = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅']
                        result_text = f'{dice_emoji[roll-1]} **{roll}**'
                    else:
                        await ctx.send('❌ Tipo de aposta inválido!')
                        return
                except ValueError:
                    await ctx.send('❌ Tipo de aposta inválido!')
                    return
            
            # Process bet
            success, net_change = self.economy.process_bet(
                str(ctx.author.id),
                ctx.author.name,
                bet_amount,
                'dados',
                won,
                multiplier
            )
            
            if not success:
                await ctx.send('❌ Erro ao processar aposta!')
                return
            
            # Create result embed
            embed = discord.Embed(
                title='🎲 Dados',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            embed.add_field(name='Resultado', value=result_text, inline=False)
            embed.add_field(name='Sua Aposta', value=bet_type, inline=True)
            embed.add_field(name='Valor', value=f'{bet_amount:,} 🪙', inline=True)
            
            if won:
                embed.add_field(
                    name='🎉 GANHOU!',
                    value=f'+{net_change:,} 🪙 ({multiplier}x)',
                    inline=False
                )
            else:
                embed.add_field(
                    name='❌ Perdeu',
                    value=f'{net_change:,} 🪙',
                    inline=False
                )
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Saldo atual: {user["coins"]:,} 🪙')
            
            await ctx.send(embed=embed)
            
            # Check achievements
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n{achievement_text}')
        
        finally:
            end_game(ctx.author.id)
    
    @commands.command(name='blackjack', aliases=['bj', '21'])
    async def blackjack(self, ctx, bet_amount: int):
        """Joga Blackjack (21)"""
        if not await ensure_not_playing(ctx):
            return
        
        if bet_amount < 10:
            await ctx.send('❌ A aposta mínima é 10 🪙!')
            return
        
        if not await self.check_balance(ctx, bet_amount):
            return
        
        start_game(ctx.author.id, 'blackjack')
        
        try:
            # Start game
            game = BlackjackGame()
            game.start_game()
            
            # Show initial hands
            embed = discord.Embed(
                title='🃏 Blackjack',
                description='Use ⬇️ para pedir carta (hit) ou 🛑 para parar (stand)',
                color=discord.Color.blue()
            )
            
            embed.add_field(name='🎴 Sua Mão', value=game.get_player_hand_str(), inline=False)
            embed.add_field(name='🂠 Mão do Dealer', value=game.get_dealer_hand_str(hide_second=True), inline=False)
            embed.add_field(name='Aposta', value=f'{bet_amount:,} 🪙', inline=True)
            
            msg = await ctx.send(embed=embed)
            
            # Add reactions
            await msg.add_reaction('⬇️')  # Hit
            await msg.add_reaction('🛑')  # Stand
            
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ['⬇️', '🛑'] and reaction.message.id == msg.id
            
            # Player's turn
            while game.can_player_hit():
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                    
                    if str(reaction.emoji) == '⬇️':
                        # Hit
                        game.player_hit()
                        
                        embed = discord.Embed(
                            title='🃏 Blackjack',
                            description='Use ⬇️ para pedir carta (hit) ou 🛑 para parar (stand)',
                            color=discord.Color.blue()
                        )
                        
                        embed.add_field(name='🎴 Sua Mão', value=game.get_player_hand_str(), inline=False)
                        embed.add_field(name='🂠 Mão do Dealer', value=game.get_dealer_hand_str(hide_second=True), inline=False)
                        
                        await msg.edit(embed=embed)
                        await msg.remove_reaction(reaction, user)
                        
                        if game.player_hand.is_busted():
                            break
                    
                    elif str(reaction.emoji) == '🛑':
                        # Stand
                        break
                
                except asyncio.TimeoutError:
                    await ctx.send('⏰ Tempo esgotado! Parando automaticamente.')
                    break
            
            # Dealer's turn
            if not game.player_hand.is_busted():
                game.dealer_play()
            
            # Determine winner
            result, multiplier = game.determine_winner()
            
            # Process bet
            won = result in ['player_win', 'player_blackjack']
            if result == 'push':
                # Return bet
                net_change = 0
                self.db.record_game(str(ctx.author.id), 'blackjack', bet_amount, 'push', 0)
            else:
                success, net_change = self.economy.process_bet(
                    str(ctx.author.id),
                    ctx.author.name,
                    bet_amount,
                    'blackjack',
                    won,
                    multiplier
                )
            
            # Show final result
            embed = discord.Embed(
                title='🃏 Blackjack - Resultado',
                color=discord.Color.green() if won else discord.Color.red() if result != 'push' else discord.Color.blue()
            )
            
            embed.add_field(name='🎴 Sua Mão', value=game.get_player_hand_str(), inline=False)
            embed.add_field(name='🂠 Mão do Dealer', value=game.get_dealer_hand_str(), inline=False)
            
            if result == 'player_blackjack':
                embed.add_field(name='🎉 BLACKJACK!', value=f'+{net_change:,} 🪙', inline=False)
            elif result == 'player_win':
                embed.add_field(name='🎉 VOCÊ GANHOU!', value=f'+{net_change:,} 🪙', inline=False)
            elif result == 'dealer_win':
                embed.add_field(name='❌ Dealer Ganhou', value=f'{net_change:,} 🪙', inline=False)
            elif result == 'push':
                embed.add_field(name='🤝 Empate', value='Aposta devolvida', inline=False)
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Saldo atual: {user["coins"]:,} 🪙')
            
            await msg.edit(embed=embed)
            
            # Check achievements
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n{achievement_text}')
        
        finally:
            end_game(ctx.author.id)
    
    @commands.command(name='jogos', aliases=['games', 'listgames'])
    async def list_games(self, ctx):
        """Lista todos os jogos disponíveis"""
        embed = discord.Embed(
            title='🎰 Jogos de Cassino Disponíveis',
            description='Teste sua sorte e ganhe moedas!',
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name='🎰 Roleta',
            value=f'`{PREFIX}roleta <valor> <tipo> <aposta>`\nTipos: numero, cor, paridade, altura',
            inline=False
        )
        
        embed.add_field(
            name='🎰 Caça-Níqueis',
            value=f'`{PREFIX}slots <valor>`\nCombine 3 símbolos para ganhar!',
            inline=False
        )
        
        embed.add_field(
            name='🎲 Dados',
            value=f'`{PREFIX}dados <valor> <tipo>`\nTipos: acima, abaixo, sete, alto, baixo, 1-6',
            inline=False
        )
        
        embed.add_field(
            name='🃏 Blackjack',
            value=f'`{PREFIX}blackjack <valor>`\nChegue a 21 sem estourar!',
            inline=False
        )
        
        embed.set_footer(text='Aposta mínima: 10 🪙 | Use /saldo para ver suas moedas')
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(Games(bot))
