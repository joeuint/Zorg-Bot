"""Contains general, but useful commands for the bot"""

import random
import discord
import bson
from discord.ext import commands
from discord import app_commands
from bot import Bot
from utils import crud

class Economy(commands.Cog):
    """Cog for Economy commands"""

    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @app_commands.command(name='openaccount', description='Opens an account in the economy system')
    async def openaccount(self, interaction: discord.Interaction) -> None:
        """Opens an economy account

        Args:
            interaction (discord.Interaction): The interaction that the bot has made
        """
        starting_cash = 0
        starting_bank = 0

        economy_collection = self.bot.db.economy

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

    @commands.cooldown(1, 60)
    @app_commands.command(name='search', description='Search for money')
    async def search(self, interaction: discord.Interaction) -> None:
        """Searches for money

        Args:
            interaction (discord.Interaction): The bot interaction
        """
        amount = random.randint(5, 50)

        if not await crud.edit_cash_user(self.bot.db, interaction.user.id, interaction.guild_id, amount):
            await interaction.response.send_message('Failed to update data (Have you opened an account?)', ephemeral=True)
            return
        await interaction.response.send_message(f'You found an item worth {amount} cash!')


async def setup(bot: commands.Bot):
    """Sets up the cog

    Args:
        bot (commands.Bot): The bot logged in
    """
    await bot.add_cog(Economy(bot))
