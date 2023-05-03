"""Discord check decorators"""
import discord
from discord import app_commands


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
