import csv
from datetime import datetime


def get_time_window(s3_client, bucket_name: str, log_key: str):
    """dowloads the log csv file
    creates a timestamp
    saves timestamp to log
    returns a tuple with last time and current time

    Args:
        s3_client (boto_s3): boto s3 client
        bucket_name (str): bucket where log is located
        log_key (str): key of where log is in s3

    Returns:
        tuple: (time_last: str, time_current: str)
    """
    s3_client.download_file(bucket_name, log_key, 'logs/last_run_s3.csv')
    time = datetime.now()

    with open('logs/last_run_s3.csv', 'r+') as file:
        last_line = file.readlines()[-1]
        csv_writer = csv.writer(file, delimiter=",")
        csv_writer.writerow([time, "None"])

    s3_client.upload_file('logs/last_run_s3.csv', bucket_name, log_key)
    return (last_line.split(',')[0], str(time))
