import os
import shutil

import boto3
from moto import mock_aws
import pytest

from src.util_2.upload_pq_to_s3 import upload_pq_to_s3


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():  # credentials required for testing
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


def test_adds_uploads_a_file():
    shutil.copy(
        "test_files/formatted_dim_staff.parquet",
        "/tmp/formatted_dim_staff.parquet",
    )
    with mock_aws():
        # Arrange
        test_s3 = boto3.client("s3")
        bucket_name = "processed-data12345"
        object_key = "2025/03/03/14/37-14-"

        # Create a mock Bucket
        test_s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        listed_objects_before = test_s3.list_objects_v2(Bucket=bucket_name)
        # Upload a file to the bucket
        upload_pq_to_s3(test_s3, object_key, bucket_name)

        listed_objects_after = test_s3.list_objects_v2(Bucket=bucket_name)

        # Assert
        assert (
            listed_objects_before["KeyCount"]
            < listed_objects_after["KeyCount"]
        )


def test_adds_uploads_a_file_with_valid_key_name():
    shutil.copy(
        "test_files/formatted_dim_staff.parquet",
        "/tmp/formatted_dim_staff.parquet",
    )
    with mock_aws():
        # Arrange
        test_s3 = boto3.client("s3")
        bucket_name = "processed-data12345"
        object_key = "2025/03/03/14/37-14-"

        # Create a mock Bucket
        test_s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        upload_pq_to_s3(test_s3, object_key, bucket_name)
        listed_objects = test_s3.list_objects_v2(Bucket=bucket_name)
        # assert listed_objects["Contents"][0]["Key"] == object_key
        for item in listed_objects["Contents"]:
            assert item["Key"].startswith(object_key)
            assert item["Key"].endswith(".parquet")
