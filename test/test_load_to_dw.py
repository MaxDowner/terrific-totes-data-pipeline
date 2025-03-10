# from src.util_3.load_to_warehouse import load_to_dw
# from moto import mock_aws, secretsmanager
# import boto3
# import pytest
# import os
# from unittest.mock import patch

# @pytest.fixture(scope="function", autouse=True)
# def aws_credentials():  # credentials required for testing
#     os.environ["AWS_ACCESS_KEY_ID"] = "testing"
#     os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
#     os.environ["AWS_SECURITY_TOKEN"] = "testing"
#     os.environ["AWS_SESSION_TOKEN"] = "testing"
#     os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


# with mock_aws():
#     client = boto3.client("secretsmanager")
#     client.create_secret(
#         Name="Tote-DB",
#         SecretString='{"username": "prod", "password": "hello", \
#         "dbname": "data", "host": "hosturl", "port": "1223"}',
#     )

# def test1():
#     pass
