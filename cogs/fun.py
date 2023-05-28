"""Contains commands that are just there for fun"""

# Third-party imports
import random
import aiohttp

# Discord
import discord
from discord.ext import commands
from discord import app_commands
from bot import Bot


async def get_meme():
    """Gets a meme from meme-api

    Returns:
        _type_: _description_
    """
    session = aiohttp.ClientSession()
    data = await session.get('https://meme-api.com/gimme')
    json = await data.json()
    await session.close()
    return json


class Fun(commands.Cog):
    """Cog for Fun commands"""

    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @app_commands.command(name='8ball', description='Shake an 8ball and see what happens!')
    @app_commands.describe(question='The question to ask it')
    # pylint: disable=unused-argument
    async def _8ball(self, interaction: discord.Interaction, question: str) -> None:
        """Ask an 8ball a question

        Args:
            interaction (discord.Interaction): The interaction that the bot has made
            question (str): The question to ask to the 8ball
        """
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        await interaction.response.send_message(random.choice(responses))

    @app_commands.command(name='dice', description='Roll a dice')
    @app_commands.describe(start='The starting number', end='The ending number')
    async def dice(self, interaction: discord.Interaction, start: int = 1, end: int = 6) -> None:
        """Generates a number from 1-6 by default

        Args:
            interaction (discord.Interaction): The interaction that the bot makes
            start (int, optional): starting value. Defaults to 1.
            end (int, optional): ending value. Defaults to 6.
        """
        if start > end:
            await interaction.response.send_message('Your start number cannot be greater than the end number')
            return
        await interaction.response.send_message(random.randint(start, end))

    @app_commands.command(name='coinflip', description='Flip a coin and see what happens!')
    async def coinflip(self, interaction: discord.Interaction) -> None:
        """Sends the user either heads or tails as if you were flipping a coin

        Args:
            interaction (discord.Interaction): The interaction that the bot has made
        """
        await interaction.response.send_message(random.choice(['Heads', 'Tails']))

    @app_commands.command(name='meme', description='Get a random meme')
    async def meme(self, interaction: discord.Interaction) -> None:
        """Fetches a meme from a random api
        Args:
            interaction (discord.Interaction): The interaction that the bot has made
        """
        data = {}
        for _ in range(6):
            data = await get_meme()
            if not data['nsfw']:
                break

        await interaction.response.send_message(data['preview'][2])


async def setup(bot: commands.Bot):
    """Sets up the cog

    Args:
        bot (commands.Bot): The bot logged in
    """
    await bot.add_cog(Fun(bot))
