"""Casino games commands cog"""

import discord
from discord.ext import commands
import asyncio
import random
from src.database.db_manager import DatabaseManager
from src.economy.economy_manager import EconomyManager
from src.core.achievements import AchievementManager
from src.core.checks import ensure_not_playing, start_game, end_game
from src.core.mensagens import MensagensCasuais as MSG
from src.games.roulette import RouletteGame
from src.games.slots import SlotsGame
from src.games.dice import DiceGame
from src.games.blackjack import BlackjackGame
from src.games.tigrinho import TigrinhoGame
from src.games.mines import MinesGame
from src.games.crash import CrashGame
from src.games.double import DoubleGame
from src.games.coinflip import CoinFlipGame
from src.games.wheel import WheelGame
from src.games.keno import KenoGame
from src.games.plinko import PlinkoGame
from src.games.baccarat import BaccaratGame
from src.games.hilo import HiLoGame
from src.games.limbo import LimboGame
from src.games.tower import TowerGame
from src.games.scratch import ScratchCardGame
from src.games.videopoker import VideoPokerGame
from src.games.heist import HeistGame
from src.config import PREFIX
import time


class Games(commands.Cog):
    """Casino game commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.db = DatabaseManager()
        self.economy = EconomyManager(self.db)
        self.achievements = AchievementManager(self.db)
        self.heist_cooldowns = {}  # user_id: timestamp
        self.active_heists = {}  # message_id: heist_data
    
    async def check_balance(self, ctx, amount: int) -> bool:
        """Check if user can afford the bet"""
        user = self.db.get_user(str(ctx.author.id), ctx.author.name)
        
        # Check if balance is negative
        if user['coins'] < 0:
            await ctx.send(f'🚨 **YOU ARE IN DEBT!**\nBalance: **{user["coins"]:,} 🪙**\n\nPay your debts before playing!')
            return False
        
        if not self.economy.can_afford(str(ctx.author.id), ctx.author.name, amount):
            await ctx.send(MSG.saldo_insuficiente())
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
            await ctx.send(MSG.aposta_minima())
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
                await ctx.send(MSG.erro_processar())
                return
            
            # Create result embed
            embed = discord.Embed(
                title=f'🎰 European Roulette - {ctx.author.display_name}',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            color_emoji = {'vermelho': '🔴', 'preto': '⚫', 'verde': '🟢'}
            embed.add_field(
                name='Result',
                value=f'{color_emoji.get(color, "⚪")} **{number}** ({color})',
                inline=False
            )
            
            embed.add_field(name='Your Bet', value=f'{bet_type}: {bet_value}', inline=True)
            embed.add_field(name='Amount', value=f'{bet_amount:,} 🪙', inline=True)
            
            if won:
                embed.add_field(
                    name='🎉 WON!',
                    value=f'+{net_change:,} 🪙 (multiplicador: {multiplier}x)',
                    inline=False
                )
            else:
                embed.add_field(
                    name='❌ Lost',
                    value=f'{net_change:,} 🪙',
                    inline=False
                )
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            
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
            await ctx.send(MSG.aposta_minima())
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
                await ctx.send(MSG.erro_processar())
                return
            
            # Create result embed
            embed = discord.Embed(
                title=f'🎰 Slot Machine - {ctx.author.display_name}',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            embed.add_field(
                name='Result',
                value=f'**{SlotsGame.format_reels(reels)}**',
                inline=False
            )
            
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            
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
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            
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
            await ctx.send(MSG.aposta_minima())
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
                        await ctx.send('❌ Invalid bet type!')
                        return
                except ValueError:
                    await ctx.send('❌ Invalid bet type!')
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
                await ctx.send(MSG.erro_processar())
                return
            
            # Create result embed
            embed = discord.Embed(
                title=f'🎲 Dados - {ctx.author.display_name}',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            embed.add_field(name='Result', value=result_text, inline=False)
            embed.add_field(name='Your Bet', value=bet_type, inline=True)
            embed.add_field(name='Amount', value=f'{bet_amount:,} 🪙', inline=True)
            
            if won:
                embed.add_field(
                    name='🎉 WON!',
                    value=f'+{net_change:,} 🪙 ({multiplier}x)',
                    inline=False
                )
            else:
                embed.add_field(
                    name='❌ Lost',
                    value=f'{net_change:,} 🪙',
                    inline=False
                )
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            
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
            await ctx.send(MSG.aposta_minima())
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
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            
            msg = await ctx.send(embed=embed)
            
            # Try to add reactions, fall back to text input if forbidden
            use_reactions = True
            try:
                await msg.add_reaction('⬇️')  # Hit
                await msg.add_reaction('🛑')  # Stand
            except discord.Forbidden:
                use_reactions = False
                await ctx.send('💡 Digite `hit` para pedir carta ou `stand` para parar.')
            
            if use_reactions:
                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ['⬇️', '🛑'] and reaction.message.id == msg.id
            else:
                def check_msg(m):
                    return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['hit', 'stand', 'h', 's']
            
            # Player's turn
            while game.can_player_hit():
                try:
                    if use_reactions:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                        action = 'hit' if str(reaction.emoji) == '⬇️' else 'stand'
                    else:
                        response = await self.bot.wait_for('message', timeout=30.0, check=check_msg)
                        action = 'hit' if response.content.lower() in ['hit', 'h'] else 'stand'
                    
                    if action == 'hit':
                        # Hit
                        game.player_hit()
                        
                        embed = discord.Embed(
                            title='🃏 Blackjack',
                            description='Use ⬇️ para pedir carta (hit) ou 🛑 para parar (stand)' if use_reactions else 'Digite `hit` ou `stand`',
                            color=discord.Color.blue()
                        )
                        
                        embed.add_field(name='🎴 Sua Mão', value=game.get_player_hand_str(), inline=False)
                        embed.add_field(name='🂠 Mão do Dealer', value=game.get_dealer_hand_str(hide_second=True), inline=False)
                        
                        await msg.edit(embed=embed)
                        
                        if use_reactions:
                            try:
                                await msg.remove_reaction(reaction, user)
                            except discord.Forbidden:
                                pass  # Ignore if can't remove reactions
                        
                        if game.player_hand.is_busted():
                            break
                    
                    elif action == 'stand':
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
                title=f'🃏 Blackjack - {ctx.author.display_name}',
                color=discord.Color.green() if won else discord.Color.red() if result != 'push' else discord.Color.blue()
            )
            
            embed.add_field(name='🎴 Sua Mão', value=game.get_player_hand_str(), inline=False)
            embed.add_field(name='🂠 Mão do Dealer', value=game.get_dealer_hand_str(), inline=False)
            
            if result == 'player_blackjack':
                embed.add_field(name='🎉 BLACKJACK!', value=f'+{net_change:,} 🪙', inline=False)
            elif result == 'player_win':
                embed.add_field(name='🎉 YOU WON!', value=f'+{net_change:,} 🪙', inline=False)
            elif result == 'dealer_win':
                embed.add_field(name='❌ Dealer Ganhou', value=f'{net_change:,} 🪙', inline=False)
            elif result == 'push':
                embed.add_field(name='🤝 Tie', value='Bet returned', inline=False)
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            
            await msg.edit(embed=embed)
            
            # Check achievements
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n{achievement_text}')
        
        finally:
            end_game(ctx.author.id)
    
    @commands.command(name='tigrinho', aliases=['tiger', 'tigre'])
    async def tigrinho(self, ctx, bet_amount: int):
        """
        Joga Tigrinho (Fortune Tiger) - slot 3x3
        Uso: /tigrinho <valor>
        """
        if not await ensure_not_playing(ctx):
            return
        
        if bet_amount < 10:
            await ctx.send(MSG.aposta_minima())
            return
        
        if not await self.check_balance(ctx, bet_amount):
            return
        
        start_game(ctx.author.id, 'tigrinho')
        
        try:
            # Create spinning animation
            embed = discord.Embed(
                title='🐅 Tigrinho - Fortune Tiger',
                description=MSG.girando(),
                color=discord.Color.gold()
            )
            
            # Show initial spinning animation
            grid_display = TigrinhoGame.format_spinning_frame(0)
            embed.add_field(name='Grade', value=f'```\n{grid_display}\n```', inline=False)
            
            msg = await ctx.send(embed=embed)
            
            # Animate spinning
            for i in range(3):
                await asyncio.sleep(0.8)
                embed = discord.Embed(
                    title='🐅 Tigrinho - Fortune Tiger',
                    description=MSG.girando(),
                    color=discord.Color.gold()
                )
                grid_display = TigrinhoGame.format_spinning_frame(i)
                embed.add_field(name='Grade', value=f'```\n{grid_display}\n```', inline=False)
                await msg.edit(embed=embed)
            
            # Final spin
            grid = TigrinhoGame.spin()
            won, total_multiplier, win_descriptions = TigrinhoGame.calculate_win(grid)
            
            # Process bet
            success, net_change = self.economy.process_bet(
                str(ctx.author.id),
                ctx.author.name,
                bet_amount,
                'tigrinho',
                won,
                total_multiplier
            )
            
            if not success:
                await ctx.send(MSG.erro_processar())
                return
            
            # Create final result embed
            embed = discord.Embed(
                title=f'🐅 Tigrinho - {ctx.author.display_name}',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            grid_display = TigrinhoGame.format_grid(grid)
            embed.add_field(name='Result', value=f'```\n{grid_display}\n```', inline=False)
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            
            if won:
                win_text = '\n'.join(win_descriptions)
                embed.add_field(
                    name='🎉 WON!',
                    value=f'{win_text}\n\n**Total: +{net_change:,} 🪙 ({total_multiplier:.0f}x)**',
                    inline=False
                )
            else:
                embed.add_field(
                    name='❌ Sem combinações',
                    value=f'{net_change:,} 🪙',
                    inline=False
                )
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            
            await msg.edit(embed=embed)
            
            # Check achievements
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n{achievement_text}')
        
        finally:
            end_game(ctx.author.id)
    
    @commands.command(name='crash', aliases=['aviator'])
    async def crash(self, ctx, bet_amount: int, target_multiplier: float = 2.0):
        """
        Joga Crash - multiplier cresce até crashar
        Uso: /crash <valor> [multiplicador_alvo]
        Exemplo: /crash 100 2.5
        """
        if not await ensure_not_playing(ctx):
            return
        
        if bet_amount < 10:
            await ctx.send(MSG.aposta_minima())
            return
        
        if target_multiplier < 1.1 or target_multiplier > 100:
            await ctx.send('❌ O multiplicador deve estar entre 1.1x e 100x!')
            return
        
        if not await self.check_balance(ctx, bet_amount):
            return
        
        start_game(ctx.author.id, 'crash')
        
        try:
            # Generate crash point
            crash_point = CrashGame.generate_crash_point()
            
            # Create initial embed
            embed = discord.Embed(
                title='🚀 Crash',
                description=f'Alvo: **{target_multiplier:.2f}x**\n{CrashGame.get_risk_level(target_multiplier)}',
                color=discord.Color.blue()
            )
            
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            embed.add_field(name='🎯 Meta', value=f'{target_multiplier:.2f}x', inline=True)
            
            msg = await ctx.send(embed=embed)
            
            # Animate multiplier growth
            steps = CrashGame.get_multiplier_steps(crash_point, num_steps=8)
            
            for current in steps:
                await asyncio.sleep(0.6)
                
                # Check if we passed target
                if current >= target_multiplier:
                    break
                
                embed = discord.Embed(
                    title='🚀 Crash',
                    description=CrashGame.format_multiplier_animation(current),
                    color=discord.Color.blue()
                )
                
                embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
                embed.add_field(name='🎯 Meta', value=f'{target_multiplier:.2f}x', inline=True)
                
                await msg.edit(embed=embed)
            
            # Determine result
            won, final_multiplier = CrashGame.simulate_crash(crash_point, target_multiplier)
            
            # Process bet
            success, net_change = self.economy.process_bet(
                str(ctx.author.id),
                ctx.author.name,
                bet_amount,
                'crash',
                won,
                target_multiplier if won else 0
            )
            
            if not success:
                await ctx.send(MSG.erro_processar())
                return
            
            # Show final result
            if won:
                embed = discord.Embed(
                    title=f'🚀 Crash - {ctx.author.display_name}',
                    description=f'✅ You cashed out at **{target_multiplier:.2f}x**!',
                    color=discord.Color.green()
                )
                embed.add_field(
                    name='🎉 WON!',
                    value=f'+{net_change:,} 🪙 ({target_multiplier:.2f}x)',
                    inline=False
                )
                embed.add_field(
                    name='Crash Point',
                    value=f'O jogo crashou em {crash_point:.2f}x',
                    inline=False
                )
            else:
                embed = discord.Embed(
                    title=f'🚀 Crash - {ctx.author.display_name}',
                    description=CrashGame.format_crash(crash_point),
                    color=discord.Color.red()
                )
                embed.add_field(
                    name='❌ Lost',
                    value=f'{net_change:,} 🪙\nCrash antes do alvo {target_multiplier:.2f}x',
                    inline=False
                )
            
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            
            await msg.edit(embed=embed)
            
            # Check achievements
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n{achievement_text}')
        
        finally:
            end_game(ctx.author.id)
    
    @commands.command(name='double', aliases=['cor', 'color'])
    async def double(self, ctx, bet_amount: int, bet_color: str):
        """
        Joga Double - aposta em cores
        Uso: /double <valor> <cor>
        Cores: vermelho/red, preto/black, branco/white
        """
        if not await ensure_not_playing(ctx):
            return
        
        if bet_amount < 10:
            await ctx.send(MSG.aposta_minima())
            return
        
        if not DoubleGame.validate_color(bet_color):
            await ctx.send(
                f'❌ Cor inválida! Use: vermelho, preto ou branco\n\n'
                f'{DoubleGame.get_color_info()}'
            )
            return
        
        if not await self.check_balance(ctx, bet_amount):
            return
        
        start_game(ctx.author.id, 'double')
        
        try:
            # Show spinning animation
            embed = discord.Embed(
                title='🎡 Double - Roleta de Cores',
                description='🎲 Girando a roleta...',
                color=discord.Color.purple()
            )
            
            embed.add_field(name='Your Bet', value=bet_color.title(), inline=True)
            embed.add_field(name='Amount', value=f'{bet_amount:,} 🪙', inline=True)
            
            wheel_display = DoubleGame.format_wheel_animation()
            embed.add_field(name='Roleta', value=wheel_display, inline=False)
            
            # Show history
            if DoubleGame.history:
                embed.add_field(
                    name='Histórico Recente',
                    value=DoubleGame.format_history(),
                    inline=False
                )
            
            msg = await ctx.send(embed=embed)
            
            # Animate
            for _ in range(3):
                await asyncio.sleep(0.7)
                wheel_display = DoubleGame.format_wheel_animation()
                embed = discord.Embed(
                    title='🎡 Double - Roleta de Cores',
                    description='🎲 Girando a roleta...',
                    color=discord.Color.purple()
                )
                embed.add_field(name='Your Bet', value=bet_color.title(), inline=True)
                embed.add_field(name='Amount', value=f'{bet_amount:,} 🪙', inline=True)
                embed.add_field(name='Roleta', value=wheel_display, inline=False)
                await msg.edit(embed=embed)
            
            # Spin for result
            result = DoubleGame.spin()
            won, multiplier = DoubleGame.check_win(result, bet_color)
            
            # Process bet
            success, net_change = self.economy.process_bet(
                str(ctx.author.id),
                ctx.author.name,
                bet_amount,
                'double',
                won,
                multiplier
            )
            
            if not success:
                await ctx.send(MSG.erro_processar())
                return
            
            # Show final result
            embed = discord.Embed(
                title=f'🎡 Double - {ctx.author.display_name}',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            embed.add_field(
                name='Result',
                value=DoubleGame.format_result(result),
                inline=False
            )
            
            embed.add_field(name='Your Bet', value=bet_color.title(), inline=True)
            embed.add_field(name='Amount', value=f'{bet_amount:,} 🪙', inline=True)
            
            if won:
                embed.add_field(
                    name='🎉 WON!',
                    value=f'+{net_change:,} 🪙 ({multiplier:.0f}x)',
                    inline=False
                )
            else:
                embed.add_field(
                    name='❌ Lost',
                    value=f'{net_change:,} 🪙',
                    inline=False
                )
            
            # Show updated history
            embed.add_field(
                name='Histórico Recente',
                value=DoubleGame.format_history(),
                inline=False
            )
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            
            await msg.edit(embed=embed)
            
            # Check achievements
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n{achievement_text}')
        
        finally:
            end_game(ctx.author.id)
    
    @commands.command(name='mines', aliases=['campo', 'minas'])
    async def mines(self, ctx, bet_amount: int, difficulty: str = 'medio'):
        """
        Joga Mines - campo minado
        Uso: /mines <valor> [dificuldade]
        Dificuldades: facil, medio, dificil, extremo
        """
        if not await ensure_not_playing(ctx):
            return
        
        if bet_amount < 10:
            await ctx.send(MSG.aposta_minima())
            return
        
        difficulty_lower = difficulty.lower()
        if difficulty_lower not in ['facil', 'medio', 'dificil', 'extremo']:
            await ctx.send('❌ Dificuldade inválida! Use: facil, medio, dificil ou extremo')
            return
        
        if not await self.check_balance(ctx, bet_amount):
            return
        
        start_game(ctx.author.id, 'mines')
        
        try:
            # Create game
            grid_size, num_mines = MinesGame.get_difficulty_settings(difficulty_lower)
            game = MinesGame(grid_size, num_mines)
            
            # Show initial grid
            embed = discord.Embed(
                title='💣 Mines - Campo Minado',
                description=f'**Dificuldade:** {difficulty.title()}\n'
                           f'**Minas:** {num_mines}/{game.total_tiles}\n'
                           f'Use `revelar <linha> <coluna>` ou `sair` para sacar',
                color=discord.Color.blue()
            )
            
            grid_display = game.format_grid()
            embed.add_field(name='Grade', value=f'```\n{grid_display}\n```', inline=False)
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            embed.add_field(name='Multiplicador Atual', value=f'{game.get_multiplier():.2f}x', inline=True)
            embed.add_field(name='Tiles Seguros Restantes', value=f'{game.get_safe_tiles_remaining()}', inline=True)
            
            await ctx.send(embed=embed)
            
            # Game loop
            while not game.game_over:
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                
                try:
                    response = await self.bot.wait_for('message', timeout=60.0, check=check)
                    content = response.content.lower().strip()
                    
                    if content == 'sair' or content == 'cashout' or content == 'cash':
                        # Cash out
                        multiplier = game.cash_out()
                        
                        # Process win
                        success, net_change = self.economy.process_bet(
                            str(ctx.author.id),
                            ctx.author.name,
                            bet_amount,
                            'mines',
                            True,
                            multiplier
                        )
                        
                        embed = discord.Embed(
                            title=f'💣 Mines - {ctx.author.display_name}',
                            description=f'✅ You cashed out safely!',
                            color=discord.Color.green()
                        )
                        
                        grid_display = game.format_grid(reveal_all=True)
                        embed.add_field(name='Grade Final', value=f'```\n{grid_display}\n```', inline=False)
                        embed.add_field(
                            name='🎉 WON!',
                            value=f'+{net_change:,} 🪙 ({multiplier:.2f}x)',
                            inline=False
                        )
                        embed.add_field(name='Tiles Revelados', value=f'{len(game.revealed)}/{game.safe_tiles}', inline=True)
                        
                        user = self.db.get_user(str(ctx.author.id), ctx.author.name)
                        embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
                        
                        await ctx.send(embed=embed)
                        break
                    
                    elif content.startswith('revelar ') or content.startswith('r '):
                        # Reveal tile
                        parts = content.split()
                        if len(parts) != 3:
                            await ctx.send('❌ Formato: `revelar <linha> <coluna>` (exemplo: revelar 0 0)')
                            continue
                        
                        try:
                            row = int(parts[1])
                            col = int(parts[2])
                            
                            if row < 0 or row >= grid_size or col < 0 or col >= grid_size:
                                await ctx.send(f'❌ Posição inválida! Use valores entre 0 e {grid_size-1}')
                                continue
                            
                            is_safe, current_multiplier = game.reveal_tile(row, col)
                            
                            if not is_safe:
                                # Hit a mine!
                                success, net_change = self.economy.process_bet(
                                    str(ctx.author.id),
                                    ctx.author.name,
                                    bet_amount,
                                    'mines',
                                    False,
                                    0
                                )
                                
                                embed = discord.Embed(
                                    title=f'💣 Mines - {ctx.author.display_name}',
                                    description='💥 You hit a mine!',
                                    color=discord.Color.red()
                                )
                                
                                grid_display = game.format_grid(reveal_all=True)
                                embed.add_field(name='Grade Final', value=f'```\n{grid_display}\n```', inline=False)
                                embed.add_field(
                                    name='❌ Lost',
                                    value=f'{net_change:,} 🪙',
                                    inline=False
                                )
                                
                                user = self.db.get_user(str(ctx.author.id), ctx.author.name)
                                embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
                                
                                await ctx.send(embed=embed)
                                break
                            else:
                                # Safe tile!
                                embed = discord.Embed(
                                    title='💣 Mines - Campo Minado',
                                    description=f'✅ Tile seguro!\n**Dificuldade:** {difficulty.title()}\n'
                                               f'Use `revelar <linha> <coluna>` ou `sair` para sacar',
                                    color=discord.Color.blue()
                                )
                                
                                grid_display = game.format_grid()
                                embed.add_field(name='Grade', value=f'```\n{grid_display}\n```', inline=False)
                                embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
                                embed.add_field(name='Multiplicador Atual', value=f'{current_multiplier:.2f}x', inline=True)
                                embed.add_field(name='Tiles Seguros Restantes', value=f'{game.get_safe_tiles_remaining()}', inline=True)
                                embed.add_field(
                                    name='Ganho Potencial',
                                    value=f'{int(bet_amount * current_multiplier):,} 🪙',
                                    inline=True
                                )
                                
                                await ctx.send(embed=embed)
                                
                                # Check if all safe tiles revealed
                                if game.get_safe_tiles_remaining() == 0:
                                    # Perfect clear!
                                    multiplier = game.cash_out()
                                    
                                    success, net_change = self.economy.process_bet(
                                        str(ctx.author.id),
                                        ctx.author.name,
                                        bet_amount,
                                        'mines',
                                        True,
                                        multiplier
                                    )
                                    
                                    embed = discord.Embed(
                                        title=f'💣 Mines - {ctx.author.display_name}',
                                        description='🏆 You revealed all safe tiles!',
                                        color=discord.Color.gold()
                                    )
                                    
                                    grid_display = game.format_grid(reveal_all=True)
                                    embed.add_field(name='Grade Final', value=f'```\n{grid_display}\n```', inline=False)
                                    embed.add_field(
                                        name='🏆 VITÓRIA PERFEITA!',
                                        value=f'+{net_change:,} 🪙 ({multiplier:.2f}x)',
                                        inline=False
                                    )
                                    
                                    user = self.db.get_user(str(ctx.author.id), ctx.author.name)
                                    embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
                                    
                                    await ctx.send(embed=embed)
                                    break
                        
                        except ValueError:
                            await ctx.send('❌ Use números válidos para linha e coluna!')
                            continue
                    
                    else:
                        await ctx.send('❌ Comando inválido! Use `revelar <linha> <coluna>` ou `sair`')
                
                except asyncio.TimeoutError:
                    # Timeout - auto cash out
                    if len(game.revealed) > 0 and not game.hit_mine:
                        multiplier = game.cash_out()
                        
                        success, net_change = self.economy.process_bet(
                            str(ctx.author.id),
                            ctx.author.name,
                            bet_amount,
                            'mines',
                            True,
                            multiplier
                        )
                        
                        await ctx.send(
                            f'⏰ Tempo esgotado! Cash out automático.\n'
                            f'Ganho: +{net_change:,} 🪙 ({multiplier:.2f}x)'
                        )
                    else:
                        # No tiles revealed or hit mine
                        await ctx.send('⏰ Tempo esgotado! Aposta perdida.')
                    break
            
            # Check achievements
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n{achievement_text}')
        
        finally:
            end_game(ctx.author.id)
    
    @commands.command(name='coinflip', aliases=['moeda', 'cara', 'coroa', 'flip'])
    async def coinflip(self, ctx, bet_amount: int, choice: str):
        """
        Joga cara ou coroa
        Uso: /coinflip <valor> <escolha>
        Escolhas: cara, coroa, heads, tails
        """
        if not await ensure_not_playing(ctx):
            return
        
        if bet_amount < 10:
            await ctx.send(MSG.aposta_minima())
            return
        
        if not CoinFlipGame.validate_choice(choice):
            await ctx.send(MSG.escolha_invalida() + ' Use: cara, coroa, heads ou tails')
            return
        
        if not await self.check_balance(ctx, bet_amount):
            return
        
        start_game(ctx.author.id, 'coinflip')
        
        try:
            # Show flipping animation
            embed = discord.Embed(
                title='🪙 Cara ou Coroa',
                description='Flipping the coin...',
                color=discord.Color.blue()
            )
            msg = await ctx.send(embed=embed)
            
            for frame in CoinFlipGame.get_animation_frames():
                await asyncio.sleep(0.4)
                embed.description = f'{frame} Girando...'
                await msg.edit(embed=embed)
            
            # Flip coin
            result = CoinFlipGame.flip()
            won, multiplier = CoinFlipGame.check_win(result, choice)
            
            # Process bet
            success, net_change = self.economy.process_bet(
                str(ctx.author.id),
                ctx.author.name,
                bet_amount,
                'coinflip',
                won,
                multiplier
            )
            
            if not success:
                await ctx.send(MSG.erro_processar())
                return
            
            # Show result
            embed = discord.Embed(
                title=f'🪙 Cara ou Coroa - {ctx.author.display_name}',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            embed.add_field(name='Result', value=CoinFlipGame.format_result(result), inline=False)
            embed.add_field(name='Sua Escolha', value=choice.title(), inline=True)
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            
            if won:
                embed.add_field(
                    name='🎉 WON!',
                    value=f'+{net_change:,} 🪙 ({multiplier}x)',
                    inline=False
                )
            else:
                embed.add_field(
                    name='❌ Lost',
                    value=f'{net_change:,} 🪙',
                    inline=False
                )
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            
            await msg.edit(embed=embed)
            
            # Check achievements
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n{achievement_text}')
        
        finally:
            end_game(ctx.author.id)
    
    @commands.command(name='wheel', aliases=['roda', 'fortune'])
    async def wheel(self, ctx, bet_amount: int):
        """
        Joga Roda da Fortuna
        Uso: /wheel <valor>
        """
        if not await ensure_not_playing(ctx):
            return
        
        if bet_amount < 10:
            await ctx.send(MSG.aposta_minima())
            return
        
        if not await self.check_balance(ctx, bet_amount):
            return
        
        start_game(ctx.author.id, 'wheel')
        
        try:
            # Show spinning animation
            embed = discord.Embed(
                title='🎡 Roda da Fortuna',
                description=MSG.girando(),
                color=discord.Color.purple()
            )
            msg = await ctx.send(embed=embed)
            
            for _ in range(3):
                await asyncio.sleep(0.6)
            
            # Spin wheel
            segment = WheelGame.spin()
            won, multiplier, description = WheelGame.calculate_win(segment)
            
            # Process bet
            success, net_change = self.economy.process_bet(
                str(ctx.author.id),
                ctx.author.name,
                bet_amount,
                'wheel',
                won,
                multiplier
            )
            
            if not success:
                await ctx.send(MSG.erro_processar())
                return
            
            # Show result
            embed = discord.Embed(
                title=f'🎡 Roda da Fortuna - {ctx.author.display_name}',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            embed.add_field(name='Result', value=WheelGame.format_result(segment), inline=False)
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            
            if won:
                embed.add_field(
                    name='🎉 Prêmio!',
                    value=f'+{net_change:,} 🪙 ({multiplier}x)',
                    inline=False
                )
            else:
                embed.add_field(
                    name='❌ Sem prêmio',
                    value=f'{net_change:,} 🪙',
                    inline=False
                )
            
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            
            await msg.edit(embed=embed)
            
            # Check achievements
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                achievement_text = '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements])
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n{achievement_text}')
        
        finally:
            end_game(ctx.author.id)
    

    @commands.command(name='plinko', aliases=['pl'])
    async def plinko(self, ctx, bet_amount: int, risk: str = 'medio'):
        """Plinko - bola cai por pinos. Uso: /plinko <valor> [risco]"""
        if not await ensure_not_playing(ctx) or bet_amount < 10 or not PlinkoGame.validate_risk(risk) or not await self.check_balance(ctx, bet_amount):
            if bet_amount < 10: await ctx.send(MSG.aposta_minima())
            elif not PlinkoGame.validate_risk(risk): await ctx.send(MSG.escolha_invalida() + ' Use: baixo, medio ou alto')
            return
        start_game(ctx.author.id, 'plinko')
        try:
            embed = discord.Embed(title='🎯 Plinko', description=f'{PlinkoGame.get_risk_description(risk)}\n\nSoltando a bola...', color=discord.Color.blue())
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            slot = PlinkoGame.drop_ball()
            won, multiplier = PlinkoGame.calculate_win(slot, risk)
            success, net_change = self.economy.process_bet(str(ctx.author.id), ctx.author.name, bet_amount, 'plinko', won, multiplier)
            if not success: await ctx.send(MSG.erro_processar()); return
            embed = discord.Embed(title=f'🎯 Plinko - {ctx.author.display_name}', description=PlinkoGame.format_board(slot, risk), color=discord.Color.green() if won else discord.Color.red())
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            embed.add_field(name='Slot', value=f'**{slot}** ({multiplier}x)', inline=True)
            embed.add_field(name='🎉 WON!' if won else '❌ Lost', value=f'{net_change:+,} 🪙', inline=False)
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            await msg.edit(embed=embed)
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n' + '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements]))
        finally:
            end_game(ctx.author.id)

    @commands.command(name='limbo', aliases=['lb'])
    async def limbo(self, ctx, bet_amount: int, target: float):
        """Limbo - resultado precisa passar o alvo. Uso: /limbo <valor> <multiplicador>"""
        if not await ensure_not_playing(ctx) or bet_amount < 10 or not LimboGame.validate_target(target) or not await self.check_balance(ctx, bet_amount):
            if bet_amount < 10: await ctx.send(MSG.aposta_minima())
            elif not LimboGame.validate_target(target): await ctx.send(f'❌ Multiplicador entre {LimboGame.MIN_TARGET}x e {LimboGame.MAX_TARGET}x!')
            return
        start_game(ctx.author.id, 'limbo')
        try:
            win_chance = LimboGame.calculate_win_chance(target)
            embed = discord.Embed(title='🎲 Limbo', description=f'{LimboGame.get_risk_level(target)}\nAlvo: **{target}x**\nChance: ~{win_chance:.1f}%\n\nGerando...', color=discord.Color.blue())
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(1.2)
            result = LimboGame.generate_result()
            won, multiplier = LimboGame.check_win(result, target)
            success, net_change = self.economy.process_bet(str(ctx.author.id), ctx.author.name, bet_amount, 'limbo', won, multiplier)
            if not success: await ctx.send(MSG.erro_processar()); return
            embed = discord.Embed(title=f'🎲 Limbo - {ctx.author.display_name}', description=LimboGame.format_result(result, target, won), color=discord.Color.green() if won else discord.Color.red())
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            embed.add_field(name='Alvo', value=f'{target}x', inline=True)
            embed.add_field(name='🎉 WON!' if won else '❌ Lost', value=f'{net_change:+,} 🪙' + (f' ({multiplier}x)' if won else ''), inline=False)
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            await msg.edit(embed=embed)
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n' + '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements]))
        finally:
            end_game(ctx.author.id)

    @commands.command(name='scratch', aliases=['raspadinha', 'sc'])
    async def scratch(self, ctx, bet_amount: int):
        """Raspadinha - cartão instantâneo. Uso: /scratch <valor>"""
        if not await ensure_not_playing(ctx) or bet_amount < 10 or not await self.check_balance(ctx, bet_amount):
            if bet_amount < 10: await ctx.send(MSG.aposta_minima())
            return
        start_game(ctx.author.id, 'scratch')
        try:
            embed = discord.Embed(title='🎫 Raspadinha', description='Raspando...', color=discord.Color.gold())
            embed.add_field(name='Cartão', value=ScratchCardGame.format_card_hidden(), inline=False)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            card = ScratchCardGame.generate_card()
            won, multiplier, best_prize = ScratchCardGame.calculate_best_prize(card)
            success, net_change = self.economy.process_bet(str(ctx.author.id), ctx.author.name, bet_amount, 'scratch', won, multiplier)
            if not success: await ctx.send(MSG.erro_processar()); return
            best_index = card.index(best_prize)
            embed = discord.Embed(title=f'🎫 Raspadinha - {ctx.author.display_name}', color=discord.Color.green() if won else discord.Color.red())
            embed.add_field(name='Cartão', value=ScratchCardGame.format_card_revealed(card, best_index), inline=False)
            embed.add_field(name='Prêmio', value=f'{best_prize["emoji"]} {best_prize["label"]}', inline=True)
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            embed.add_field(name='🎉 WON!' if won else '❌ Lost', value=f'{net_change:+,} 🪙' + (f' ({multiplier}x)' if won else ''), inline=False)
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            await msg.edit(embed=embed)
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n' + '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements]))
        finally:
            end_game(ctx.author.id)

    @commands.command(name='keno', aliases=['kn'])
    async def keno(self, ctx, bet_amount: int, *numbers: int):
        """Keno - loteria. Uso: /keno <valor> <num1> <num2> ... (1-10 números entre 1-40)"""
        if not await ensure_not_playing(ctx) or bet_amount < 10:
            if bet_amount < 10: await ctx.send(MSG.aposta_minima())
            return
        numbers_list = list(numbers)
        if not KenoGame.validate_numbers(numbers_list, len(numbers_list)):
            await ctx.send(f'❌ Escolha de {KenoGame.MIN_NUMBERS} a {KenoGame.MAX_NUMBERS} números únicos entre 1 e {KenoGame.NUMBER_RANGE}!'); return
        if not await self.check_balance(ctx, bet_amount): return
        start_game(ctx.author.id, 'keno')
        try:
            embed = discord.Embed(title='🎱 Keno', description=f'Seus números: {KenoGame.format_numbers(numbers_list)}\n\nSorteando...', color=discord.Color.blue())
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            drawn = KenoGame.draw_numbers()
            matches = KenoGame.check_matches(numbers_list, drawn)
            won, multiplier = KenoGame.calculate_win(len(numbers_list), matches)
            success, net_change = self.economy.process_bet(str(ctx.author.id), ctx.author.name, bet_amount, 'keno', won, multiplier)
            if not success: await ctx.send(MSG.erro_processar()); return
            embed = discord.Embed(title=f'🎱 Keno - {ctx.author.display_name}', color=discord.Color.green() if won else discord.Color.red())
            embed.add_field(name='Seus Números', value=KenoGame.format_numbers(numbers_list, drawn), inline=False)
            embed.add_field(name='Sorteados', value=KenoGame.format_numbers(drawn), inline=False)
            embed.add_field(name='Acertos', value=f'**{matches}/{len(numbers_list)}**', inline=True)
            embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
            embed.add_field(name='🎉 WON!' if won else '❌ Lost', value=f'{net_change:+,} 🪙' + (f' ({multiplier}x)' if won else ''), inline=False)
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            await msg.edit(embed=embed)
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n' + '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements]))
        finally:
            end_game(ctx.author.id)



    @commands.command(name='baccarat', aliases=['bac'])
    async def baccarat(self, ctx, bet_amount: int, bet_type: str):
        """Baccarat - jogue contra a banca. Uso: /baccarat <valor> <jogador|banca|empate>"""
        if not await ensure_not_playing(ctx) or bet_amount < 10 or not BaccaratGame.validate_bet(bet_type) or not await self.check_balance(ctx, bet_amount):
            if bet_amount < 10: await ctx.send(MSG.aposta_minima())
            elif not BaccaratGame.validate_bet(bet_type): await ctx.send('❌ Aposta inválida! Use: jogador, banca ou empate')
            return
        start_game(ctx.author.id, 'baccarat')
        try:
            embed = discord.Embed(title='🎴 Baccarat', description='Distribuindo cartas...', color=discord.Color.blue())
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(1.2)
            winner, player_hand, banker_hand, player_value, banker_value = BaccaratGame.play_game()
            won, multiplier = BaccaratGame.calculate_win(winner, bet_type)
            success, net_change = self.economy.process_bet(str(ctx.author.id), ctx.author.name, bet_amount, 'baccarat', won, multiplier)
            if not success: await ctx.send(MSG.erro_processar()); return
            embed = discord.Embed(title=f'🎴 Baccarat - {ctx.author.display_name}', color=discord.Color.green() if won else discord.Color.red())
            embed.add_field(name='Jogador', value=BaccaratGame.format_hand(player_hand, player_value), inline=False)
            embed.add_field(name='Banca', value=BaccaratGame.format_hand(banker_hand, banker_value), inline=False)
            embed.add_field(name='Vencedor', value=winner.title(), inline=True)
            embed.add_field(name='Your Bet', value=bet_type.title(), inline=True)
            embed.add_field(name='🎉 WON!' if won else '❌ Lost', value=f'{net_change:+,} 🪙' + (f' ({multiplier}x)' if won else ''), inline=False)
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            await msg.edit(embed=embed)
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n' + '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements]))
        finally:
            end_game(ctx.author.id)

    @commands.command(name='hilo', aliases=['highlow', 'hl'])
    async def hilo(self, ctx, bet_amount: int, guess: str):
        """Hi-Lo - próxima carta maior ou menor. Uso: /hilo <valor> <alto|baixo|igual>"""
        if not await ensure_not_playing(ctx) or bet_amount < 10 or not HiLoGame.validate_guess(guess) or not await self.check_balance(ctx, bet_amount):
            if bet_amount < 10: await ctx.send(MSG.aposta_minima())
            elif not HiLoGame.validate_guess(guess): await ctx.send('❌ Escolha inválida! Use: alto, baixo ou igual')
            return
        start_game(ctx.author.id, 'hilo')
        try:
            current = HiLoGame.draw_card()
            embed = discord.Embed(title='🎴 Hi-Lo', description=f'Carta atual: {HiLoGame.format_card(current)}\n\n{HiLoGame.get_odds(current)}\n\nSua escolha: **{guess.title()}**\n\nRevelando próxima carta...', color=discord.Color.blue())
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            next_card = HiLoGame.draw_card()
            won, multiplier = HiLoGame.compare_cards(current, next_card, guess)
            success, net_change = self.economy.process_bet(str(ctx.author.id), ctx.author.name, bet_amount, 'hilo', won, multiplier)
            if not success: await ctx.send(MSG.erro_processar()); return
            embed = discord.Embed(title=f'🎴 Hi-Lo - {ctx.author.display_name}', color=discord.Color.green() if won else discord.Color.red())
            embed.add_field(name='Carta Anterior', value=HiLoGame.format_card(current), inline=True)
            embed.add_field(name='Nova Carta', value=HiLoGame.format_card(next_card), inline=True)
            embed.add_field(name='Sua Escolha', value=guess.title(), inline=True)
            embed.add_field(name='🎉 WON!' if won else '❌ Lost', value=f'{net_change:+,} 🪙' + (f' ({multiplier}x)' if won else ''), inline=False)
            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
            await msg.edit(embed=embed)
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n' + '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements]))
        finally:
            end_game(ctx.author.id)

    @commands.command(name='tower', aliases=['torre', 'tw'])
    async def tower(self, ctx, bet_amount: int, difficulty: str = 'medio'):
        """Tower - suba a torre interativo. Uso: /tower <valor> [dificuldade]"""
        if not await ensure_not_playing(ctx) or bet_amount < 10 or not TowerGame.validate_difficulty(difficulty) or not await self.check_balance(ctx, bet_amount):
            if bet_amount < 10: await ctx.send(MSG.aposta_minima())
            elif not TowerGame.validate_difficulty(difficulty): await ctx.send('❌ Dificuldade inválida! Use: facil, medio, dificil, extremo')
            return
        start_game(ctx.author.id, 'tower')
        try:
            game = TowerGame(difficulty)
            embed = discord.Embed(title='🗼 Tower', description=f'{TowerGame.get_difficulty_info(difficulty)}\n\nEscolha um tile (0-{game.tiles_per_level-1}) ou digite `sair` para sacar', color=discord.Color.blue())
            embed.add_field(name='Torre', value=f'```\n{game.format_tower()}\n```', inline=False)
            embed.add_field(name='Multiplicador', value=f'{game.get_multiplier():.2f}x', inline=True)
            await ctx.send(embed=embed)
            
            while not game.game_over:
                def check(m): return m.author == ctx.author and m.channel == ctx.channel
                try:
                    response = await self.bot.wait_for('message', timeout=60.0, check=check)
                    content = response.content.lower().strip()
                    if content in ['sair', 'cashout']:
                        multiplier = game.cash_out()
                        success, net_change = self.economy.process_bet(str(ctx.author.id), ctx.author.name, bet_amount, 'tower', True, multiplier)
                        embed = discord.Embed(title=f'🗼 Tower - {ctx.author.display_name}', description='✅ Cash out!', color=discord.Color.green())
                        embed.add_field(name='Torre', value=f'```\n{game.format_tower(True)}\n```', inline=False)
                        embed.add_field(name='🎉 WON!', value=f'+{net_change:,} 🪙 ({multiplier:.2f}x)', inline=False)
                        user = self.db.get_user(str(ctx.author.id), ctx.author.name)
                        embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
                        await ctx.send(embed=embed)
                        break
                    try:
                        tile_index = int(content)
                        is_safe, current_mult = game.choose_tile(tile_index)
                        if not is_safe:
                            success, net_change = self.economy.process_bet(str(ctx.author.id), ctx.author.name, bet_amount, 'tower', False, 0)
                            embed = discord.Embed(title=f'🗼 Tower - {ctx.author.display_name}', description='💥 Tile errado!', color=discord.Color.red())
                            embed.add_field(name='Torre', value=f'```\n{game.format_tower(True)}\n```', inline=False)
                            embed.add_field(name='❌ Lost', value=f'{net_change:,} 🪙', inline=False)
                            user = self.db.get_user(str(ctx.author.id), ctx.author.name)
                            embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
                            await ctx.send(embed=embed)
                            break
                        else:
                            if game.won:
                                success, net_change = self.economy.process_bet(str(ctx.author.id), ctx.author.name, bet_amount, 'tower', True, current_mult)
                                embed = discord.Embed(title=f'🗼 Tower - {ctx.author.display_name}', description='🏆 Topo alcançado!', color=discord.Color.gold())
                                embed.add_field(name='Torre', value=f'```\n{game.format_tower(True)}\n```', inline=False)
                                embed.add_field(name='🏆 VITÓRIA!', value=f'+{net_change:,} 🪙 ({current_mult:.2f}x)', inline=False)
                                user = self.db.get_user(str(ctx.author.id), ctx.author.name)
                                embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
                                await ctx.send(embed=embed)
                                break
                            embed = discord.Embed(title='🗼 Tower', description=f'✅ Seguro! Nível {game.current_level}\n\nEscolha próximo tile ou `sair`', color=discord.Color.blue())
                            embed.add_field(name='Torre', value=f'```\n{game.format_tower()}\n```', inline=False)
                            embed.add_field(name='Multiplicador', value=f'{current_mult:.2f}x', inline=True)
                            embed.add_field(name='Ganho Potencial', value=f'{int(bet_amount * current_mult):,} 🪙', inline=True)
                            await ctx.send(embed=embed)
                    except ValueError:
                        await ctx.send('❌ Use um número válido ou `sair`!')
                except asyncio.TimeoutError:
                    if game.current_level > 0:
                        multiplier = game.cash_out()
                        success, net_change = self.economy.process_bet(str(ctx.author.id), ctx.author.name, bet_amount, 'tower', True, multiplier)
                        await ctx.send(f'⏰ Tempo esgotado! Cash out automático: +{net_change:,} 🪙')
                    else:
                        await ctx.send('⏰ Tempo esgotado!')
                    break
            
            new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
            if new_achievements:
                await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n' + '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements]))
        finally:
            end_game(ctx.author.id)

    @commands.command(name='videopoker', aliases=['poker', 'vp'])
    async def videopoker(self, ctx, bet_amount: int):
        """Video Poker - Jacks or Better. Uso: /videopoker <valor>"""
        if not await ensure_not_playing(ctx) or bet_amount < 10 or not await self.check_balance(ctx, bet_amount):
            if bet_amount < 10: await ctx.send(MSG.aposta_minima())
            return
        start_game(ctx.author.id, 'videopoker')
        try:
            game = VideoPokerGame()
            hand = game.deal()
            embed = discord.Embed(title='🎰 Video Poker', description='Digite os números das cartas para segurar (0-4) separados por espaço.\nExemplo: `0 2 4` ou `todas` ou `nenhuma`', color=discord.Color.blue())
            embed.add_field(name='Sua Mão', value=game.format_hand_with_positions(), inline=False)
            await ctx.send(embed=embed)
            
            def check(m): return m.author == ctx.author and m.channel == ctx.channel
            try:
                response = await self.bot.wait_for('message', timeout=30.0, check=check)
                content = response.content.lower().strip()
                if content in ['todas', 'all']:
                    game.hold_cards([0, 1, 2, 3, 4])
                elif content in ['nenhuma', 'none', '']:
                    game.hold_cards([])
                else:
                    try:
                        positions = [int(x) for x in content.split()]
                        if not game.hold_cards(positions):
                            await ctx.send('❌ Posições inválidas!'); return
                    except ValueError:
                        await ctx.send('❌ Digite números válidos!'); return
                
                final_hand = game.draw()
                hand_name, multiplier = game.evaluate_hand()
                won = multiplier > 0
                success, net_change = self.economy.process_bet(str(ctx.author.id), ctx.author.name, bet_amount, 'videopoker', won, multiplier)
                if not success: await ctx.send(MSG.erro_processar()); return
                
                embed = discord.Embed(title=f'🎰 Video Poker - {ctx.author.display_name}', color=discord.Color.green() if won else discord.Color.red())
                embed.add_field(name='Mão Final', value=game.format_hand(show_held=True), inline=False)
                embed.add_field(name='Result', value=hand_name, inline=True)
                embed.add_field(name='Bet', value=f'{bet_amount:,} 🪙', inline=True)
                embed.add_field(name='🎉 WON!' if won else '❌ Lost', value=f'{net_change:+,} 🪙' + (f' ({multiplier}x)' if won else ''), inline=False)
                user = self.db.get_user(str(ctx.author.id), ctx.author.name)
                embed.set_footer(text=f'Current balance: {user["coins"]:,} 🪙')
                await ctx.send(embed=embed)
                
                new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
                if new_achievements:
                    await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n' + '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements]))
            except asyncio.TimeoutError:
                await ctx.send('⏰ Tempo esgotado!')
        finally:
            end_game(ctx.author.id)


    @commands.command(name='jogos', aliases=['games', 'listgames'])
    async def list_games(self, ctx):
        """Lista todos os jogos disponíveis"""
        embed = discord.Embed(
            title='🎰 Jogos de Cassino Disponíveis',
            description='Test your luck and win coins! 18 games available!',
            color=discord.Color.purple()
        )
        
        # Original games
        embed.add_field(
            name='🐅 Tigrinho (Fortune Tiger)',
            value=f'`{PREFIX}tigrinho <valor>`\nSlot 3x3 com múltiplas linhas!',
            inline=True
        )
        
        embed.add_field(
            name='🚀 Crash',
            value=f'`{PREFIX}crash <valor> [mult]`\nMultiplicador até crashar!',
            inline=True
        )
        
        embed.add_field(
            name='🎡 Double',
            value=f'`{PREFIX}double <valor> <cor>`\nVermelho/Preto (2x), Branco (14x)',
            inline=True
        )
        
        embed.add_field(
            name='💣 Mines',
            value=f'`{PREFIX}mines <valor> [dif]`\nCampo minado interativo!',
            inline=True
        )
        
        embed.add_field(
            name='🎰 Roleta',
            value=f'`{PREFIX}roleta <valor> <tipo> <aposta>`\nRoleta europeia clássica',
            inline=True
        )
        
        embed.add_field(
            name='🎰 Slot Machine',
            value=f'`{PREFIX}slots <valor>`\nCombine 3 símbolos!',
            inline=True
        )
        
        embed.add_field(
            name='🎲 Dados',
            value=f'`{PREFIX}dados <valor> <tipo>`\nAcima, abaixo, número...',
            inline=True
        )
        
        embed.add_field(
            name='🃏 Blackjack',
            value=f'`{PREFIX}blackjack <valor>`\nChegue a 21!',
            inline=True
        )
        
        # New games
        embed.add_field(
            name='🪙 Cara ou Coroa',
            value=f'`{PREFIX}coinflip <valor> <cara|coroa>`\nSimples e rápido!',
            inline=True
        )
        
        embed.add_field(
            name='🎡 Roda da Fortuna',
            value=f'`{PREFIX}wheel <valor>`\nGire para ganhar prêmios!',
            inline=True
        )
        
        embed.add_field(
            name='🎯 Plinko',
            value=f'`{PREFIX}plinko <valor> [risco]`\nBola cai por pinos!',
            inline=True
        )
        
        embed.add_field(
            name='🎲 Limbo',
            value=f'`{PREFIX}limbo <valor> <alvo>`\nPasse o multiplicador!',
            inline=True
        )
        
        embed.add_field(
            name='🎫 Raspadinha',
            value=f'`{PREFIX}scratch <valor>`\nCartão instantâneo!',
            inline=True
        )
        
        embed.add_field(
            name='🎱 Keno',
            value=f'`{PREFIX}keno <valor> <nums...>`\nLoteria de números!',
            inline=True
        )
        
        embed.add_field(
            name='🎴 Baccarat',
            value=f'`{PREFIX}baccarat <valor> <tipo>`\nJogador, banca ou empate',
            inline=True
        )
        
        embed.add_field(
            name='🎴 Hi-Lo',
            value=f'`{PREFIX}hilo <valor> <alto|baixo|igual>`\nPróxima carta!',
            inline=True
        )
        
        embed.add_field(
            name='🗼 Tower',
            value=f'`{PREFIX}tower <valor> [dif]`\nSuba a torre!',
            inline=True
        )
        
        embed.add_field(
            name='🎰 Video Poker',
            value=f'`{PREFIX}videopoker <valor>`\nJacks or Better!',
            inline=True
        )
        
        embed.set_footer(text='Minimum bet: 10 🪙 | Use /balance to check your coins')
        
        await ctx.send(embed=embed)

    @commands.command(name='roubar', aliases=['rob', 'steal', 'heist'])
    async def heist(self, ctx, target: discord.Member):
        """
        Try to steal coins from another player!
        O alvo tem 15 segundos para defender respondendo um desafio.
        Uso: /roubar @usuario
        """
        
        # Verificações básicas
        if target.id == ctx.author.id:
            await ctx.send('❌ You can\'t steal from yourself!')
            return
        
        if target.bot:
            await ctx.send('❌ Não dá pra roubar de bot não, espertão!')
            return
        
        # Verificar cooldown
        current_time = time.time()
        if ctx.author.id in self.heist_cooldowns:
            time_left = HeistGame.COOLDOWN - (current_time - self.heist_cooldowns[ctx.author.id])
            if time_left > 0:
                minutes = int(time_left // 60)
                seconds = int(time_left % 60)
                await ctx.send(f'⏰ Calma aí ladrão! Espera mais **{minutes}m {seconds}s** antes de tentar roubar de novo.')
                return
        
        # Check balances
        robber = self.db.get_user(str(ctx.author.id), ctx.author.name)
        victim = self.db.get_user(str(target.id), target.name)
        
        # Verificar se o ladrão está negativado
        if robber['coins'] < 0:
            await ctx.send(f'❌ You are in debt! Pay off your debts first (balance: **{robber["coins"]:,} 🪙**)')
            return
        
        can_rob, error_msg = HeistGame.can_rob(robber['coins'], victim['coins'])
        if not can_rob:
            await ctx.send(f'❌ {error_msg}')
            return
        
        # Calcular quantidade a roubar
        steal_amount = HeistGame.calculate_steal_amount(victim['coins'])
        
        # Debug log
        print(f"[HEIST] Victim: {target.name} | Balance: {victim['coins']:,} | Amount stolen: {steal_amount:,}")
        
        # Gerar desafio de defesa
        challenge_type, question, correct_answer = HeistGame.generate_challenge()
        
        # Mensagem inicial
        embed = discord.Embed(
            title='🚨 ROUBO EM ANDAMENTO! 🚨',
            description=f'**{ctx.author.display_name}** está tentando roubar **{target.display_name}**!',
            color=discord.Color.red()
        )
        
        embed.add_field(
            name='💰 Em Jogo',
            value=f'{steal_amount:,} 🪙 ({HeistGame.get_loot_description(steal_amount)})',
            inline=False
        )
        
        embed.add_field(
            name=f'{challenge_type["emoji"]} DESAFIO: {challenge_type["name"]}',
            value=f'{question}\n\n{target.mention} responda em **{HeistGame.DEFENSE_TIME} segundos**!',
            inline=False
        )
        
        embed.add_field(
            name='⚔️ Como Funciona',
            value='• Responda corretamente = Defende e ladrão paga multa\n• Errar/Demorar = Ladrão leva a grana',
            inline=False
        )
        
        embed.set_footer(text=f'Dificuldade: {challenge_type["difficulty"]} | Tempo: {HeistGame.DEFENSE_TIME}s')
        
        heist_msg = await ctx.send(embed=embed)
        
        # Armazenar dados do roubo
        self.active_heists[heist_msg.id] = {
            'robber_id': ctx.author.id,
            'robber_name': ctx.author.display_name,
            'target_id': target.id,
            'target_name': target.display_name,
            'amount': steal_amount,
            'correct_answer': correct_answer,
            'challenge_type': challenge_type['type'],
            'start_time': current_time
        }
        
        # Aguardar resposta
        def check(m):
            return m.author.id == target.id and m.channel.id == ctx.channel.id
        
        try:
            response = await self.bot.wait_for('message', timeout=HeistGame.DEFENSE_TIME, check=check)
            
            # Verificar resposta
            is_correct = HeistGame.check_answer(response.content, correct_answer, challenge_type['type'])
            
            if is_correct:
                # DEFESA BEM SUCEDIDA!
                penalty = int(robber['coins'] * HeistGame.FAIL_PENALTY_PERCENT)
                penalty = min(penalty, steal_amount)  # Máximo = valor que ia roubar
                
                # Se o ladrão não tem dinheiro suficiente, usa o que tem e negativa
                actual_penalty = penalty
                robber_balance = robber['coins']
                went_negative = False
                
                if robber_balance < penalty:
                    # Ladrão não tem dinheiro suficiente, vai ficar negativo
                    went_negative = True
                    actual_penalty = penalty  # Cobra a multa completa mesmo que não tenha
                
                # Transferir penalidade do ladrão para a vítima (pode deixar negativo)
                self.economy.remove_coins(str(ctx.author.id), actual_penalty, 'Penalidade de roubo falho')
                self.economy.add_coins(str(target.id), actual_penalty, 'Defesa de roubo')
                
                defense_msg = random.choice(HeistGame.get_defense_messages())
                
                embed = discord.Embed(
                    title='🛡️ DEFESA BEM SUCEDIDA!',
                    description=f'**{target.display_name}** {defense_msg}!',
                    color=discord.Color.green()
                )
                
                embed.add_field(
                    name='✅ Resposta Correta',
                    value=f'**{response.content}**',
                    inline=False
                )
                
                penalty_text = f'**{ctx.author.display_name}** pagou **{actual_penalty:,} 🪙** de multa!'
                if went_negative:
                    new_balance = robber_balance - actual_penalty
                    penalty_text += f'\n⚠️ **IN DEBT!** Balance is now **{new_balance:,} 🪙**'
                
                embed.add_field(
                    name='💸 Penalidade do Ladrão',
                    value=penalty_text,
                    inline=False
                )
                
                if went_negative:
                    embed.set_footer(text='Crime não compensa! Agora está devendo!')
                else:
                    embed.set_footer(text='Crime não compensa!')
                
                await ctx.send(embed=embed)
                
            else:
                # ROUBO BEM SUCEDIDO!
                self.economy.remove_coins(str(target.id), steal_amount, f'Roubado por {ctx.author.name}')
                self.economy.add_coins(str(ctx.author.id), steal_amount, f'Roubou de {target.name}')
                
                success_msg = random.choice(HeistGame.get_success_messages())
                
                embed = discord.Embed(
                    title='💰 ROUBO BEM SUCEDIDO!',
                    description=f'**{ctx.author.display_name}** {success_msg} de **{target.display_name}**!',
                    color=discord.Color.gold()
                )
                
                embed.add_field(
                    name='❌ Resposta Errada',
                    value=f'You said: **{response.content}**\nCorrect was: **{correct_answer}**',
                    inline=False
                )
                
                embed.add_field(
                    name='💰 Lucro do Ladrão',
                    value=f'**+{steal_amount:,} 🪙**',
                    inline=False
                )
                
                embed.set_footer(text='Deveria ter estudado mais!')
                await ctx.send(embed=embed)
                
                # Adicionar cooldown
                self.heist_cooldowns[ctx.author.id] = current_time
        
        except asyncio.TimeoutError:
            # TEMPO ESGOTADO - ROUBO BEM SUCEDIDO!
            self.economy.remove_coins(str(target.id), steal_amount, f'Roubado por {ctx.author.name}')
            self.economy.add_coins(str(ctx.author.id), steal_amount, f'Roubou de {target.name}')
            
            success_msg = random.choice(HeistGame.get_success_messages())
            
            embed = discord.Embed(
                title='💰 ROUBO BEM SUCEDIDO!',
                description=f'**{ctx.author.display_name}** {success_msg} de **{target.display_name}**!',
                color=discord.Color.gold()
            )
            
            embed.add_field(
                name='⏰ Tempo Esgotado!',
                value=f'{target.display_name} não respondeu a tempo...',
                inline=False
            )
            
            embed.add_field(
                name='💰 Lucro do Ladrão',
                value=f'**+{steal_amount:,} 🪙**',
                inline=False
            )
            
            embed.add_field(
                name='💡 Resposta Correta Era',
                value=f'**{correct_answer}**',
                inline=False
            )
            
            embed.set_footer(text='Dormiu no ponto!')
            await ctx.send(embed=embed)
            
            # Adicionar cooldown
            self.heist_cooldowns[ctx.author.id] = current_time
        
        # Limpar dados do roubo
        if heist_msg.id in self.active_heists:
            del self.active_heists[heist_msg.id]
        
        # Verificar conquistas
        new_achievements = self.achievements.check_achievements(str(ctx.author.id), ctx.author.name)
        if new_achievements:
            await ctx.send(f'🏆 **Conquistas Desbloqueadas!**\n' + '\n'.join([f'{a.emoji} **{a.title}** (+{a.reward} 🪙)' for a in new_achievements]))


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(Games(bot))
