import os
import json
import pytest
import boto3
from moto import mock_aws

from src.util.retrieve_time_window import retrieve_time_window


@pytest.fixture(scope="function")
def aws_credentials():  # credentials required for testing
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


def test_no_bucket_exists(aws_credentials):
    # Arrange
    with mock_aws():
        expected = "raise log here"
        # Act
        result = retrieve_time_window()
        # Assert
        assert expected == result


def test_no_previous_object_returns_default_timestamp(aws_credentials):
    # Arrange
    with mock_aws():
        bucket_name = 'ingestion-data-8787685'
        test_client = boto3.client('s3')
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )
        expected = "1970-01-01 00:00:00.000"
        # Act
        result = retrieve_time_window()[0]
        # Assert
        assert expected == result


def test_returns_a_tuple_of_strings(aws_credentials):
    # Arrange
    with mock_aws():
        bucket_name = 'ingestion-data-8787685'
        test_client = boto3.client('s3')
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )
        test_client.put_object(
            Body=json.dumps([
                {'t1': []},
                {'t2': []},
                {'t3': []},
                {'t4': []},
                {'t5': []},
                {'t6': []},
                {'time_of_update': "1970-01-01 00:00:00.000"}
                ]),
            Bucket=bucket_name,
            Key='1970/01/01/'
        )
        # Act
        expected_return_type = tuple
        expected_nested_return_type = str
        result = retrieve_time_window()
        # Assert
        assert isinstance(result, expected_return_type)
        assert isinstance(result[0], expected_nested_return_type)
        assert isinstance(result[1], expected_nested_return_type)
        assert len(result) == 2


def test_returns_a_timestamp_from_a_bucket_object(aws_credentials):
    # Arrange
    with mock_aws():
        bucket_name = 'ingestion-data-8787685'
        test_client = boto3.client('s3')
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )
        test_client.put_object(
            Body=json.dumps([
                {'t1': []},
                {'t2': []},
                {'t3': []},
                {'t4': []},
                {'t5': []},
                {'t6': []},
                {'time_of_update': "1970-01-01 00:00:00.000"}
                ]),
            Bucket=bucket_name,
            Key='1970/01/01/'
        )
        # Act
        expected = "1970-01-01 00:00:00.000"
        result = retrieve_time_window()
        # Assert
        assert result[0] == expected


def test_returns_a_timestamp_from_the_correct_bucket_object(aws_credentials):
    # Arrange
    with mock_aws():
        bucket_name = 'ingestion-data-8787685'
        test_client = boto3.client('s3')
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )
        test_client.put_object(
            Body=json.dumps([
                {'t1': []},
                {'t2': []},
                {'t3': []},
                {'t4': []},
                {'t5': []},
                {'t6': []},
                {'time_of_update': "1970-01-01 00:00:00.000"}
                ]),
            Bucket=bucket_name,
            Key='1970/01/01/'
        )
        test_client.put_object(
            Body=json.dumps([
                {'t1': []},
                {'t2': []},
                {'t3': []},
                {'t4': []},
                {'t5': []},
                {'t6': []},
                {'time_of_update': "2007-09-27 00:00:00.000"}]),
            Bucket=bucket_name,
            Key='2007/09/27/'
        )
        test_client.put_object(
            Body=json.dumps([
                {'t1': []},
                {'t2': []},
                {'t3': []},
                {'t4': []},
                {'t5': []},
                {'t6': []},
                {'time_of_update': "2025-10-05 00:00:00.000"}]),
            Bucket=bucket_name,
            Key='2025/10/05/'
        )
        # Act
        times = ["1970-01-01 00:00:00.000",
                 "2007-09-27 00:00:00.000",
                 "2025-10-05 00:00:00.000"]
        result = retrieve_time_window()
        # Assert
        assert result[0] == max(times)
