import os

# from unittest.mock import patch

import pytest
from moto import mock_aws
import boto3
from botocore.exceptions import ClientError

from src.util.get_secret import get_secret


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


def test_get_secret_valid(aws_credentials):
    with mock_aws():
        client = boto3.client("secretsmanager")
        client.create_secret(
            Name="ProdSecrets",
            SecretString='{"username": "prod", "password": "hello"}',
        )

        expected_response = {"username": "prod", "password": "hello"}
        response = get_secret(client, "ProdSecrets")
        assert response == expected_response


def test_get_secret_invalid(aws_credentials):
    with mock_aws():
        client = boto3.client("secretsmanager")
        client.create_secret(
            Name="NotASecret",
            SecretString='{"username": "uhoh", "password": "nonono"}',
        )
        with pytest.raises(ClientError):
            get_secret(client, "ProdSecrets")

def test_get_secret_live():
    secret_name = "test-secret"
    region_name = "eu-west-2"
    # Create a Secrets Manager client
    client = boto3.client('secretsmanager')
    result = get_secret(client, 'test')
    assert result == 'test'