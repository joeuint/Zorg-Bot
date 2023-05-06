"""Utilites relating to the database"""
from pymongo import MongoClient

DB_CLIENT = None

def init_db(hostname, port, db_name) -> MongoClient:
    """Initializes and returns the MongoDB connection

    Returns:
        MongoClient: The MongoDB database instance
    """
    # pylint: disable=W0603
    global DB_CLIENT
    DB_CLIENT = MongoClient('localhost', 27017)['astral_bot']
    return DB_CLIENT
