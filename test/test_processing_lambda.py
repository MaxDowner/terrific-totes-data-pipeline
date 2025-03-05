from unittest.mock import patch
import os
import glob

from moto import mock_aws
import boto3
import pytest

from src.processing_lambda import processing_lambda_handler


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():  # credentials required for testing
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


events = {
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
                    "name": "ingested-data123456",
                    "ownerIdentity": {"principalId": "EXAMPLE"},
                    "arn": "arn:aws:s3:::ingested-data123456",
                },
                "object": {
                    "key": "2025/03/03/14/37-14.json",
                    "size": 1024,
                    "eTag": "0123456789abcdef0123456789abcdef",
                    "sequencer": "0A1B2C3D4E5F678901",
                },
            },
        }
    ]
}


def clear_temp_pq_files():
    file_list = glob.glob("/tmp/*.parquet")
    for file in file_list:
        os.remove(file)


def test_handler_downloads_the_json_file_from_the_bucket():
    clear_temp_pq_files()
    with mock_aws():
        # Arrange
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/37-14.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        if os.path.exists("/tmp/37-14.json"):
            os.remove("/tmp/37-14.json")

        processing_lambda_handler(events, {})

        assert os.path.exists("/tmp/37-14.json")
        if os.path.exists("/tmp/37-14.json"):
            os.remove("/tmp/37-14.json")
        clear_temp_pq_files()


@patch("src.processing_lambda.process_staff")
def test_staff_util_runs_with_data(mocks_staff):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/37-14.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocks_staff.assert_called_once()
        clear_temp_pq_files()


@patch("src.processing_lambda.process_staff")
def test_staff_util_runs_without_data(mocks_staff):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/00-00.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocks_staff.assert_not_called()
        clear_temp_pq_files()


# currency


@patch("src.processing_lambda.currency_to_parquet")
def test_currency_util_runs_with_data(mocked_currency):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/37-14.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocked_currency.assert_called_once()
        clear_temp_pq_files()


@patch("src.processing_lambda.currency_to_parquet")
def test_currency_util_doesnt_run_without_data(mocked_currency):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/00-00.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocked_currency.assert_not_called()
        clear_temp_pq_files()


# design


@patch("src.processing_lambda.design_to_parquet")
def test_design_util_runs_with_data(mocked_design):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/37-14.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocked_design.assert_called_once()
        clear_temp_pq_files()


@patch("src.processing_lambda.design_to_parquet")
def test_design_util_doesnt_run_without_data(mocked_design):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/00-00.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocked_design.assert_not_called()
        clear_temp_pq_files()


# address


@patch("src.processing_lambda.address_to_parquet")
def test_address_util_runs_with_data(mocked_address):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/37-14.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocked_address.assert_called_once()
        clear_temp_pq_files()


@patch("src.processing_lambda.address_to_parquet")
def test_address_util_doesnt_run_without_data(mocked_address):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/00-00.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocked_address.assert_not_called()
        clear_temp_pq_files()


# counterparty


@patch("src.processing_lambda.counterparty_to_parquet")
def test_counterparty_util_runs_with_data(mocked_counterparty):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/37-14.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocked_counterparty.assert_called_once()
        clear_temp_pq_files()


@patch("src.processing_lambda.counterparty_to_parquet")
def test_counterparty_util_doesnt_run_without_data(mocked_counterparty):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/00-00.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocked_counterparty.assert_not_called()
        clear_temp_pq_files()


# sales_order


@patch("src.processing_lambda.sales_to_parquet")
def test_sales_util_runs_with_data(mocked_sales):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/37-14.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocked_sales.assert_called_once()
        clear_temp_pq_files()


@patch("src.processing_lambda.sales_to_parquet")
def test_sales_util_doesnt_run_without_data(mocked_sales):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/00-00.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocked_sales.assert_not_called()
        clear_temp_pq_files()


@patch("src.processing_lambda.upload_pq_to_s3")
def test_handler_invokes_once_the_upload_pq_to_s3_function(mocked_upload):
    clear_temp_pq_files()
    with mock_aws():
        test_s3_in = boto3.client("s3")
        bucket_name = "ingested-data123456"
        object_key = "2025/03/03/14/37-14.json"
        file = "test_files/37-14.json"

        # Create a mock ingress Bucket
        test_s3_in.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )
        # upload mock file to ingress
        test_s3_in.upload_file(file, bucket_name, object_key)

        # Create a mock processed bucket
        test_s3_out = boto3.client("s3")
        bucket_name = "processed-data123456"

        test_s3_out.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
        )

        processing_lambda_handler(events, {})

        mocked_upload.assert_called_once()
        clear_temp_pq_files()
