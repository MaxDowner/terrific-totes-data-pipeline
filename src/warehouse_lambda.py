import boto3
import logging
from src.util.get_secret import get_secret
from src.util_3.load_to_warehouse import load_to_dw


logger = logging.getLogger("Processing Lambda logger")
logger.setLevel(logging.INFO)


def warehouse_lambda_handler(event, context):

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
    except Exception as e:
        logger.error(e)
        return

    sm_client = boto3.client('secretsmanager')
    try:
        warehouse_creds = get_secret(sm_client, 'totes-data-warehouse')
        logger.info("Successfully retrieved warehouse credentials")
    except Exception as e:
        logger.error(e)
        return

    try:
        load_to_dw(warehouse_creds, filepath, table_name)
        logger.info("Successfully updated the data warehouse")
    except Exception as e:
        logger.error(e)
        return

    return [processing_bucket, parquet_download_key, table_name]
