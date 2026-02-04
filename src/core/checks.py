"""Command checks and utilities"""

from discord.ext import commands

active_games = {}


def is_user_playing(user_id: int) -> bool:
    return user_id in active_games


def start_game(user_id: int, game_type: str):
    active_games[user_id] = game_type


def end_game(user_id: int):
    if user_id in active_games:
        del active_games[user_id]


async def ensure_not_playing(ctx):
    if is_user_playing(ctx.author.id):
        await ctx.send('❌ You are already playing! Finish the current game first.')
        return False
    return True
