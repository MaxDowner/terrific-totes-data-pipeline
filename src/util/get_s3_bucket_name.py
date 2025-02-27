import boto3


def get_s3_bucket_name():
    try:
        bucket_name = ""

        s3_resource = boto3.resource("s3")
        for bucket in s3_resource.buckets.all():
            if bucket.name.startswith("ingestion-"):
                bucket_name = bucket.name
        if bucket_name:
            return bucket_name
        else:
            raise Exception("bucket not found")
    except Exception:
        return "bucket not found"
