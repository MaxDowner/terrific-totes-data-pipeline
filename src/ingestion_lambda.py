import json

import boto3

from src.util.ingress import ingress_handler
from src.util.filepath_from_timestamp import filename_from_timestamp
from src.util.get_s3_bucket_name import get_s3_bucket_name
from src.util.ingress_upload_to_s3 import upload_ingestion_to_s3

def ingestion_lambda_handler(event, context):
    # Retrieve all data into data dumps list
    # updated_data = ingress_handler()
    # timestamp = updated_data[-1]["time_of_update"]
    # key_minus_suffix = filepath_from_timestamp(timestamp)
    #   -> filepath of format 1970/01/01/00/00-00 with file suffix to be decided upon
    # convert ingress_handler output (updated_data) to filetype
    # bn = get_s3_bucket_name('ingestion-data')
    # s3c = boto.client("s3")
    # ingress_upload_to_s3(s3c, bn, key_minus_suffix(plius suffix), updated_data)
    updated_data = ingress_handler()
    end_function = True
    for table in updated_data:
        for key in table:
            if isinstance(table[key], list) and table[key]:
                end_function = False
                break
    if end_function:
        return
    timestamp = updated_data[-1]["time_of_update"]
    key = filename_from_timestamp(timestamp) + '.json'
    data_body = json.dumps(updated_data)
    bucket_name = get_s3_bucket_name('ingestion-data-')
    s3c = boto3.client("s3")
    upload_ingestion_to_s3(
        s3c,
        bucket_name,
        key,
        data_body)