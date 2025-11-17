"""General commands cog - Help and utility commands"""

import discord
from discord.ext import commands
from src.config import PREFIX


class General(commands.Cog):
    """General utility commands"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['ajuda', 'h'])
    async def help_command(self, ctx):
        """Mostra todos os comandos disponíveis"""
        embed = discord.Embed(
            title='🎮 Bot Macacolândia - Comandos',
            description='Bot completo de música, cassino e diversão!',
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name='🎵 Música',
            value=(
                f'`{PREFIX}play <url/busca>` - Toca uma música\n'
                f'`{PREFIX}pause` - Pausa a música\n'
                f'`{PREFIX}skip` - Pula música\n'
                f'`{PREFIX}queue` - Ver fila\n'
                f'`{PREFIX}volume <0-100>` - Ajustar volume'
            ),
            inline=False
        )
        
        embed.add_field(
            name='💰 Economia',
            value=(
                f'`{PREFIX}saldo` - Ver seu saldo\n'
                f'`{PREFIX}diario` - Recompensa diária\n'
                f'`{PREFIX}transferir <@user> <valor>` - Transferir moedas\n'
                f'`{PREFIX}ranking` - Top 10 jogadores\n'
                f'`{PREFIX}conquistas` - Ver suas conquistas'
            ),
            inline=False
        )
        
        embed.add_field(
            name='🎰 Jogos de Cassino',
            value=(
                f'`{PREFIX}slots <valor>` - Caça-níqueis\n'
                f'`{PREFIX}roleta <valor> <tipo> <aposta>` - Roleta\n'
                f'`{PREFIX}dados <valor> <tipo>` - Dados\n'
                f'`{PREFIX}blackjack <valor>` - Blackjack (21)\n'
                f'`{PREFIX}coinflip <valor> <cara/coroa>` - Cara ou coroa\n'
                f'`{PREFIX}jogos` - Listar todos os jogos'
            ),
            inline=False
        )
        
        embed.add_field(
            name='🎉 Diversão',
            value=(
                f'`{PREFIX}piada` - Piada aleatória\n'
                f'`{PREFIX}trivia` - Quiz com recompensa\n'
                f'`{PREFIX}enquete <min> "pergunta" "op1" "op2"` - Criar enquete\n'
                f'`{PREFIX}8ball <pergunta>` - Bola mágica 8'
            ),
            inline=False
        )
        
        embed.add_field(
            name='📊 Info',
            value=(
                f'`{PREFIX}historico` - Ver transações\n'
                f'`{PREFIX}help` - Este menu de ajuda'
            ),
            inline=False
        )
        
        embed.set_footer(text=f'Use {PREFIX}<comando> para executar | Aposta mínima: 10 🪙')
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(General(bot))
