from pymongo import MongoClient


def init_db() -> MongoClient:
    global db_client
    db_client = MongoClient('localhost', 27017)['astral_bot']
    return db_client
