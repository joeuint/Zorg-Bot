"""Utilites relating to the database"""
from pymongo import MongoClient
from pymongo.database import Database

DB: Database = None

def init_db(hostname: str, port: int, db_name: str) -> MongoClient:
    """Initializes and returns the MongoDB connection

    Returns:
        MongoClient: The MongoDB database instance
    """
    # pylint: disable=W0603
    global DB
    DB = MongoClient(hostname, port)[db_name]
    return DB
