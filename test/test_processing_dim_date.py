from src.util.pg_connection_aws import connect_to_db, close_connection
import os
import boto3
from unittest.mock import patch
from moto import mock_aws
import pytest


@pytest.fixture(scope="function", autouse=True)
def aws_credentials():  # credentials required for testing
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

query = """
        SELECT 
        day AS date_id,
        EXTRACT(YEAR FROM day)::INTEGER  AS year,
        EXTRACT(MONTH FROM day)::INTEGER  AS month,
        EXTRACT(DAY FROM day)::INTEGER  as day,
        EXTRACT(ISODOW FROM day)::INTEGER AS day_of_week,
        TO_CHAR(day, 'Day') AS day_name,
        TO_CHAR(day, 'Month') as month_name,
        EXTRACT(QUARTER FROM day)::INTEGER  AS quarter
        FROM generate_series('2022-01-01'::date, '2030-12-31'::date, '1 day') AS day;
        """

@patch("src.util.pg_connection_aws.Connection.run")
def test_dim_date_query_returns_response_from_db(mock_query):
    with mock_aws():
        # Arrange
        p