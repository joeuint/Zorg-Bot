"""Utilites relating to the database"""
import motor.motor_asyncio as motor

def init_db(hostname: str, port: int, db_name: str) -> motor.AsyncIOMotorDatabase:
    """Initializes and returns the MongoDB connection

    Returns:
        MongoClient: The MongoDB database instance
    """
    # pylint: disable=C0103
    db = motor.AsyncIOMotorClient(hostname, port)[db_name]
    return db
