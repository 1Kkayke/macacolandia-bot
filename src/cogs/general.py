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
            title='🎵 Bot de Música Macacolândia - Comandos',
            description='Aqui estão todos os comandos disponíveis:',
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name='🎵 Reprodução',
            value=(
                f'`{PREFIX}play <url/busca>` - Toca uma música\n'
                f'`{PREFIX}pause` - Pausa a música atual\n'
                f'`{PREFIX}resume` - Retoma a música pausada\n'
                f'`{PREFIX}stop` - Para a música e limpa a fila\n'
                f'`{PREFIX}skip` - Pula para a próxima música\n'
                f'`{PREFIX}leave` - Desconecta o bot do canal'
            ),
            inline=False
        )
        
        embed.add_field(
            name='🔊 Volume',
            value=(
                f'`{PREFIX}volume <0-100>` - Define o volume\n'
                f'`{PREFIX}volumeup` - Aumenta o volume em 10%\n'
                f'`{PREFIX}volumedown` - Diminui o volume em 10%'
            ),
            inline=False
        )
        
        embed.add_field(
            name='📋 Fila',
            value=(
                f'`{PREFIX}queue` - Mostra a fila de músicas\n'
                f'`{PREFIX}nowplaying` - Mostra a música atual\n'
                f'`{PREFIX}clear` - Limpa a fila\n'
                f'`{PREFIX}shuffle` - Embaralha a fila'
            ),
            inline=False
        )
        
        embed.set_footer(text=f'Use {PREFIX}comando para executar um comando')
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(General(bot))
