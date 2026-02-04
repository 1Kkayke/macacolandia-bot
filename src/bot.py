"""Main bot entry point"""

import discord
from discord.ext import commands
import asyncio
import os
import sys
import socket
from src.config import TOKEN, PREFIX
from src.database.db_manager import DatabaseManager

LOCK_FILE = 'bot.lock'
HOSTNAME = socket.gethostname()


async def load_cogs(bot):
    """Load all cogs"""
    loaded = list(bot.extensions.keys())
    
    for extension in loaded:
        try:
            await bot.unload_extension(extension)
        except:
            pass
    
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
            print(f'✅ Loaded: {cog}')
        except Exception as e:
            print(f'❌ Error loading {cog}: {e}')


async def main():
    """Main function to run the bot"""
    if os.path.exists(LOCK_FILE):
        print('⚠️  Bot is already running! Stop the previous instance first.')
        print(f'   If the bot is not running, delete the file: {LOCK_FILE}')
        sys.exit(1)
    
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))
    
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.members = True

        bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
        db = DatabaseManager()

        @bot.event
        async def on_ready():
            if hasattr(bot, '_ready_called'):
                print('🔄 Bot reconnected')
                return
            
            bot._ready_called = True
            print(f'🤖 Bot connected as {bot.user.name}')
            print(f'📊 ID: {bot.user.id}')
            print(f'🎮 Bot is online!')
            print(f'📍 Servers: {len(bot.guilds)}')
            print(f'🖥️  Running on: {HOSTNAME}')
            print('------')

            print('🔄 Syncing servers and members to database...')
            for guild in bot.guilds:
                icon_url = str(guild.icon.url) if guild.icon else None
                db.update_guild(str(guild.id), guild.name, guild.member_count, icon_url)
                
                member_count = 0
                for member in guild.members:
                    if not member.bot:
                        db.add_guild_member(str(guild.id), str(member.id))
                        member_count += 1
                print(f'   Synced {guild.name}: {member_count} members')
                
            print('✅ Servers and members synced!')
            
            command_names = [cmd.name for cmd in bot.commands]
            duplicates = [name for name in command_names if command_names.count(name) > 1]
            
            if duplicates:
                print('❌ ERROR: Duplicate commands detected!')
                print(f'   Duplicate commands: {set(duplicates)}')
                print('   MULTIPLE BOT INSTANCES ARE RUNNING!')
                print('   Stop all other instances (Railway, Dokploy, local)')
                print('------')
            else:
                print('✅ No duplicate commands detected')
                print('------')
            
            await bot.change_presence(activity=discord.Game(name=f'{PREFIX}help | Casino Bot'))

        @bot.event
        async def on_guild_join(guild):
            print(f'➕ Joined server: {guild.name} (ID: {guild.id})')
            icon_url = str(guild.icon.url) if guild.icon else None
            db.update_guild(str(guild.id), guild.name, guild.member_count, icon_url)
            
            for member in guild.members:
                if not member.bot:
                    db.add_guild_member(str(guild.id), str(member.id))

        @bot.event
        async def on_guild_remove(guild):
            print(f'➖ Left server: {guild.name} (ID: {guild.id})')
            db.remove_guild(str(guild.id))

        @bot.event
        async def on_member_join(member):
            if not member.bot:
                db.add_guild_member(str(member.guild.id), str(member.id))

        @bot.event
        async def on_member_remove(member):
            if not member.bot:
                db.remove_guild_member(str(member.guild.id), str(member.id))

        @bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f'❌ Missing argument! Use `{PREFIX}help` to see commands.')
            elif isinstance(error, commands.CommandNotFound):
                pass
            elif isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f'⏰ Wait {error.retry_after:.1f}s to use this command again.')
            else:
                print(f'Error in command {ctx.command}: {error}')
                await ctx.send(f'❌ An error occurred: {str(error)}')

        await load_cogs(bot)

        if not TOKEN:
            print('❌ ERROR: Discord token not found!')
            print('Please create a .env file with your DISCORD_TOKEN')
            return
        
        await bot.start(TOKEN)
    
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)


if __name__ == '__main__':
    asyncio.run(main())
