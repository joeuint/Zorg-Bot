"""Status utilities for the bot"""
import json
from random import choice
from typing import List, Dict
import os
import discord

dirname = os.path.dirname(__file__)

STATUS_FILE = os.path.join(dirname, '../static/activities.json')

async def get_random_activity() -> Dict[str, str]:
    """Gets a random activity from STATUS_FILE"""
    with open(STATUS_FILE, 'r', encoding='UTF-8') as json_file:
        json_data: List[dict] = json.load(json_file)
        status = choice(json_data)
        activity_type = status.get('type')
        message = status.get('message')
        if activity_type == 'Playing':
            activity = discord.Game(name=message)
        elif activity_type == 'Listening to':
            activity = discord.Activity(type=discord.ActivityType.listening, name=message)
        elif activity_type == 'Watching':
            activity = discord.Activity(type=discord.ActivityType.watching, name=message)
        return activity
