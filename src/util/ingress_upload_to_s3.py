import boto3
import os
import logging
from botocore.exceptions import ClientError
# from src.util.ingress import ingress_handler

def upload_ingestion_to_s3(s3_client, bucket_name, key, body_content):
    """
    Args:
        bucket_name: a fixed bucket name referred to in the environment variables
        key: an object path name which uses the ingress_handler timestamp
        body_content: a list of dictionaries supplied by the ingress_handler function
    
    Raises:
        ClientError: An unexpected error occurred in execution. Other errors
        result in an informative log message.     
    """ 
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=body_content
        )
    except ClientError as e:
        logging.error(f"Failed to upload data to s3:{str(e)}")