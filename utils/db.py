"""Utilities relating to the database"""
import motor.motor_asyncio as motor

def init_db(hostname: str, port: int, db_name: str, username: str = '', password: str = '') -> motor.AsyncIOMotorDatabase:
    """Initializes and returns the MongoDB connection

    Returns:
        AsyncIOMotorDatabase: The Motor database instance
    """
    # pylint: disable=C0103

    if username != '' or password != '':
        db = motor.AsyncIOMotorClient(hostname, port, username=username, password=password, auth_source='admin').get_database(db_name)
    else:
        db = motor.AsyncIOMotorClient(hostname, port).get_database(db_name)
    return db
