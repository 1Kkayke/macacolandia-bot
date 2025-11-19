"""Main bot entry point - Macacolândia Music Bot"""

import discord
from discord.ext import commands
import asyncio
import os
import sys
import socket
from src.config import TOKEN, PREFIX
from src.database.db_manager import DatabaseManager

# Lock file to prevent multiple instances
LOCK_FILE = 'bot.lock'
# Get hostname to identify where bot is running
HOSTNAME = socket.gethostname()


async def load_cogs(bot):
    """Load all cogs"""
    # Get list of loaded extensions
    loaded = list(bot.extensions.keys())
    
    # Unload all cogs first to prevent duplicates
    for extension in loaded:
        try:
            await bot.unload_extension(extension)
        except:
            pass
    
    # Load cogs
    cogs_to_load = [
        'src.cogs.general',
        'src.cogs.music',
        'src.cogs.economy',
        'src.cogs.games',
        'src.cogs.fun',
        'src.cogs.memes'
    ]
    
    for cog in cogs_to_load:
        try:
            await bot.load_extension(cog)
            print(f'✅ Carregado: {cog}')
        except Exception as e:
            print(f'❌ Erro ao carregar {cog}: {e}')


async def main():
    """Main function to run the bot"""
    # Check for lock file
    if os.path.exists(LOCK_FILE):
        print('⚠️  Bot já está rodando! Pare a instância anterior primeiro.')
        print(f'   Se o bot não estiver rodando, delete o arquivo: {LOCK_FILE}')
        sys.exit(1)
    
    # Create lock file
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))
    
    try:
        # Discord intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.members = True  # Enable members intent for user tracking

        # Bot instance
        bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
        db = DatabaseManager()

        @bot.event
        async def on_ready():
            # Check if bot is already connected (reconnection)
            if hasattr(bot, '_ready_called'):
                print('🔄 Bot reconectado')
                return
            
            bot._ready_called = True
            print(f'🤖 Bot conectado como {bot.user.name}')
            print(f'📊 ID: {bot.user.id}')
            print(f'🎮 Bot Macacolândia está online!')
            print(f'📍 Servidores: {len(bot.guilds)}')
            print(f'🖥️  Executando em: {HOSTNAME}')
            print('------')

            # Sync guilds and members to database
            print('🔄 Sincronizando servidores e membros com o banco de dados...')
            for guild in bot.guilds:
                icon_url = str(guild.icon.url) if guild.icon else None
                db.update_guild(str(guild.id), guild.name, guild.member_count, icon_url)
                
                # Sync members
                member_count = 0
                for member in guild.members:
                    if not member.bot:
                        db.add_guild_member(str(guild.id), str(member.id))
                        member_count += 1
                print(f'   Synced {guild.name}: {member_count} members')
                
            print('✅ Servidores e membros sincronizados!')
            
            # Check for duplicate commands (multiple instances)
            command_names = [cmd.name for cmd in bot.commands]
            duplicates = [name for name in command_names if command_names.count(name) > 1]
            
            if duplicates:
                print('❌ ERRO: Comandos duplicados detectados!')
                print(f'   Comandos duplicados: {set(duplicates)}')
                print('   MÚLTIPLAS INSTÂNCIAS DO BOT ESTÃO RODANDO!')
                print('   Pare todas as outras instâncias (Railway, Dokploy, local)')
                print('------')
            else:
                print('✅ Nenhum comando duplicado detectado')
                print('------')
            
            await bot.change_presence(activity=discord.Game(name=f'{PREFIX}help | Usa ai porra!'))

        @bot.event
        async def on_guild_join(guild):
            """Log when bot joins a guild"""
            print(f'➕ Entrei no servidor: {guild.name} (ID: {guild.id})')
            icon_url = str(guild.icon.url) if guild.icon else None
            db.update_guild(str(guild.id), guild.name, guild.member_count, icon_url)
            
            # Sync members
            for member in guild.members:
                if not member.bot:
                    db.add_guild_member(str(guild.id), str(member.id))

        @bot.event
        async def on_guild_remove(guild):
            """Log when bot leaves a guild"""
            print(f'➖ Sai do servidor: {guild.name} (ID: {guild.id})')
            db.remove_guild(str(guild.id))

        @bot.event
        async def on_member_join(member):
            """Log when a member joins a guild"""
            if not member.bot:
                db.add_guild_member(str(member.guild.id), str(member.id))

        @bot.event
        async def on_member_remove(member):
            """Log when a member leaves a guild"""
            if not member.bot:
                db.remove_guild_member(str(member.guild.id), str(member.id))

        @bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f'❌ Argumento faltando! Use `{PREFIX}help` para ver os comandos.')
            elif isinstance(error, commands.CommandNotFound):
                pass  # Silencia comando não encontrado para reduzir spam
            elif isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f'⏰ Aguarde {error.retry_after:.1f}s para usar este comando novamente.')
            else:
                print(f'Erro no comando {ctx.command}: {error}')
                await ctx.send(f'❌ Ocorreu um erro: {str(error)}')

        # Load cogs
        await load_cogs(bot)

        # Run the bot
        if not TOKEN:
            print('❌ ERRO: Token do Discord não encontrado!')
            print('Por favor, crie um arquivo .env com seu DISCORD_TOKEN')
            return
        
        await bot.start(TOKEN)
    
    finally:
        # Remove lock file on exit
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)


if __name__ == '__main__':
    asyncio.run(main())
