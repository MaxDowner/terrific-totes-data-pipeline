import json
import boto3

from src.util.ingress import ingress_handler
from src.util.filepath_from_timestamp import filename_from_timestamp
from src.util.get_s3_bucket_name import get_s3_bucket_name
from src.util.ingress_upload_to_s3 import upload_ingestion_to_s3
from src.util.get_secret import get_secret


def ingestion_lambda_handler(event, context):
    """
    Checks for updates in the live database and
    extracts new data and processes the data into
    a JSON output >> sends JSON to 'Ingested-Data' buckets
    """

    # get db details
    secret_name = "Tote-DB"
    region_name = "eu-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager", region_name=region_name
    )
    db_details = get_secret(client, secret_name)

    #  create s3 client
    s3c = boto3.client("s3")
    print('created client')
    # remote last runs log file / time windows
    bucket_name_logs = "totes-s3-logs"
    object_key = "logs/last_run.csv"

    updated_data = ingress_handler(
        db_details, s3c, bucket_name_logs, object_key
    )
    print('got data')
    end_function = True
    for table in updated_data:
        for key in table:
            if isinstance(table[key], list) and table[key]:
                end_function = False
                break
    if end_function:
        return
    timestamp = updated_data[-1]["time_of_update"]
    key = filename_from_timestamp(timestamp) + ".json"
    data_body = json.dumps(updated_data, default=str)
    bucket_name_data = get_s3_bucket_name("ingested-data")
    upload_ingestion_to_s3(s3c, bucket_name_data, key, data_body)
