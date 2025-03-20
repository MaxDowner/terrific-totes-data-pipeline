import os
import shutil
from datetime import datetime

import boto3
import pytest
from moto import mock_aws

from src.util.get_time_window_s3 import get_time_window


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


shutil.copy(
        "logs/last_run_test.csv",
        "logs/last_run.csv"
    )


# Test the returns
def test_returns_tuple():
    with mock_aws():
        test_client = boto3.client("s3")
        bucket_name = "test_bucket1"
        object_key = "logs/last_run.scv"

        # Create a mock Bucket
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # Upload a file to the bucket
        test_client.upload_file(
            "logs/last_run_test.csv", bucket_name, object_key
        )

        result = get_time_window(test_client, bucket_name, object_key)
        assert isinstance(result, tuple)


def test_tuple_returns_2_strings():
    with mock_aws():
        test_client = boto3.client("s3")
        bucket_name = "test_bucket1"
        object_key = "logs/last_run.scv"

        # Create a mock Bucket
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # Upload a file to the bucket
        test_client.upload_file(
            "logs/last_run_test.csv", bucket_name, object_key
        )
        result = get_time_window(test_client, bucket_name, object_key)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], str)


def test_returns_valid_datetime_format():
    with mock_aws():
        test_client = boto3.client("s3")
        bucket_name = "test_bucket1"
        object_key = "logs/last_run.scv"

        # Create a mock Bucket
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # Upload a file to the bucket
        test_client.upload_file(
            "logs/last_run_test.csv", bucket_name, object_key
        )
        result = get_time_window(test_client, bucket_name, object_key)
        # print(result)
        format = "%Y-%m-%d %H:%M:%S.%f"
        # not liking the 1970 format???
        # print(result[0])
        # date_1_formatted = datetime.strptime(result[0], format)
        # print(date_1_formatted)
        date_2_formatted = datetime.strptime(result[1], format)
        assert result[0] == "2022-01-01 00:00:00.000000"
        assert result[1] == str(date_2_formatted)


# # test the csv


def test_writes_to_csv():
    with mock_aws():
        test_client = boto3.client("s3")
        bucket_name = "test_bucket1"
        object_key = "logs/last_run.scv"

        # Create a mock Bucket
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # Upload a file to the bucket
        test_client.upload_file(
            "logs/last_run_test.csv", bucket_name, object_key
        )
        #  read the file, save number of lines
        with open("logs/last_run_test.csv", "r") as file:
            lines_before = len(file.readlines())
        with open("logs/last_run_test.csv", "rb") as file:
            # Go to the end of the file before the last break-line
            file.seek(-2, os.SEEK_END)
            # Keep reading backward until you find the next break-line
            while file.read(1) != b"\n":
                file.seek(-2, os.SEEK_CUR)
            last_line_before = file.readline().decode()
        # run our cammand, updates the file
        get_time_window(test_client, bucket_name, object_key)
        with open("/tmp/last_run_s3.csv", "r") as file:
            lines_after = len(file.readlines())
            # updated_last_line = file.readlines()[-1]
        with open("/tmp/last_run_s3.csv", "rb") as file:
            # Go to the end of the file before the last break-line
            file.seek(-2, os.SEEK_END)
            # Keep reading backward until you find the next break-line
            while file.read(1) != b"\n":
                file.seek(-2, os.SEEK_CUR)
            last_line_after = file.readline().decode()
        assert last_line_before != last_line_after
        assert lines_after == lines_before + 1


def test_writes_to_csv_to_s3():
    with mock_aws():
        test_client = boto3.client("s3")
        bucket_name = "test_bucket1"
        object_key = "logs/last_run.scv"

        # Create a mock Bucket
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # Upload a file to the bucket
        test_client.upload_file(
            "logs/last_run_test.csv", bucket_name, object_key
        )
        #  read the file, save number of lines
        with open("logs/last_run_test.csv", "r") as file:
            lines_before = len(file.readlines())
        with open("logs/last_run_test.csv", "rb") as file:
            # Go to the end of the file before the last break-line
            file.seek(-2, os.SEEK_END)
            # Keep reading backward until you find the next break-line
            while file.read(1) != b"\n":
                file.seek(-2, os.SEEK_CUR)
            last_line_before = file.readline().decode()
        # run our command, updates the file
        get_time_window(test_client, bucket_name, object_key)
        test_client.download_file(
            bucket_name, object_key, "logs/last_run_s3_downloaded_for_test.csv"
        )
        with open("logs/last_run_s3_downloaded_for_test.csv", "r") as file:
            lines_after = len(file.readlines())
            # updated_last_line = file.readlines()[-1]
        with open("logs/last_run_s3_downloaded_for_test.csv", "rb") as file:
            # Go to the end of the file before the last break-line
            file.seek(-2, os.SEEK_END)
            # Keep reading backward until you find the next break-line
            while file.read(1) != b"\n":
                file.seek(-2, os.SEEK_CUR)
            last_line_after = file.readline().decode()
        assert last_line_before != last_line_after
        assert lines_after == lines_before + 1


def test_adds_time_and_None():
    with mock_aws():
        test_client = boto3.client("s3")
        bucket_name = "test_bucket1"
        object_key = "logs/last_run.scv"

        # Create a mock Bucket
        test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # Upload a file to the bucket
        test_client.upload_file(
            "logs/last_run_test.csv", bucket_name, object_key
        )
        result = get_time_window(test_client, bucket_name, object_key)
        test_client.download_file(
            bucket_name, object_key, "logs/last_run_s3_downloaded_for_test.csv"
        )
        with open("logs/last_run_s3_downloaded_for_test.csv", "rb") as file:
            # Go to the end of the file before the last break-line
            file.seek(-2, os.SEEK_END)
            # Keep reading backward until you find the next break-line
            while file.read(1) != b"\n":
                file.seek(-2, os.SEEK_CUR)
            last_line = file.readline().decode()
        items = last_line.split(",")
        assert items[0] == result[1]
        assert items[1].strip() == "None"


shutil.copy(
        "logs/last_run_test.csv",
        "logs/last_run.csv"
    )
