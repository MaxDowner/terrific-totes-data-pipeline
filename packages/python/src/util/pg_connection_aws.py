import logging

from pg8000.native import Connection


logger = logging.getLogger("PGConnectionLogger")
logger.setLevel(logging.INFO)


def connect_to_db(db_details: dict):
    """connects to postgres db using PG8000
    use secret manager util to get db_details

    Args:
        db_details (dict): dict containing login details

    Returns:
        class: PG8000 connection
    """
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
    """closes the db

    Args:
        db (pg8000): dabase connection
    """
    logger.info("Closing connection to remote database")
    db.close()
