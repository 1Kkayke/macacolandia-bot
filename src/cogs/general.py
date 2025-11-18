"""General commands cog - Help and utility commands"""

import discord
from discord.ext import commands
import socket
import os
from src.config import PREFIX


class General(commands.Cog):
    """General utility commands"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', aliases=['ajuda', 'h'])
    async def help_command(self, ctx):
        """Mostra todos os comandos disponíveis"""
        embed = discord.Embed(
            title='🎮 Ow mano, os bagulho que eu faço',
            description='Caralho mano, esse bot faz um monte de parada loca, se vira aí!',
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name='🎵 Música (pra tu ouvir tuas porcaria)',
            value=(
                f'`{PREFIX}play <url/busca>` - Bota pra tocar aí porra\n'
                f'`{PREFIX}pause` - Para essa merda\n'
                f'`{PREFIX}skip` - Pula essa bosta\n'
                f'`{PREFIX}queue` - Vê as parada na fila\n'
                f'`{PREFIX}volume <0-100>` - Aumenta ou diminui essa porra'
            ),
            inline=False
        )
        
        embed.add_field(
            name='💰 Grana (pra tu ver se tá rico ou fudido)',
            value=(
                f'`{PREFIX}saldo` - Vê quanto tu tem de grana aí\n'
                f'`{PREFIX}diario` - Pega teu migalho diário fdp\n'
                f'`{PREFIX}transferir <@user> <valor>` - Manda grana pros parça\n'
                f'`{PREFIX}ranking` - Top 10 dos rico do bagulho\n'
                f'`{PREFIX}conquistas` - Vê tuas conquista aí mano'
            ),
            inline=False
        )
        
        embed.add_field(
            name='🎰 Cassino (pra tu perder tudo)',
            value=(
                f'`{PREFIX}slots <valor>` - Caça níquel do tiozão\n'
                f'`{PREFIX}roleta <valor> <tipo> <aposta>` - Roleta pra tu se foder\n'
                f'`{PREFIX}dados <valor> <tipo>` - Joga uns dados aí\n'
                f'`{PREFIX}blackjack <valor>` - 21 ou tu se fode\n'
                f'`{PREFIX}coinflip <valor> <cara/coroa>` - Cara ou coroa, vamo sortear\n'
                f'`{PREFIX}jogos` - Lista tudo que tem pra tu perder grana'
            ),
            inline=False
        )
        
        embed.add_field(
            name='🎉 Zueira (pra dar risada)',
            value=(
                f'`{PREFIX}piada` - Conta uma piada merda\n'
                f'`{PREFIX}trivia` - Responde uns bagulho aí e ganha grana\n'
                f'`{PREFIX}enquete <min> "pergunta" "op1" "op2"` - Faz uma votação aí\n'
                f'`{PREFIX}8ball <pergunta>` - Pergunta pro oráculo aleatório'
            ),
            inline=False
        )
        
        embed.add_field(
            name='🎭 Memes e Zoeiras (pra rir pra caralho)',
            value=(
                f'`{PREFIX}fato` - Fato aleatório engraçado♪\n'
                f'`{PREFIX}meme` - Meme randômico da net♪\n'
                f'`{PREFIX}memede2025` - Memes de 2025 fdp♪\n'
                f'`{PREFIX}memedodia` - Meme do dia carai♪\n'
                f'`{PREFIX}memedesucesso` - Meme pra motivar♪\n'
                f'`{PREFIX}memedefracasso` - Meme de fracasso mesmo♪\n'
                f'`{PREFIX}memedetroll` - Trollagem pesada♪\n'
                f'`{PREFIX}memedezoacao` - Zueira não tem limites♪\n'
                f'`{PREFIX}memebr` - Memes br puro sangue♪\n'
                f'`{PREFIX}topmeme` - Os top meme de hj'
            ),
            inline=False
        )
        
        embed.add_field(
            name='📊 Info (se liga)',
            value=(
                f'`{PREFIX}historico` - Vê onde tu gastou tua grana\n'
                f'`{PREFIX}help` - Esse menu aqui ó'
            ),
            inline=False
        )
        
        embed.set_footer(text=f'Usa {PREFIX}<comando> aí porra | ♪ = pego da net mesmo')
        await ctx.send(embed=embed)
    
    @commands.command(name='ping', aliases=['latencia', 'lat'])
    async def ping(self, ctx):
        """Mostra latência e informações do bot"""
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title='🏓 Pong caralho!',
            color=discord.Color.green()
        )
        embed.add_field(name='Latência (o delay)', value=f'{latency}ms', inline=True)
        embed.add_field(name='Servidores (onde tô)', value=len(self.bot.guilds), inline=True)
        embed.add_field(name='Host (onde tá rodando)', value=socket.gethostname(), inline=True)
        embed.add_field(
            name='⚠️ Tá triplicando os comando?',
            value='Ó aí mano, deve ter vários bot rodando ao mesmo tempo!\nDesliga o Railway/Dokploy ou tua máquina aí porra.',
            inline=False
        )
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog to the bot"""
    await bot.add_cog(General(bot))
