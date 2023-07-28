"""
Database CRUD (Create Read Update Delete) utilities
Contains repeatable code for database querys
"""

import typing
import bson
import motor.motor_asyncio as motor

async def get_economy_user_by_id(database: motor.AsyncIOMotorDatabase, user_id: int, server_id: int) -> typing.Mapping[str, typing.Any]:
    """Uses a user_id and server_id to retrieve a user from economy collection

    Args:
        database (motor.AsyncIOMotorDatabase): The bot database instance
        user_id (int): user_id of target
        server_id (int): server_id where the command was ran
    """
    collection = database.economy
    return await collection.find_one({'$and': [ {'server_id': bson.Int64(server_id)}, {'user_id': bson.Int64(user_id)} ]})

async def edit_cash_user(database: motor.AsyncIOMotorDatabase, user_id: int, server_id: int, amount: int) -> typing.Mapping[str, typing.Any]:
    """Increments users cash by x amount

    Args:
        database (motor.AsyncIOMotorDatabase): The bot database instance
        user_id (int): user_id of target
        server_id (int): server_id where the command was ran
        amount (int): The amount to increment by
    """
    collection = database.economy

    return (await collection.update_one({'$and': [ {'server_id': bson.Int64(server_id)}, {'user_id': bson.Int64(user_id)} ]}, {
        '$inc': {'cash': amount}
    })).matched_count > 0
