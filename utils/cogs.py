import os
import logging
import asyncio


def load_cogs(bot, root):
    cog_files = os.listdir(os.path.join(os.getcwd(), './cogs'))
    for file in cog_files:
        if file.endswith('.py'):
            asyncio.run(bot.load_extension(f'cogs.{file[:-3]}'))
            root.log(logging.INFO, f'Loaded extension: {file[:-3]}')
