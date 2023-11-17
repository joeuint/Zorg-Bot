"""Discord check decorators"""
import os
import discord
from discord.ext import commands
from discord import app_commands

from utils.db import init_db
from utils import crud


def can_kick():
    """Returns the predicate"""
    def predicate(interaction: discord.Interaction) -> bool:
        """Checks if the user has the permission to kick members

        Args:
            interaction (discord.Interaction): The interaction that the bot makes

        Returns:
            bool: Returns true if permissions are met
        """
        return interaction.permissions.kick_members
    return app_commands.check(predicate)


def can_ban():
    """Returns the predicate"""
    def predicate(interaction: discord.Interaction) -> bool:
        """Checks if the user has the permission to kick members

        Args:
            interaction (discord.Interaction): The interaction that the bot makes

        Returns:
            bool: Returns true if permissions are met
        """
        return interaction.permissions.ban_members
    return app_commands.check(predicate)


def can_manage_messages():
    """Returns the predicate"""
    def predicate(interaction: discord.Interaction) -> bool:
        """Checks if the user has the permission to kick members

        Args:
            interaction (discord.Interaction): The interaction that the bot makes

        Returns:
            bool: Returns true if permissions are met
        """
        return interaction.permissions.manage_messages
    return app_commands.check(predicate)


def can_manage_nicknames():
    """Returns the predicate"""
    def predicate(interaction: discord.Interaction) -> bool:
        """Checks if the user has the permission to kick members

        Args:
            interaction (discord.Interaction): The interaction that the bot makes

        Returns:
            bool: Returns true if permissions are met
        """
        return interaction.permissions.manage_nicknames
    return app_commands.check(predicate)

def check_hierarchy(member: discord.Member, user: discord.Member, guild: discord.Guild, bot: commands.Bot) -> bool:
    """Checks if user is high enough in the role hierarchy to perform an action

    Args:
        member (discord.Member): The victim
        user (discord.Member): The invocator
        guild (discord.Guild): The guild

    Returns:
        bool: Returns False if not authorized
    """
    if member.top_role >= user.top_role and user.id != guild.owner_id:
        return False
    if member.id in (guild.owner_id, bot.user.id):
        return False
    return True

def has_bankacc():
    # TODO: Maybe the decorator can accept self?
    """Returns the predicate"""
    async def predicate(interaction: discord.Interaction) -> bool:
        """Check if a user's bank account exists

        Args:
            interaction (discord.Interaction)

        Returns:
            bool: Whether the user has an account or not
        """
        # I'm way too tired to do this better
        database = init_db(os.getenv('MONGO_HOSTNAME'), int(os.getenv('MONGO_PORT')), os.getenv('MONGO_DB'))

        if await crud.get_economy_user_by_id(database, interaction.user.id, interaction.guild_id) is None:
            raise app_commands.CheckFailure("You do not have a bank account. To get one, please run /openaccount.")
        return True
    return app_commands.check(predicate)
