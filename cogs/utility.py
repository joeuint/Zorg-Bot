"""Contains general, but useful commands for the bot"""

import discord
from discord.ext import commands
from discord import app_commands
from bot import Bot


class Utility(commands.Cog):
    """Cog for Utility commands"""

    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @app_commands.command(name='ping', description='pong')
    async def ping(self, interaction: discord.Interaction) -> None:
        """Returns the ping of the bot

        Args:
            interaction (discord.Interaction): The interaction that the bot has made
        """
        await interaction.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms')


async def setup(bot: commands.Bot):
    """Sets up the cog

    Args:
        bot (commands.Bot): The bot logged in
    """
    await bot.add_cog(Utility(bot))
