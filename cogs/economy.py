"""Contains general, but useful commands for the bot"""

import discord
import bson
from discord.ext import commands
from discord import app_commands
from bot import Bot


class Economy(commands.Cog):
    """Cog for Economy commands"""

    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @app_commands.command(name='openaccount', description='Opens an account in the economy system')
    async def ping(self, interaction: discord.Interaction) -> None:
        """Returns the ping of the bot

        Args:
            interaction (discord.Interaction): The interaction that the bot has made
        """
        starting_cash = 0
        starting_bank = 0

        economy_collection = self.bot.db.get_collection('economy')

        if await economy_collection.count_documents({'$and': [ {'server_id': bson.Int64(interaction.guild_id)}, {'user_id': bson.Int64(interaction.user.id)} ]}) > 0:
            await interaction.response.send_message('You already have an account.')
            return
        await economy_collection.insert_one({
            'server_id': interaction.guild_id,
            'user_id': interaction.user.id,
            'wallet': starting_cash,
            'bank': starting_bank,
        })

        await interaction.response.send_message('Account created!')


async def setup(bot: commands.Bot):
    """Sets up the cog

    Args:
        bot (commands.Bot): The bot logged in
    """
    await bot.add_cog(Economy(bot))
