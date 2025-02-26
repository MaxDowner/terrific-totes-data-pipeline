import boto3
from moto import mock_aws
import pytest
import os
from src.util.ingress_upload_to_s3 import upload_ingestion_to_s3
from botocore.exceptions import ClientError
import json

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
        object_key = 'test/uploaded_object'
        dummy_object = '{name: hello}'
        
        # Create a mock Bucket
        mock_bucket = test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )
        # Upload a file to the bucket
        function_call = upload_ingestion_to_s3(test_client, bucket_name, object_key, dummy_object)
        listed_buckets = test_client.list_buckets() 

        assert listed_buckets['Buckets'][0]['Name'] == bucket_name

def test_upload_function_writes_the_object_to_the_bucket():
    with mock_aws():
        test_client = boto3.client('s3')
        bucket_name = 'test_bucket1'
        object_key = 'test/uploaded_object'
        dummy_object = '{name: hello}'    

        # Create a mock Bucket
        mock_bucket = test_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
        )

        # Upload a file to the bucket
        function_call = upload_ingestion_to_s3(test_client, bucket_name, object_key, dummy_object)

        listed_objects = test_client.list_objects_v2(
            Bucket=bucket_name
        )
        # Retrieve Object contents
        get_my_object = test_client.get_object(Bucket=bucket_name, Key=object_key)
        object_content = get_my_object['Body'].read().decode('utf-8')

        # Assert 
        assert listed_objects['Contents'][0]['Key'] == object_key
        assert object_content == '{name: hello}' 

def test_upload_function_raises_exception_if_bucket_not_present():
    with mock_aws():
        pass

def test_upload_raise_a_client_error_if_invalid__client_call():
    with mock_aws():
        pass