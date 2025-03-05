import logging
import json

import boto3

from src.util_2.staff_to_parquet import process_staff
from src.util_2.upload_pq_to_s3 import upload_pq_to_s3
from src.util.get_s3_bucket_name import get_s3_bucket_name
from src.util_2.currency_to_parquet import currency_to_parquet
from src.util_2.design_to_parquet import design_to_parquet
from src.util_2.address_to_parquet import address_to_parquet
from src.util_2.counterparty_to_parquet import counterparty_to_parquet
from src.util_2.sales_to_parquet import sales_to_parquet


logger = logging.getLogger("Processing Lambda logger")
logger.setLevel(logging.INFO)


def processing_lambda_handler(event, context):
    """Lambda that processes the data and upload to s3 bucket"""
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
    # util section - data processing
    # util - currency
    if db_dict.get("currency"):
        currency_to_parquet(db_dict["currency"])
        logger.info("Ran process currency util function")
    # util staff
    if db_dict.get("staff"):
        process_staff(db_dict["staff"])
        logger.info("Ran process staff util function")
    # util - design
    if db_dict.get("design"):
        design_to_parquet(db_dict["design"])
        logger.info("Ran process design util function")
    # util - address
    if db_dict.get("address"):
        address_to_parquet(db_dict["address"])
        logger.info("Ran process address util function")
    # util - counterparty
    if db_dict.get("counterparty"):
        counterparty_to_parquet(db_dict["counterparty"])
        logger.info("Ran process counterparty util function")
    # util - sales order
    if db_dict.get("sales_order"):
        sales_to_parquet(db_dict["sales_order"])
        logger.info("Ran process sales_order util function")

    # upload the pq to s3 bucket
    key_prefix = json_download_key[:-5]
    processed_bucket = get_s3_bucket_name("processed-data")
    upload_pq_to_s3(s3_client, key_prefix, processed_bucket)
    logger.info(
        f'Parquet file(s) uploaded to "s3://{processed_bucket}/{key_prefix}"'
    )
