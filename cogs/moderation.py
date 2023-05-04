"""Contains general, but useful commands for the bot"""

from random import choices
import string
import discord
from discord.ext import commands
from discord import app_commands
from utils.checks import can_kick, can_ban, can_manage_nicknames


class Moderation(commands.Cog):
    """Cog for Moderation commands"""

    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name='ban', description='Bans a user')
    @app_commands.describe(member='The member to ban.', reason='The reason for the ban', hidden='If the command is visible to the chat')
    @can_ban()
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = 'No reason provided', hidden: bool = False):
        """bans the mentioned user

        Args:
            interaction (discord.Interaction): The interaction that the bot makes
            member (discord.Member): The member to ban
            reason (str, optional): The reason for the ban. Defaults to 'No reason provided'.
            hidden (bool, optional): Hides the message. Defaults to False.
        """
        if reason == '':
            reason = 'No reason Provided'

        if member.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message('You can only ban people below you!', ephemeral=True)
            return
        if member.id == interaction.guild.owner_id:
            await interaction.response.send_message('You cannot ban the owner!', ephemeral=True)
            return
        await member.ban(reason=reason + f' (Banned by {interaction.user.name}#{interaction.user.discriminator})')
        await interaction.response.send_message('Member has been banned', ephemeral=hidden)

    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        """Executes when the ban command fails

        Args:
            interaction (discord.Interaction): The interaction that the bot makes
            error (discord.app_commands.AppCommandError): The exception that occured
        """
        if isinstance(error, discord.app_commands.errors.CommandInvokeError):
            if str(error.__cause__) == '403 Forbidden (error code: 50013): Missing Permissions':
                # Bot missing permissions
                await interaction.response.send_message('I do not have the permissions to do that!', ephemeral=True)

    @app_commands.command(name='kick', description='Kicks a user')
    @app_commands.describe(member='The member to kick.', reason='The reason for the kick', hidden='If the command is visible to the chat')
    @can_kick()
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = 'No reason provided', hidden: bool = False):
        """Kicks the mentioned user

        Args:
            interaction (discord.Interaction): The interaction that the bot makes
            member (discord.Member): The member to ban
            reason (str, optional): The reason for the kick. Defaults to 'No reason provided'.
            hidden (bool, optional): Hides the message. Defaults to False.
        """
        if reason == '':
            reason = 'No reason Provided'

        if member.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message('You can only kick people below you!', ephemeral=True)
            return
        if member.id == interaction.guild.owner_id:
            await interaction.response.send_message('You cannot kick the owner!', ephemeral=True)
            return
        await member.kick(reason=reason + f' (Kicked by {interaction.user.name}#{interaction.user.discriminator})')
        await interaction.response.send_message('Member has been kicked', ephemeral=hidden)

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        """Executes when kick command fails

        Args:
            interaction (discord.Interaction): The interaction that the bot makes
            error (discord.app_commands.AppCommandError): The exception that occurs
        """
        if isinstance(error, discord.app_commands.errors.CommandInvokeError):
            if str(error.__cause__) == '403 Forbidden (error code: 50013): Missing Permissions':
                await interaction.response.send_message('I do not have the permissions to do that!', ephemeral=True)

    @app_commands.command(name='modnick', description='Moderates a user\'s nickname')
    @app_commands.describe(member='The member to moderate')
    @can_manage_nicknames()
    async def mod_nick(self, interaction: discord.Interaction, member: discord.Member):
        """Moderates a user's nickname

        Args:
            interaction (discord.Interaction): The interaction that the bot makes
            member (discord.Member): The member to nickname moderate
        """
        if member.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message('You can only change the nickname of people below you!', ephemeral=True)
            return
        if member.id == interaction.guild.owner_id:
            await interaction.response.send_message('You cannot change the nickname of the owner!', ephemeral=True)
            return
        nickname_id = ''.join(choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=9))
        await member.edit(nick=f'Moderated {nickname_id}')

        await interaction.response.send_message('Nickname Moderated!')


async def setup(bot: commands.Bot):
    """Sets up the cog

    Args:
        bot (commands.Bot): The bot logged in
    """
    await bot.add_cog(Moderation(bot))
