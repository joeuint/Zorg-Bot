"""Contains general, but useful commands for the bot"""

import discord
from discord.ext import commands
from discord import app_commands
from bot import Bot


class Settings(commands.GroupCog, name='settings'):
    """Cog for Utility commands"""

    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    # pylint: disable=W0221
    def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.permissions.manage_guild

    @app_commands.command(name='muterole', description='Configure the bot')
    @app_commands.describe(role='The mute role')
    async def muterole(self, interaction: discord.Interaction, role: discord.Role):
        """Sets the muterole for the server

        Args:
            interaction (discord.Interaction): The discord interaction
        """
        settings_collection = self.bot.db.get_collection('settings')
        await settings_collection.update_one(
            { 'server_id': interaction.guild_id },
            { '$set': {'mute_role': role.id} },
            upsert=True
        )
        await interaction.response.send_message(f'Mute role set to {role.name} ({role.id})')

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if error.isinstance(app_commands.errors.CheckFailure):
            await interaction.response.send_message('You need to be able to manage the server to use this command!')

async def setup(bot: commands.Bot):
    """Sets up the cog

    Args:
        bot (commands.Bot): The bot logged in
    """
    await bot.add_cog(Settings(bot))
