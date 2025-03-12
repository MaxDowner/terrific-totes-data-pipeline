import boto3
import logging
from src.util.get_secret import get_secret
from src.util_3.load_to_warehouse import load_to_dw


logger = logging.getLogger("Processing Lambda logger")
logger.setLevel(logging.INFO)


def warehouse_lambda_handler(event, context):
    """Lambda function that populates datawarehouse with updated information
    from a bucket of processed data
    Args:
        event (dict): S3 Put event triggered by data entering processed bucket  
        context (dict): empty dictionary in this function
        
    Raises:
        e1: Unable to download from S3 error
        e2: Unable to access secrets error
        e3: Unable to update the data warehouse error
    
    Returns:
        [str, str, str]: processing bucket, download key, table name
    """
    processing_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    parquet_download_key = event["Records"][0]["s3"]["object"]["key"]
    table_name = parquet_download_key[29:-8]
    logger.info(f"Attempting to download {parquet_download_key}")
    s3_client = boto3.client("s3")
    filepath = '/tmp/downloaded_file.parquet'

    try:
        s3_client.download_file(
            processing_bucket, parquet_download_key, filepath
        )
        logger.info("Successfully downloaded file")
    except Exception as e1:
        logger.error(e1)
        return

    sm_client = boto3.client('secretsmanager')
    try:
        warehouse_creds = get_secret(sm_client, 'totes-data-warehouse')
        logger.info("Successfully retrieved warehouse credentials")
    except Exception as e2:
        logger.error(e2)
        return

    try:
        load_to_dw(warehouse_creds, filepath, table_name)
        logger.info("Successfully updated the data warehouse")
    except Exception as e3:
        logger.error(e3)
        return

    return [processing_bucket, parquet_download_key, table_name]
