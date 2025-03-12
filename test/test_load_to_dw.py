from moto import mock_aws
import boto3
import pytest
import pyarrow
import os
import shutil
import numpy as np
from unittest.mock import patch, MagicMock
from src.util_3.load_to_warehouse import load_to_dw
from src.util.get_secret import get_secret


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():  # credentials required for testing
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


def test_load_to_dw_retrieves_the_secret_from_secretsmanager():
    # mock 'get_secret'
    with mock_aws():
        test_client = boto3.client("secretsmanager")
        test_client.create_secret(
            Name="Tote-DB",
            SecretString='{"username": "prod", "password": "hello", \
            "dbname": "data", "host": "hosturl", "port": "1223"}',
        )
        secret = get_secret(test_client, "Tote-DB")
        assert secret["username"] == "prod"
        assert secret["password"] == "hello"


@patch("adbc_driver_postgresql.dbapi.connect")
def test_db_connection(mock_connection):
    with mock_aws():
        shutil.copy(
            "test_files/formatted_dim_staff.parquet",
            "/tmp/formatted_dim_staff.parquet",
        )
        client = boto3.client("secretsmanager")
        client.create_secret(
            Name="Tote-DB",
            SecretString='{"username": "prod", "password": "hello", \
            "dbname": "data", "host": "hosturl", "port": "1223"}',
        )
        table_name = "dim_staff"
        file = "/tmp/formatted_dim_staff.parquet"
        secret = get_secret(client, "Tote-DB")
        uri = (
            f"postgresql://{secret['username']}:"
            f"{secret['password']}@{secret['host']}"
            f":{secret['port']}/{secret['dbname']}"
        )
        mock_conn = MagicMock()
        mock_connection.return_value = mock_conn
        load_to_dw(secret, file, table_name)
        # Assert
        mock_connection.assert_called_once_with(uri)  # DB connection called?


@patch("adbc_driver_postgresql.dbapi.connect")  # Mock dw connection
def test_load_to_dw_(mock_connection):
    mock_conn = MagicMock()  # a fake connection object
    mock_cursor = MagicMock()  # a fake cursor
    mock_connection.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    # Mock adbc_ingest
    with mock_aws():
        shutil.copy(
            "test_files/formatted_dim_staff.parquet",
            "/tmp/formatted_dim_staff.parquet",
        )
        table_name = "dim_staff"
        file = "/tmp/formatted_dim_staff.parquet"
        client = boto3.client("secretsmanager")
        client.create_secret(
            Name="Tote-DB",
            SecretString='{"username": "prod", "password": "hello", \
            "dbname": "data", "host": "hosturl", "port": "1223"}',
        )
        secret = get_secret(client, "Tote-DB")
        load_to_dw(secret, file, table_name)
    called_arguments, called_kwargs = mock_cursor.adbc_ingest.call_args
    # Assert adbc_ingest was called with the expected arguments
    assert mock_cursor.adbc_ingest.call_count == 1
    assert called_arguments[0] == "dim_staff"
    assert isinstance(called_arguments[1], pyarrow.Table)


@patch("adbc_driver_postgresql.dbapi.connect")  # Mock dw connection
def test_load_to_dw_returns_int32_instead_of_int64(mock_connection):
    # Arrange
    shutil.copy(
        "test_files/formatted_dim_staff.parquet",
        "/tmp/formatted_dim_staff.parquet",
    )
    mock_conn = MagicMock()  # fake connection object
    mock_cursor = MagicMock()  # fake cursor
    mock_connection.return_value = mock_conn
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    # convert df into a parquet file
    file_path = "/tmp/formatted_dim_staff.parquet"
    # ACT  <<<<<<<<<<<<<<<<<<<<<<<<<<<
    load_to_dw(
        {
            "username": "prod",
            "password": "hello",
            "dbname": "data",
            "host": "hosturl",
            "port": "1223",
        },
        file_path,
        "dim_staff",
    )
    # extract PyArrow table passed to adbc_ingest
    called_arguments, _ = mock_cursor.adbc_ingest.call_args
    arrow_table = called_arguments[1]
    # convert back to df
    result_df = arrow_table.to_pandas()
    # ASSERT <<<<<<<<<<<<<<<<<<<<<<<<<
    assert result_df["staff_id"].dtype == np.int32
    mock_conn.commit.assert_called_once()  # commit() has been called
