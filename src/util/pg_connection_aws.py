import logging

from pg8000.native import Connection

from src.util.get_secret import get_secret

logger = logging.getLogger("PGConnectionLogger")
logger.setLevel(logging.INFO)

def connect_to_db_AWS(sm_client, secret_details):
    """Connects to the 'totesys' database using PG8000,
    and environment variables using Python Dotenv."""
    user_details = get_secret(sm_client, secret_details)
    if not user_details:
        logger.error('ERROR - Could not retrieve secret details!')
    logger.info(f"Connecting to remote database {user_details['dbname']}")
    return Connection(
        user=user_details['username'],
        password=user_details['password'],
        database=user_details['dbname'],
        host=user_details['host'],
        port=user_details['port']
    )


def close_connection_AWS(db):
    logger.info(f"Closing connection to remote database")
    db.close()
