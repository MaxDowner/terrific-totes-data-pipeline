import boto3
from moto import mock_aws
import pytest
import os
from src.util.ingress_upload_to_s3 import upload_ingestion_to_s3
from botocore.exceptions import ClientError


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
    os.environ["AWS_SECURITY_TOKEN"] = "test"
    os.environ["AWS_SESSION_TOKEN"] = "test"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


def test_upload_function_that_the_bucket_exists():
    with mock_aws():
        test_client = boto3.client('s3')
        bucket_name = 'test_bucket1'
        listed_buckets = test_client.list_buckets()
        assert listed_buckets['Buckets'][0]['Name'] == bucket_name


def test_upload_function_writes_the_object_to_the_bucket():
    with mock_aws():
        test_client = boto3.client('s3')
        bucket_name = 'test_bucket1'
        object_key = 'test/uploaded_object'
        listed_objects = test_client.list_objects_v2(
            Bucket=bucket_name
        )
        # Retrieve Object contents
        get_my_object = test_client.get_object(
            Bucket=bucket_name,
            Key=object_key
            )
        object_content = get_my_object['Body'].read().decode('utf-8')
        # Assert
        assert listed_objects['Contents'][0]['Key'] == object_key
        assert object_content == '{name: hello}'


def test_upload_function_raises_exception_if_bucket_not_present():
    with mock_aws():
        # setup client
        test_client = boto3.client('s3')
        object_key = 'test/uploaded_object'
        dummy_object = '{name: hello}'
        fake_bucket_name = 'fake_bucket'
        # try to upload a file to a fake bucket
        with pytest.raises(ClientError) as exc:
            upload_ingestion_to_s3(test_client,
                                   fake_bucket_name,
                                   object_key,
                                   dummy_object)
        err = exc.value.response["Error"]
        assert err["Message"] == 'The specified bucket does not exist'
