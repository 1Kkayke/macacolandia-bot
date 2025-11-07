"""Music source for YouTube audio streaming"""

import discord
import asyncio
import yt_dlp as youtube_dl
from src.config import YTDL_FORMAT_OPTIONS, FFMPEG_OPTIONS


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

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)
