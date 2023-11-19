"""Utilities relating to the database"""
import motor.motor_asyncio as motor

def init_db(hostname: str, port: int, db_name: str, username: str = '', password: str = '') -> motor.AsyncIOMotorDatabase:
    """Initializes and returns the MongoDB connection

    Returns:
        AsyncIOMotorDatabase: The Motor database instance
    """
    # pylint: disable=C0103

    if username or password:
        db = motor.AsyncIOMotorClient(f'mongodb://{username}:{password}@{hostname}:{port}/{db_name}')
    else:
        db = motor.AsyncIOMotorClient(f'mongodb://{hostname}:{port}/{db_name}')
    return db
