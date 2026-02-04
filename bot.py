"""
Backwards compatibility wrapper for bot.py
"""

if __name__ == '__main__':
    print("⚠️  Note: bot.py has been refactored into the src/ package.")
    print("    The bot will still run, but consider using 'python run.py' instead.\n")
    
    from src.bot import main
    import asyncio
    
    asyncio.run(main())
