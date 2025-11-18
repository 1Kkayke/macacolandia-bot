"""Music source for YouTube audio streaming"""

import discord
import asyncio
import yt_dlp as youtube_dl
from src.config import YTDL_FORMAT_OPTIONS, FFMPEG_OPTIONS, FFMPEG_EXECUTABLE


# Create YouTube DL instance
ytdl = youtube_dl.YoutubeDL(YTDL_FORMAT_OPTIONS)


class YTDLSource(discord.PCMVolumeTransformer):
    """Audio source for YouTube videos"""
    
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')
        self.thumbnail = data.get('thumbnail')
        self.requester = None

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        """Create a YTDLSource from a URL or search query"""
        loop = loop or asyncio.get_event_loop()
        try:
            data = await asyncio.wait_for(
                loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream)),
                timeout=60.0  # 60 second timeout
            )
        except asyncio.TimeoutError:
            raise Exception("A busca demorou muito tempo. Tente novamente.")
        except Exception as e:
            # Re-raise with more context
            error_msg = str(e)
            if 'Sign in' in error_msg or 'login' in error_msg.lower():
                raise Exception("YouTube está pedindo login. Tente outra música ou URL.")
            elif 'Video unavailable' in error_msg or 'not available' in error_msg.lower():
                raise Exception("Música não disponível no YouTube.")
            elif 'copyright' in error_msg.lower():
                raise Exception("Música bloqueada por copyright.")
            else:
                raise Exception(f"Erro ao buscar música: {error_msg}")

        if not data:
            raise Exception("Nenhum resultado encontrado para esta busca.")

        if 'entries' in data:
            # Take first item from a playlist
            if len(data['entries']) == 0:
                raise Exception("Nenhum resultado encontrado.")
            data = data['entries'][0]

        if not data:
            raise Exception("Erro ao processar a música.")

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, executable=FFMPEG_EXECUTABLE, **FFMPEG_OPTIONS), data=data)
