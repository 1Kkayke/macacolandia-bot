"""
Entry point for the bot
"""

if __name__ == '__main__':
    from src.bot import main
    import asyncio
    
    asyncio.run(main())
