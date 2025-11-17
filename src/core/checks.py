"""Command checks and utilities"""

from discord.ext import commands


# Store active game sessions to prevent concurrent games
active_games = {}


def is_user_playing(user_id: int) -> bool:
    """Check if user is currently in a game"""
    return user_id in active_games


def start_game(user_id: int, game_type: str):
    """Mark user as playing a game"""
    active_games[user_id] = game_type


def end_game(user_id: int):
    """Mark user as finished playing"""
    if user_id in active_games:
        del active_games[user_id]


async def ensure_not_playing(ctx):
    """Check that user is not currently playing"""
    if is_user_playing(ctx.author.id):
        await ctx.send('❌ Você já está jogando! Termine o jogo atual primeiro.')
        return False
    return True
