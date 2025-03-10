def filename_from_timestamp(timestamp):
    '''
    Return a sensible aws object key
    constructed from the time at which the ingestion lambda runs.
    '''

    year = timestamp[:4]
    month = timestamp[5:7]
    day = timestamp[8:10]
    hour = timestamp[11:13]
    minute = timestamp[14:19].replace(":", "-")

    filepath = f"{year}/{month}/{day}/{hour}/{minute}"

    return filepath
