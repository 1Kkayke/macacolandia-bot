"""Configuration module for the bot"""

import os
import platform
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '/')

# Check if cookies file exists
COOKIES_FILE = Path(__file__).parent.parent / 'youtube_cookies.txt'
USE_COOKIES = COOKIES_FILE.exists()

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
    'cookiefile': str(COOKIES_FILE) if USE_COOKIES else None,
    'age_limit': None,
    'username': None,
    'password': None,
}

# Print cookie status on load
if USE_COOKIES:
    print("✅ Cookies do YouTube carregados! O bot pode tocar músicas restritas.")
else:
    print("⚠️  Sem cookies do YouTube. Execute 'python extract_cookies.py' se tiver problemas com músicas restritas.")

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
