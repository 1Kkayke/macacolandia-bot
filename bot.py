"""
Backwards compatibility wrapper for bot.py

This file maintains backwards compatibility with the old bot.py entry point.
The actual bot code has been refactored into the src/ package for better organization.

To run the bot, you can still use:
    python bot.py

Or use the new entry point:
    python run.py
"""

if __name__ == '__main__':
    print("⚠️  Note: bot.py has been refactored into the src/ package for better organization.")
    print("    The bot will still run normally, but consider using 'python run.py' instead.\n")
    
    from src.bot import main
    import asyncio
    
    asyncio.run(main())
