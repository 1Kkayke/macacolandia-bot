"""Bot configuration"""

import os
import platform
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '/')

COOKIES_FILE = Path(__file__).parent.parent / 'youtube_cookies.txt'
USE_COOKIES = COOKIES_FILE.exists()

BROWSER_FOR_COOKIES = None
try:
    import browser_cookie3
    for browser_name in ['chrome', 'edge', 'firefox', 'opera', 'brave']:
        try:
            browser_func = getattr(browser_cookie3, browser_name, None)
            if browser_func:
                list(browser_func(domain_name='.youtube.com'))
                BROWSER_FOR_COOKIES = browser_name
                break
        except:
            continue
except:
    pass

YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': False,
    'no_warnings': False,
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

if USE_COOKIES:
    print("✅ YouTube cookies loaded from file!")
elif BROWSER_FOR_COOKIES:
    print(f"✅ Using cookies from {BROWSER_FOR_COOKIES.title()}!")
else:
    print("⚠️  No YouTube cookies. Some videos may not work.")

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

if platform.system() == 'Windows':
    FFMPEG_EXECUTABLE = os.getenv('FFMPEG_PATH', 'ffmpeg')
else:
    FFMPEG_EXECUTABLE = 'ffmpeg'
