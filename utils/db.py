"""Utilites relating to the database"""
from pymongo import MongoClient

DB = None

def init_db(hostname, port, db_name) -> MongoClient:
    """Initializes and returns the MongoDB connection

    Returns:
        MongoClient: The MongoDB database instance
    """
    # pylint: disable=W0603
    global DB
    DB = MongoClient(hostname, port)[db_name]
    return DB
