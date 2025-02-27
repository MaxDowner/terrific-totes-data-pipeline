# from src.util.ingress import ingress_handler

def ingestion_lambda_handler(event, context):
    pass
    # Retrieve all data into data dumps list
    # updated_data = ingress_handler()
    # timestamp = updated_data[-1]["time_of_update"]
    # key_minus_suffix = filepath_from_timestamp(timestamp)
    #   -> filepath of format 1970/01/01/00/00-00 with file suffix to be decided upon
    # convert ingress_handler output (updated_data) to filetype
    # bn = get_s3_bucket_name('ingestion-data')
    # s3c = boto.client("s3")
    # ingress_upload_to_s3(s3c, bn, key_minus_suffix(plius suffix), updated_data)