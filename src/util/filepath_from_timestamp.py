def filename_from_timestamp(timestamp: str):
    """Return a sensible aws object key
    constructed from the time at which the ingestion lambda runs.

    Args:
        timestamp (str):timstamp calculated in lambda

    Returns:
        str: filepath for s3 key '{year}/{month}/{day}/{hour}/{minute}'
    """

    year = timestamp[:4]
    month = timestamp[5:7]
    day = timestamp[8:10]
    hour = timestamp[11:13]
    minute = timestamp[14:19].replace(":", "-")

    filepath = f"{year}/{month}/{day}/{hour}/{minute}"

    return filepath
