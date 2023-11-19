"""Database utilities"""

from motor.motor_asyncio import AsyncIOMotorClient

async def init_db(hostname, port, db_name, username = '', password = ''):
    """Initializes the database

    Args:
        username (str): The username to use
        password (str): The password to use
        hostname (str): The hostname to use
        port (int): The port to use
        db_name (str): The database name to use

    Returns:
        AsyncIOMotorClient: The database instance
    """
    client = AsyncIOMotorClient(f'mongodb://{username}:{password}@{hostname}:{port}/{db_name}?authSource=admin')[db_name]
    return client[db_name]
