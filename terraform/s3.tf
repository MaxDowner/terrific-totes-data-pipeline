resource "aws_s3_bucket" "ingestion_data_bucket" {
    bucket_prefix = var.data_ingestion_bucket_prefix
    tags = {
        bucket_use = "stores ingested data"
    }
}
# THE TWO RESOURCES BELOW, I believe versioning is required for object lock
resource "aws_s3_bucket_versioning" "ingestion_versioning" {
  bucket = aws_s3_bucket.ingestion_data_bucket.bucket
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_object_lock_configuration" "ingestion_object_lock" {
  bucket = aws_s3_bucket.ingestion_data_bucket.bucket
  depends_on = [aws_s3_bucket_versioning.ingestion_versioning.arn]

  rule {
    default_retention {
      # check that governance is the correct mode
      mode = "GOVERNANCE"
      days = 1
    }
  }
}
# THE TWO RESOURCES ABOVE
resource "aws_s3_bucket" "ingestion_code_bucket" {
    bucket_prefix = var.code_ingestion_bucket_prefix
    tags = {
        bucket_use = "ingests data"
    }
}

resource "aws_s3_object" "lambda_code" {
  bucket = aws_s3_bucket.ingestion_code_bucket.bucket
  key = "toy/function.zip"
  source = "${path.module}/../function.zip"
}

resource "aws_s3_object" "layer_code" {
  bucket = aws_s3_bucket.ingestion_code_bucket.bucket
  key = "toy/layer.zip"
  source = "${path.module}/../layer.zip"
}