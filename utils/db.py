"""Utilities relating to the database"""
import motor.motor_asyncio as motor

def init_db(hostname: str, port: int, db_name: str, username: str = '', password: str = '') -> motor.AsyncIOMotorDatabase:
    """Initializes and returns the MongoDB connection

    Returns:
        AsyncIOMotorDatabase: The Motor database instance
    """

    if username != '' or password != '':
        uri = f'mongodb://{username}:{password}@{hostname}:{port}/?authSource=\'admin\''
        db = motor.AsyncIOMotorClient(uri)[db_name]
    else:
        uri = f'mongodb://{hostname}:{port}/{db_name}'
        db = motor.AsyncIOMotorClient(uri)[db_name]
    return db
