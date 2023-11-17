"""Contains general, but useful commands for the bot"""

from discord.ext import commands, tasks
from utils.status import get_random_activity
from bot import Bot


class Status(commands.Cog):
    """Cog for updating the bot's status"""

    def __init__(self, bot) -> None:
        self.bot: Bot = bot

    @tasks.loop(hours=1)
    async def update_activity_task(self):
        """Updates the bot's status every hour"""
        activity = await get_random_activity()
        await self.bot.change_presence(activity=activity)
        self.bot.root.info(f'Updated activity to {activity.name} ({activity.type})')

    @commands.Cog.listener('on_ready')
    async def initial_activity_task(self):
        """Updates the bot's activity on ready"""
        activity = await get_random_activity()
        await self.bot.change_presence(activity=activity)
        self.bot.root.info(f'Set initial activity to {activity.name} ({activity.type})')

async def setup(bot: commands.Bot):
    """Sets up the cog

    Args:
        bot (commands.Bot): The bot logged in
    """
    await bot.add_cog(Status(bot))
