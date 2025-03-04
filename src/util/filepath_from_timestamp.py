def filename_from_timestamp(timestamp):

    year = timestamp[:4]
    month = timestamp[5:7]
    day = timestamp[8:10]
    hour = timestamp[11:13]
    minute = timestamp[14:19].replace(":", "-")

    filepath = f"{year}/{month}/{day}/{hour}/{minute}"

    return filepath
