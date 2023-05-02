import discord
from discord import app_commands


def can_kick():
    def predicate(interaction: discord.Interaction):
        return interaction.permissions.kick_members
    return app_commands.check(predicate)


def can_ban():
    def predicate(interaction: discord.Interaction):
        return interaction.permissions.ban_members
    return app_commands.check(predicate)


def can_manage_messages():
    def predicate(interaction: discord.Interaction):
        return interaction.permissions.manage_messages
    return app_commands.check(predicate)


def can_manage_nicknames():
    def predicate(interaction: discord.Interaction):
        return interaction.permissions.manage_nicknames
    return app_commands.check(predicate)
