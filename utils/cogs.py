"""Utility commands relating to cogs"""

import os
import logging
import asyncio
from discord.ext import commands


def load_cogs(bot: commands.Bot, root: logging.Logger) -> None:
    """Loads all cogs in the ./cogs directory

    Args:
        bot (commands.Bot): The discord bot instance
        root (logging.Logger): The root logger (for logging)
    """
    cog_files = os.listdir(os.path.join(os.getcwd(), './cogs'))
    for file in cog_files:
        if file.endswith('.py'):
            asyncio.run(bot.load_extension(f'cogs.{file[:-3]}'))
            root.log(logging.INFO, f'Loaded extension: {file[:-3]}')
