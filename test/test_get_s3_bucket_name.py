import os

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
    assert isinstance(get_s3_bucket_name(), str)


def test_returns_a_string_starting_with_ingestion_live():
    result = get_s3_bucket_name()
    assert "ingestion-" in result


def test_execption(aws_credentials):
    with mock_aws():
        result = get_s3_bucket_name()
        assert result == "bucket not found"
