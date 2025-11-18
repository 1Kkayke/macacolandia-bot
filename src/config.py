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

# Try to detect which browser to use for cookies
# Priority: Chrome > Edge > Firefox
BROWSER_FOR_COOKIES = None
try:
    import browser_cookie3
    # Try browsers in order of preference
    for browser_name in ['chrome', 'edge', 'firefox', 'opera', 'brave']:
        try:
            browser_func = getattr(browser_cookie3, browser_name, None)
            if browser_func:
                # Test if we can access cookies
                list(browser_func(domain_name='.youtube.com'))
                BROWSER_FOR_COOKIES = browser_name
                break
        except:
            continue
except:
    pass

# YouTube DL options
YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,  # Changed to False to see yt-dlp errors
    'no_warnings': False,  # Changed to False to see warnings
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
    'extract_flat': False,
    'force_generic_extractor': False,
    'cookiefile': str(COOKIES_FILE) if USE_COOKIES else None,
    'cookiesfrombrowser': (BROWSER_FOR_COOKIES,) if BROWSER_FOR_COOKIES and not USE_COOKIES else None,
    'age_limit': None,
    'username': None,
    'password': None,
    'extractor_args': {
        'youtube': {
            'player_client': ['ios', 'android', 'web'],
            'skip': ['hls', 'dash'],
        }
    },
}

# Print cookie status on load
if USE_COOKIES:
    print("✅ Cookies do YouTube carregados do arquivo! O bot pode tocar músicas restritas.")
elif BROWSER_FOR_COOKIES:
    print(f"✅ Usando cookies do {BROWSER_FOR_COOKIES.title()}! O bot pode tocar músicas restritas.")
else:
    print("⚠️  Sem cookies do YouTube. Algumas músicas podem não funcionar.")

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
