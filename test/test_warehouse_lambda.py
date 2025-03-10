from src.warehouse_lambda import warehouse_lambda_handler
import pytest
from unittest.mock import patch
import os
import boto3
from moto import mock_aws

@pytest.fixture(scope="function")
def aws_credentials():  # credentials required for testing
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

event = {
    "Records": [
        {
            "eventVersion": "2.0",
            "eventSource": "aws:s3",
            "awsRegion": "eu-west-2",
            "eventTime": "1970-01-01T00:00:00.000Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {"principalId": "EXAMPLE"},
            "requestParameters": {"sourceIPAddress": "127.0.0.1"},
            "responseElements": {
                "x-amz-request-id": "EXAMPLE123456789",
                "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome",
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "testConfigRule",
                "bucket": {
                    "name": "processed-data",
                    "ownerIdentity": {"principalId": "EXAMPLE"},
                    "arn": "arn:aws:s3:::ingested-data123456",
                },
                "object": {
                    "key": "2025/03/03/14/37-14formatted_dim_address.parquet",
                    "size": 1024,
                    "eTag": "0123456789abcdef0123456789abcdef",
                    "sequencer": "0A1B2C3D4E5F678901",
                },
            },
        }
    ]
}

def test_warehouse_lambda_downloads_file(aws_credentials):
    # Arrange
    if os.path.exists("/tmp/downloaded_file.parquet"):
        os.remove("/tmp/downloaded_file.parquet")
    with mock_aws():
        test_client = boto3.client('s3')
        test_client.create_bucket(
            Bucket='processed-data',
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )
        file = 'test_files/44-50formatted_dim_currency.parquet'
        object_key = '2025/03/03/14/37-14formatted_dim_address.parquet'
        # Act
        test_client.upload_file(file, 'processed-data', object_key)
        warehouse_lambda_handler(event, {})
        # Assert
        assert os.path.exists("/tmp/downloaded_file.parquet")

@patch('src.warehouse_lambda.load_to_dw')
def test_warehouse_lambda_does_not_return_error_when_ran_successfully(mock_load, aws_credentials):
    # Arrange
    if os.path.exists("/tmp/downloaded_file.parquet"):
        os.remove("/tmp/downloaded_file.parquet")
    with mock_aws():
        mock_load.return_value = None
        test_client = boto3.client('s3')
        test_client.create_bucket(
            Bucket='processed-data',
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )
        dummy_secret_client = boto3.client('secretsmanager')
        dummy_secret_client.create_secret(
            Name="totes-data-warehouse",
            SecretString='{"username": "user"}'
        )
        file = 'test_files/44-50formatted_dim_currency.parquet'
        object_key = '2025/03/03/14/37-14formatted_dim_address.parquet'
        # Act
        test_client.upload_file(file, 'processed-data', object_key)
        result = warehouse_lambda_handler(event, {})
        # Assert
        assert result[0] == 'processed-data'
        assert result[1] == '2025/03/03/14/37-14formatted_dim_address.parquet'
        assert result[2] == 'dim_address'
        mock_load.assert_called_once()

