# imports
import boto3

#function:
def warehouse_lambda_handler(event, context):
    processing_bucket = event["Records"][0]["s3"]["bucket"]["name"] # <<< Bucket to get data from
    parquet_download_key = event["Records"][0]["s3"]["object"]["key"]  # <<< Key to access data
    table_name = parquet_download_key[29:-8]        # << table to update

    s3_client = boto3.client("s3")
    filepath = '/tmp/downloaded_file.parquet'
    try:
        s3_client.download_file(
            processing_bucket, parquet_download_key, filepath
        )
    except:
        pass

    return [processing_bucket, parquet_download_key, table_name]



"""
# Download the parquet file
s3_client.download_file(
    processing_bucket, parquet_download_key, parquet_file_name
)
logger.info(f'Downloaded data to "{parquet_file_name}" inside Lambda')

use local (tmp) parquet file in query

# query = fUPDATE {table_name}  < USING PARQUET SQL SHIZZLE

get secrets for data warehouse
connect to db using warehouse secrets
execute query
close db
log yay

"""