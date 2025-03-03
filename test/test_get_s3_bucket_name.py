import os
import boto3

import pytest
from moto import mock_aws

from src.util.get_s3_bucket_name import get_s3_bucket_name


@pytest.fixture(scope="function")
def aws_credentials():  # credentials required for testing
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


def test_returns_a_string():
    assert isinstance(get_s3_bucket_name("ingestion-"), str)


def test_returns_a_string_starting_with_ingestion_live(aws_credentials):
    with mock_aws():
        test_client = boto3.client('s3')
        test_client.create_bucket(
            Bucket='ingestion-data-123456',
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )
        result = get_s3_bucket_name("ingestion-")
        assert "ingestion-" in result


def test_execption(aws_credentials):
    with mock_aws():
        result = get_s3_bucket_name("ingestion-")
        assert result == "bucket not found"
