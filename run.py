"""
Entry point for Macacolândia Music Bot

This script runs the bot from the src package.
"""

if __name__ == '__main__':
    from src.bot import main
    import asyncio
    
    asyncio.run(main())
