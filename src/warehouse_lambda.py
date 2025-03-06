# imports

#function:
def warehouse_lambda_handler(event, context):
    processing_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    return processing_bucket
"""
This lambda will be invoked by any updates to PROCESSED-DATA bucket

# BUCKET THAT CREATES EVENT
# print(processing_bucket)
# (HOPEFULLY) LIST OF KEYS OF OBJECTS THAT ARE NEW IN BUCKET
parquet_download_key = event["Records"][0]["s3"]["object"]["key"] < MULTIPLE PARQUET FILES PER INVOKATION???
# print(parquet_download_key)
# MAY BE IRRELEVANT
parquet_file_name = f"/tmp/{parquet_download_key[-10:]}" < CHANGE THIS to START:END OF TIME KEY
# print(parquet_file_name)

s3_client = boto3.client("s3")

Gets those objects from bucket
# ITERATE THROUGH LIST OF OBJECT KEYS

    # Download the parquet file
    s3_client.download_file(
        processing_bucket, parquet_download_key, parquet_file_name
    )
    logger.info(f'Downloaded data to "{parquet_file_name}" inside Lambda')

    # DO SLICING ON OBJECT KEY TO FIND DESTINATION TABLE
    # target_table = key[x:y]  # dim_design
    # query = fUPDATE {target_table}  < USING PARQUET SQL SHIZZLE
    
    get secrets for data warehouse
    connect to db using warehouse secrets
    execute query
    close db
    log yay

"""