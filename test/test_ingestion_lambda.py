import os

import pytest
import boto3
from unittest.mock import patch
from moto import mock_aws

from src.ingestion_lambda import ingestion_lambda_handler
from src.util.get_secret import get_secret

secret_name = "Tote-DB"
region_name = "eu-west-2"

# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(service_name="secretsmanager", region_name=region_name)
db_details = get_secret(client, "Tote-DB")


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():  # credentials required for testing
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@patch("src.ingestion_lambda.ingress_handler")
def test_runs_ingress_handler(mocked_ingress):
    with mock_aws():
        client = boto3.client("secretsmanager")
        client.create_secret(
            Name="Tote-DB",
            SecretString='{"username": "prod", "password": "hello", \
            "dbname": "data", "host": "hosturl", "port": "1223"}',
        )
        mocked_ingress.return_value = [
            {"currency": [1]},
            {"staff": [2]},
            {"design": [3]},
            {"address": [4]},
            {"counterparty": [5]},
            {"sales_order": [6]},
            {"time_of_update": "1970-01-01 00:00:00.000"},
        ]
        test_client = boto3.client("s3")
        bucket_name = "ingested-data"
        # Create a mock Bucket
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        ingestion_lambda_handler({}, {})
        mocked_ingress.assert_called_once()


def test_gets_valid_timestamp():
    with mock_aws():
        updated_data = [
            {"currency": [1]},
            {"staff": [2]},
            {"design": [3]},
            {"address": [4]},
            {"counterparty": [5]},
            {"sales_order": [6]},
            {"time_of_update": "1970-01-01 00:00:00.000"},
        ]
        timestamp = updated_data[-1]["time_of_update"]
        assert timestamp == "1970-01-01 00:00:00.000"


@patch("src.ingestion_lambda.ingress_handler")
@patch("src.ingestion_lambda.filename_from_timestamp")
def test_runs_filename_from_timestamp_once(
    mocked_filename_from_timestamp, mocked_ingress
):
    with mock_aws():
        client = boto3.client("secretsmanager")
        client.create_secret(
            Name="Tote-DB",
            SecretString='{"username": "prod", "password": "hello", \
                "dbname": "data", "host": "hosturl", "port": "1223"}',
        )
        mocked_ingress.return_value = [
            {"currency": [1]},
            {"staff": [2]},
            {"design": [3]},
            {"address": [4]},
            {"counterparty": [5]},
            {"sales_order": [6]},
            {"time_of_update": "1970-01-01 00:00:00.000"},
        ]
        test_client = boto3.client("s3")
        bucket_name = "ingested-data"
        # Create a mock Bucket
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        mocked_filename_from_timestamp.return_value = "1970/01/01/00/00-00"
        ingestion_lambda_handler({}, {})
        mocked_filename_from_timestamp.assert_called_once()


@patch("src.ingestion_lambda.ingress_handler")
@patch("src.ingestion_lambda.get_s3_bucket_name")
def test_runs_get_s3_bucket_name_once(
    mocked_get_s3_bucket_name, mocked_ingress
):
    with mock_aws():
        client = boto3.client("secretsmanager")
        client.create_secret(
            Name="Tote-DB",
            SecretString='{"username": "prod", "password": "hello", \
                "dbname": "data", "host": "hosturl", "port": "1223"}',
        )
        mocked_ingress.return_value = [
            {"currency": [1]},
            {"staff": [2]},
            {"design": [3]},
            {"address": [4]},
            {"counterparty": [5]},
            {"sales_order": [6]},
            {"time_of_update": "1970-01-01 00:00:00.000"},
        ]
        test_client = boto3.client("s3")
        bucket_name = "ingestion-data-123456"
        # Create a mock Bucket
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        mocked_get_s3_bucket_name.return_value = "ingestion-data-123456"
        ingestion_lambda_handler({}, {})
        mocked_get_s3_bucket_name.assert_called_once()


@patch("src.ingestion_lambda.ingress_handler")
def test_data_uploaded_to_bucket(mocked_ingress):
    with mock_aws():
        client = boto3.client("secretsmanager")
        client.create_secret(
            Name="Tote-DB",
            SecretString='{"username": "prod", "password": "hello", \
                "dbname": "data", "host": "hosturl", "port": "1223"}',
        )
        mocked_ingress.return_value = [
            {"currency": [1]},
            {"staff": [2]},
            {"design": [3]},
            {"address": [4]},
            {"counterparty": [5]},
            {"sales_order": [6]},
            {"time_of_update": "1970-01-01 00:00:00.000"},
        ]
        test_client = boto3.client("s3")
        bucket_name = "ingested-data"
        # Create a mock Bucket
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        ingestion_lambda_handler({}, {})
        listed_objects = test_client.list_objects_v2(Bucket=bucket_name)
        # Assert
        assert listed_objects["KeyCount"] == 1
