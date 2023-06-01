"""Utility commands relating to cogs"""

import os
import logging
import asyncio
from bot import Bot


def load_cogs(bot: Bot) -> None:
    """Loads all cogs in the ./cogs directory

    Args:
        bot (commands.Bot): The discord bot instance
        root (logging.Logger): The root logger (for logging)
    """
    cog_files = os.listdir(os.path.join(os.getcwd(), './cogs'))
    for file in cog_files:
        if file.endswith('.py'):
            asyncio.run(bot.load_extension(f'cogs.{file[:-3]}'))
            bot.root.log(logging.INFO, f'Loaded extension: {file[:-3]}')
