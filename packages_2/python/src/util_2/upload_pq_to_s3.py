import glob


def upload_pq_to_s3(s3_client: object, s3_key_prefix: str, bucket_name: str):
    """scans `/tmp/` folder for generated parquet files
    uploads to requested bucket using the s3 key prefix
    s3_key_prefix is the same as the downloaded json minus json
    i.e '2025/03/03/14/37-14-'
    Args:
        s3_client (object): boto3 s3 client
        s3_key_prefix (str): key prix timestamp
        bucket_name (str): processed data bucket
    """
    file_list = glob.glob('/tmp/*.parquet')
    for file in file_list:
        key = s3_key_prefix + file[5:]
        s3_client.upload_file(file, bucket_name, key)
