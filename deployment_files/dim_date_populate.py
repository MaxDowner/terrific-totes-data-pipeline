import boto3

from src.util.get_secret import get_secret

def dim_date_populate():
    # connect to db using arrow
    # check for data
    # if none run the file
    #  populate
    client = boto3.client("secretsmanager")
    db_details = get_secret(client, "totes-data-warehouse")
    table_name = "dim_date"