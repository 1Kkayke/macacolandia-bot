"""Main bot entry point - Macacolândia Music Bot"""

import discord
from discord.ext import commands
import asyncio
from src.config import TOKEN, PREFIX


async def load_cogs(bot):
    """Load all cogs"""
    # Remove existing cogs to prevent duplicates
    for cog_name in list(bot.cogs.keys()):
        await bot.remove_cog(cog_name)
    
    await bot.load_extension('src.cogs.general')
    await bot.load_extension('src.cogs.music')


async def main():
    """Main function to run the bot"""
    # Discord intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    # Bot instance
    bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

    @bot.event
    async def on_ready():
        print(f'🤖 Bot conectado como {bot.user.name}')
        print(f'📊 ID: {bot.user.id}')
        print(f'🎵 Bot de música Macacolândia está online!')
        print('------')
        await bot.change_presence(activity=discord.Game(name=f'{PREFIX}help | Música 🎵'))

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'❌ Argumento faltando! Use `{PREFIX}help` para ver os comandos.')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(f'❌ Comando não encontrado! Use `{PREFIX}help` para ver os comandos disponíveis.')
        else:
            await ctx.send(f'❌ Ocorreu um erro: {str(error)}')

    # Load cogs
    await load_cogs(bot)

    # Run the bot
    if not TOKEN:
        print('❌ ERRO: Token do Discord não encontrado!')
        print('Por favor, crie um arquivo .env com seu DISCORD_TOKEN')
        return
    
    await bot.start(TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
