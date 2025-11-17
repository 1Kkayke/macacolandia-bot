"""Verificações de comandos e utilitários"""

from discord.ext import commands


# Armazena sessões de jogos ativos para prevenir jogos concorrentes
jogos_ativos = {}


def usuario_esta_jogando(id_usuario: int) -> bool:
    """Verifica se o usuário está atualmente em um jogo"""
    return id_usuario in jogos_ativos


def iniciar_jogo(id_usuario: int, tipo_jogo: str):
    """Marca o usuário como jogando um jogo"""
    jogos_ativos[id_usuario] = tipo_jogo


def finalizar_jogo(id_usuario: int):
    """Marca o usuário como tendo finalizado de jogar"""
    if id_usuario in jogos_ativos:
        del jogos_ativos[id_usuario]


async def garantir_nao_jogando(ctx):
    """Verifica que o usuário não está jogando atualmente"""
    if usuario_esta_jogando(ctx.author.id):
        await ctx.send('❌ Você já está jogando! Termine o jogo atual primeiro.')
        return False
    return True
