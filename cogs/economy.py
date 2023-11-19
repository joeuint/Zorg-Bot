"""Contains resources needed for the economy system"""

import json
import random
import math
from time import time
import discord
import bson
from discord.ext import commands
from discord import app_commands
from bot import Bot
from utils import crud
from utils.checks import has_bankacc

class Item:
    """
    Item in the economy system
    Used for /search
    """
    name: str
    weight: int
    min_val: int
    max_val: int

    def __init__(self, name: str, weight: int, min_val: int, max_val: int) -> None:
        self.name = name
        self.weight = weight
        self.min_val = min_val
        self.max_val = max_val
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

class Economy(commands.Cog):
    """Cog for Economy commands"""

    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

        # Load economy assets
        with open('static/economy.json', encoding='utf-8') as file:
            assets = json.load(file)

        self.items: list[Item] = []

        for item in assets['items']:
            bot.root.debug(f'Loaded {item["name"]}\nWorth: {item["min_val"]}-{item["max_val"]}\nWeight: {item["weight"]}.')
            for _ in range(item['weight']):
                self.items.append(Item(item['name'], item['weight'], item['min_val'], item['max_val']))
        bot.root.info('Loaded all items')

    def format_currency(self, amount: int) -> str:
        """Formats an amount into currency by adding comma seperators & adding currency sign

        Args:
            amount (int)

        Returns:
            str: The formatted string
        """
        amount_str = f'{amount:,}'

        return 'Ƶ' + amount_str

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

    @app_commands.command(name='balance')
    @has_bankacc()
    async def balance(self, interaction: discord.Interaction):
        """Gets the users balance

        Args:
            interaction (discord.Interaction)
        """
        account = await crud.get_economy_user_by_id(self.bot.db, interaction.user.id, interaction.guild.id)

        cash = account['cash']
        bank = account['bank']

        embed = discord.Embed(title='💰 Balance')
        embed.add_field(name='💵 Cash', value=self.format_currency(cash))
        embed.add_field(name='🏦 Bank', value=self.format_currency(bank))
        embed.color = discord.Color.green()

        await interaction.response.send_message(embed=embed)

    @app_commands.checks.cooldown(1, 120, key=lambda i: (i.user.id, i.guild_id))
    @app_commands.command(name='search', description='Search for money')
    @has_bankacc()
    async def search(self, interaction: discord.Interaction) -> None:
        """Searches for money

        Args:
            interaction (discord.Interaction): The bot interaction
        """
        item = random.choice(self.items)

        amount = random.randint(item.min_val, item.max_val)

        await crud.edit_cash_user(self.bot.db, interaction.user.id, interaction.guild_id, amount)

        embed = discord.Embed(title="Item found")
        embed.add_field(name='', value=f'You found {item} worth {self.format_currency(amount)} money!')
        embed.color = discord.Colour.random()

        await interaction.response.send_message(embed=embed)

    @app_commands.checks.cooldown(1, 30, key=lambda i: (i.user.id, i.guild_id))
    @app_commands.command(name='beg', description='Beg for money')
    @has_bankacc()
    async def beg(self, interaction: discord.Interaction):
        """Begs for money

        Args:
            interaction (discord.Interaction): The bot interaction
        """

        amount = random.randint(-50, 100)

        person = [
            'a rich person',
            'Joe Biden',
            'a random person',
            'a homeless person',
            'him',
            'Gerber Life CEO',
            'Jeff Bezos',
            'Bill Gates',
            'Elon Musk',
            'Mark Zuckerberg',
            'the CEO of Roblox',
            'the CEO of Discord',
            'jeff',
            'paul',
            'a clone of you',
            'Bartholomew',
            'Cornelius Chucklebottom',
            'Phineas T. Butterguff',
            'ur mom',
            'freddy',
            'Jake from Statefarm',
            'Spongebob',
            'Doodlebob'
        ]

        positive_responses = [
            f'Here, have {self.format_currency(amount)}',
            f'Here you go peasant, {self.format_currency(amount)} for u',
            f'Whatever, here is {self.format_currency(amount)}',
            f'Fine, here is {self.format_currency(amount)}',
            f'Here, take {self.format_currency(amount)}',
            f'You poor thing, take {self.format_currency(amount)}',
            f'Hopefully this helps, {self.format_currency(amount)}',
            f'I cannot imagine being poor, take {self.format_currency(amount)}',
            f'Just don\'t buy drugs, take {self.format_currency(amount)}',
            f'How desperate are you, take {self.format_currency(amount)}'
        ]

        negative_responses = [
            'Go away loser',
            'Get a job loser',
            'Go away you vermin',
            'No',
            'I dont have any money',
            'Imagine being poor 🤣🤣',
            '💀💀',
            'Ain\'t no way 😭',
            'L + ratio + poor + discord mod',
            'I ain\'t got money',
            'Who do you think I am? a bank?',
            'No one is giving you anything go away',
            'How you just stop being poor',
            'Why should I donate to you?',
            '139.77.179.210',
            'Here, have a job application',
            'Who tf are you!?',
        ]


        embed = discord.Embed(title=random.choice(person), color=0xff0000 if amount < 0 else 0x00ff00)

        embed.add_field(name='', value=random.choice(negative_responses if amount < 0 else positive_responses))
        if amount > 0:
            await crud.edit_cash_user(self.bot.db, interaction.user.id, interaction.guild_id, amount)
        await interaction.response.send_message(embed=embed)

    async def cog_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            current_time = math.ceil(time())
            retry_after = math.ceil(error.retry_after)
            await interaction.response.send_message(f'You are on cooldown! Try again <t:{current_time + retry_after}:R>', ephemeral=True)
        else:
            await interaction.response.send_message(str(error))


async def setup(bot: commands.Bot):
    """Sets up the cog

    Args:
        bot (commands.Bot): The bot logged in
    """
    await bot.add_cog(Economy(bot))
