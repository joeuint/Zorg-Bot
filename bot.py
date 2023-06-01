"""This is where the bot's main code is in."""

# Third Party Imports
import os
import logging
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorDatabase

# Discord.py
import discord
from discord.ext import commands

# First Party Imports
from utils.logging import logging_setup
from utils.cogs import load_cogs
from utils.db import init_db

class Bot(commands.Bot):
    """An extended version of the discord.py bot class"""
    def __init__(self, prefix, *, intents):
        # pylint: disable=C0103
        self.db: AsyncIOMotorDatabase = init_db(os.getenv('MONGO_HOSTNAME'), int(os.getenv('MONGO_PORT')), os.getenv('MONGO_DB'))
        self.root = logging_setup()
        super().__init__(prefix, intents=intents)

def main() -> None:
    """The main function"""
    load_dotenv()

    token = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.message_content = True

    bot = Bot('%', intents=intents)

    load_cogs(bot)

    @bot.event
    async def on_ready():
        """Prepares the bot when it is ready"""
        bot.root.log(logging.INFO,
                 f'I am logged in as {bot.user.name}#{bot.user.discriminator}')

    @commands.is_owner()
    @bot.command()
    async def sync(ctx: commands.Context):
        """Synchronizes app commands with debug guild

        Args:
            ctx (commands.Context): The context of the interaction
        """
        guild = bot.get_guild(1091153826112872508)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        await ctx.send(f'Synced {len(synced)} commands to {guild.name}!')

    @commands.is_owner()
    @bot.command()
    async def syncglobal(ctx: commands.Context):
        """Synchronizes app commands globally

        Args:
            ctx (commands.Context): The context of the interaction
        """
        synced = await bot.tree.sync()
        await ctx.send(f'Synced {len(synced)} commands globally!')

    bot.run(token, log_handler=None)


if __name__ == '__main__':
    main()
