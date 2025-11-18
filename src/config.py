"""Configuration module for the bot"""

import os
import platform
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '/')

# YouTube DL options
YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
    'extract_flat': False,
    'force_generic_extractor': False,
    'cookiefile': None,
    'age_limit': None,
    'username': None,
    'password': None,
}

# FFmpeg options
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# FFmpeg executable path - cross-platform support
if platform.system() == 'Windows':
    # On Windows, use the local FFmpeg installation if available
    FFMPEG_EXECUTABLE = os.getenv('FFMPEG_PATH', 'ffmpeg')
else:
    # On Linux/Unix (Docker/Dokploy), use system FFmpeg
    FFMPEG_EXECUTABLE = 'ffmpeg'
