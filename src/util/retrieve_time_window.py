from datetime import datetime
import json
import boto3

from botocore.exceptions import ParamValidationError

from src.util.get_s3_bucket_name import get_s3_bucket_name


def retrieve_time_window():
    s3_client = boto3.client("s3")
    try:
        bucket_name = get_s3_bucket_name('ingestion-data-')
        objects = s3_client.list_objects_v2(
            Bucket=bucket_name
        )
        if bucket_name == "bucket not found":
            raise Exception("bucket not found")
    except ParamValidationError:
        return "raise log here"
    except Exception as e:
        print(e)
        return "raise log here"
    try:
        object_key = objects['Contents'][-1]["Key"]
        response = s3_client.get_object(
            Bucket=bucket_name,
            Key=object_key
        )
        data = response['Body'].read().decode('utf-8')
        json_data = json.loads(data)
        last_updated_record = json_data[-1]["time_of_update"]
    except Exception:
        last_updated_record = "1970-01-01 00:00:00.000"

    now = str(datetime.now())
    return (last_updated_record, now)
