import os

import pytest
import boto3
# import moto

from src.util.pg_connection_aws import connect_to_db_AWS, close_connection_AWS


@pytest.fixture(scope="function")
def aws_credentials():  # credentials required for testing
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


def test_connect_to_db_connects():
    secret_name = "Tote-DB"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    assert connect_to_db_AWS(client, secret_name)


def test_connect_to_db_fails_with_wrong_details():
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    # monkeypatch.setenv("PG_USER", "error")
    db = None
    try:
        with pytest.raises(Exception):
            db = connect_to_db_AWS(client, "secret")
    finally:
        if db:
            close_connection_AWS(db)


def test_close_connection():
    secret_name = "Tote-DB"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    db = connect_to_db_AWS(client, secret_name)
    result = db.run("SELECT * FROM STAFF")
    assert isinstance(result, list)
    close_connection_AWS(db)
    with pytest.raises(Exception):
        db.run("SELECT * FROM STAFF")
