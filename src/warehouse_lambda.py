import boto3
from src.util.get_secret import get_secret
from src.util.pg_connection_aws import connect_to_db, close_connection


def warehouse_lambda_handler(event, context):

    processing_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    parquet_download_key = event["Records"][0]["s3"]["object"]["key"]
    table_name = parquet_download_key[29:-8]

    s3_client = boto3.client("s3")
    filepath = '/tmp/downloaded_file.parquet'
    try:
        s3_client.download_file(
            processing_bucket, parquet_download_key, filepath
        )
    except:
        pass

    # query = f"""
    #             UPDATE {table_name} such and such    
    #         """

    sm_client = boto3.client('secretsmanager')
    try:
        warehouse_creds = get_secret(sm_client, 'totes-data-warehouse')
    except:
        pass
    
    db = ""
    try:
        db = connect_to_db(warehouse_creds)
        # db.run(query)
    except:
        if db:
            close_connection(db)

    # log success
    return [processing_bucket, parquet_download_key, table_name]
