import boto3
import logging
import json
from .util_2.staff_to_parquet import process_staff
from .util_2.upload_pq_to_s3 import upload_pq_to_s3
from .util.get_s3_bucket_name import get_s3_bucket_name


logger = logging.getLogger("Processing Lambda logger")
logger.setLevel(logging.INFO)


def processing_lambda_handler(event, context):
    """ Lambda that processes the data and upload to s3 bucket
    """
    # Retrieving Bucket name & Key Name
    ingestion_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    json_download_key = event["Records"][0]["s3"]["object"]["key"]
    json_file_name = f"/tmp/{json_download_key[-10:]}"

    # print(ingestion_bucket)
    # print(json_download_key)
    # print(json_file_name)

    s3_client = boto3.client("s3")

    # Download the json file
    s3_client.download_file(
        ingestion_bucket, json_download_key, json_file_name
    )
    logger.info(f'Downloaded data to "{json_file_name}" inside Lambda')

    # Unpack JSON file into table names
    with open(json_file_name, "r") as f:
        unpacked_json = json.load(f)

    db_dict = {}
    for item in unpacked_json:
        for key, value in item.items():
            db_dict[key] = value

    # util - currency
    # util section - data processing
    if db_dict.get("staff"):
        process_staff(db_dict["staff"])
        logger.info("Ran process staff util function")
    # util - design
    # util - address
    # util - counterparty
    # util - sales order

    # upload the pq to s3 bucket
    key_prefix = json_download_key[:-5]
    processed_bucket = get_s3_bucket_name("processed-data")
    print(key_prefix)
    upload_pq_to_s3(s3_client, key_prefix, processed_bucket)
    logger.info(
        f'Parquet file(s) uploaded to "s3://{processed_bucket}/{key_prefix}"'
    )
