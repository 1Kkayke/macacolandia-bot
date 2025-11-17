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
from src.games.tigrinho import TigrinhoGame
from src.games.mines import MinesGame
from src.games.crash import CrashGame
from src.games.double import DoubleGame
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
    
    @commands.command(name='tigrinho', aliases=['tiger', 'tigre'])
    async def tigrinho(self, ctx, bet_amount: int):
        """
        Joga Tigrinho (Fortune Tiger) - slot 3x3
        Uso: /tigrinho <valor>
        """
        if not await ensure_not_playing(ctx):
            return
        
        if bet_amount < 10:
            await ctx.send('❌ A aposta mínima é 10 🪙!')
            return
        
        if not await self.check_balance(ctx, bet_amount):
            return
        
        start_game(ctx.author.id, 'tigrinho')
        
        try:
            # Create spinning animation
            embed = discord.Embed(
                title='🐅 Tigrinho - Fortune Tiger',
                description='🎰 Girando...',
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
                    description='🎰 Girando...',
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
                await ctx.send('❌ Erro ao processar aposta!')
                return
            
            # Create final result embed
            embed = discord.Embed(
                title='🐅 Tigrinho - Fortune Tiger',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            grid_display = TigrinhoGame.format_grid(grid)
            embed.add_field(name='Resultado', value=f'```\n{grid_display}\n```', inline=False)
            embed.add_field(name='Aposta', value=f'{bet_amount:,} 🪙', inline=True)
            
            if won:
                win_text = '\n'.join(win_descriptions)
                embed.add_field(
                    name='🎉 GANHOU!',
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
            embed.set_footer(text=f'Saldo atual: {user["coins"]:,} 🪙')
            
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
            await ctx.send('❌ A aposta mínima é 10 🪙!')
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
            
            embed.add_field(name='Aposta', value=f'{bet_amount:,} 🪙', inline=True)
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
                
                embed.add_field(name='Aposta', value=f'{bet_amount:,} 🪙', inline=True)
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
                await ctx.send('❌ Erro ao processar aposta!')
                return
            
            # Show final result
            if won:
                embed = discord.Embed(
                    title='🚀 Crash - Cash Out!',
                    description=f'✅ Você sacou em **{target_multiplier:.2f}x**!',
                    color=discord.Color.green()
                )
                embed.add_field(
                    name='🎉 GANHOU!',
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
                    title='🚀 Crash',
                    description=CrashGame.format_crash(crash_point),
                    color=discord.Color.red()
                )
                embed.add_field(
                    name='❌ Perdeu',
                    value=f'{net_change:,} 🪙\nCrash antes do alvo {target_multiplier:.2f}x',
                    inline=False
                )
            
            embed.add_field(name='Aposta', value=f'{bet_amount:,} 🪙', inline=True)
            
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
            await ctx.send('❌ A aposta mínima é 10 🪙!')
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
            
            embed.add_field(name='Sua Aposta', value=bet_color.title(), inline=True)
            embed.add_field(name='Valor', value=f'{bet_amount:,} 🪙', inline=True)
            
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
                embed.add_field(name='Sua Aposta', value=bet_color.title(), inline=True)
                embed.add_field(name='Valor', value=f'{bet_amount:,} 🪙', inline=True)
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
                await ctx.send('❌ Erro ao processar aposta!')
                return
            
            # Show final result
            embed = discord.Embed(
                title='🎡 Double - Resultado',
                color=discord.Color.green() if won else discord.Color.red()
            )
            
            embed.add_field(
                name='Resultado',
                value=DoubleGame.format_result(result),
                inline=False
            )
            
            embed.add_field(name='Sua Aposta', value=bet_color.title(), inline=True)
            embed.add_field(name='Valor', value=f'{bet_amount:,} 🪙', inline=True)
            
            if won:
                embed.add_field(
                    name='🎉 GANHOU!',
                    value=f'+{net_change:,} 🪙 ({multiplier:.0f}x)',
                    inline=False
                )
            else:
                embed.add_field(
                    name='❌ Perdeu',
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
            embed.set_footer(text=f'Saldo atual: {user["coins"]:,} 🪙')
            
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
            await ctx.send('❌ A aposta mínima é 10 🪙!')
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
            embed.add_field(name='Aposta', value=f'{bet_amount:,} 🪙', inline=True)
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
                            title='💣 Mines - Cash Out!',
                            description=f'Você sacou com segurança!',
                            color=discord.Color.green()
                        )
                        
                        grid_display = game.format_grid(reveal_all=True)
                        embed.add_field(name='Grade Final', value=f'```\n{grid_display}\n```', inline=False)
                        embed.add_field(
                            name='🎉 GANHOU!',
                            value=f'+{net_change:,} 🪙 ({multiplier:.2f}x)',
                            inline=False
                        )
                        embed.add_field(name='Tiles Revelados', value=f'{len(game.revealed)}/{game.safe_tiles}', inline=True)
                        
                        user = self.db.get_user(str(ctx.author.id), ctx.author.name)
                        embed.set_footer(text=f'Saldo atual: {user["coins"]:,} 🪙')
                        
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
                                    title='💣 Mines - BOOM!',
                                    description='💥 Você acertou uma mina!',
                                    color=discord.Color.red()
                                )
                                
                                grid_display = game.format_grid(reveal_all=True)
                                embed.add_field(name='Grade Final', value=f'```\n{grid_display}\n```', inline=False)
                                embed.add_field(
                                    name='❌ Perdeu',
                                    value=f'{net_change:,} 🪙',
                                    inline=False
                                )
                                
                                user = self.db.get_user(str(ctx.author.id), ctx.author.name)
                                embed.set_footer(text=f'Saldo atual: {user["coins"]:,} 🪙')
                                
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
                                embed.add_field(name='Aposta', value=f'{bet_amount:,} 🪙', inline=True)
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
                                        title='💣 Mines - LIMPEZA PERFEITA!',
                                        description='🎉 Você revelou todos os tiles seguros!',
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
                                    embed.set_footer(text=f'Saldo atual: {user["coins"]:,} 🪙')
                                    
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
    
    @commands.command(name='jogos', aliases=['games', 'listgames'])
    async def list_games(self, ctx):
        """Lista todos os jogos disponíveis"""
        embed = discord.Embed(
            title='🎰 Jogos de Cassino Disponíveis',
            description='Teste sua sorte e ganhe moedas!',
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name='🐅 Tigrinho (Fortune Tiger)',
            value=f'`{PREFIX}tigrinho <valor>`\nSlot 3x3 com múltiplas linhas de pagamento!',
            inline=False
        )
        
        embed.add_field(
            name='🚀 Crash',
            value=f'`{PREFIX}crash <valor> [multiplicador]`\nMultiplicador cresce até crashar!',
            inline=False
        )
        
        embed.add_field(
            name='🎡 Double',
            value=f'`{PREFIX}double <valor> <cor>`\nAposta em cores: vermelho (2x), preto (2x), branco (14x)',
            inline=False
        )
        
        embed.add_field(
            name='💣 Mines',
            value=f'`{PREFIX}mines <valor> [dificuldade]`\nCampo minado interativo! Dificuldades: facil, medio, dificil, extremo',
            inline=False
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
