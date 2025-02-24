resource "aws_s3_bucket" "ingestion_data_bucket" {
    bucket_prefix = var.data_ingestion_bucket_prefix
    tags = {
        bucket_use = "stores ingested data"
    }
}

resource "aws_s3_bucket" "ingestion_code_bucket" {
    bucket_prefix = var.code_ingestion_bucket_prefix
    tags = {
        bucket_use = "ingests data"
    }
}