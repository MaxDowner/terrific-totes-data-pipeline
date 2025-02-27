import boto3


def get_s3_bucket_name(name_prefix: str):
    """scans the s3 buckets and returns the bucket with
     requested prefix

    Args:
        name_prefix (str): name prefix to search for

    Raises:
        Exception: if can't locate the bucket

    Returns:
        str: bucket name
    """
    try:
        s3_resource = boto3.resource("s3")
        for bucket in s3_resource.buckets.all():
            if bucket.name.startswith(name_prefix):
                return bucket.name
        raise Exception("bucket not found")
    except Exception:
        return "bucket not found"
