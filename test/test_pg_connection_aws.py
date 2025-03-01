import os

import pytest
import boto3
# import moto

from src.util.pg_connection_aws import connect_to_db, close_connection
from src.util.get_secret import get_secret

secret_name = "Tote-DB"
region_name = "eu-west-2"

# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
db_details = get_secret(client, "Tote-DB")


def test_connect_to_db_connects():
    assert connect_to_db(db_details)


def test_connect_to_db_fails_with_wrong_details():
    db = None
    try:
        with pytest.raises(Exception):
            db = connect_to_db({"username" : "not this"})
    finally:
        if db:
            close_connection(db)


def test_close_connection():
    db = connect_to_db(db_details)
    result = db.run("SELECT * FROM STAFF")
    assert isinstance(result, list)
    close_connection(db)
    with pytest.raises(Exception):
        db.run("SELECT * FROM STAFF")
