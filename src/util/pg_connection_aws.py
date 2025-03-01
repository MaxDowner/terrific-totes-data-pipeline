import logging

from pg8000.native import Connection

from src.util.get_secret import get_secret

logger = logging.getLogger("PGConnectionLogger")
logger.setLevel(logging.INFO)

def connect_to_db(db_details):
    """Connects to the 'totesys' database using PG8000,
    and environment variables using Python Dotenv."""
    if not db_details:
        logger.error('ERROR - Could not retrieve secret details!')
    logger.info(f"Connecting to remote database {db_details['dbname']}")
    return Connection(
        user=db_details['username'],
        password=db_details['password'],
        database=db_details['dbname'],
        host=db_details['host'],
        port=db_details['port']
    )


def close_connection(db):
    logger.info(f"Closing connection to remote database")
    db.close()
