resource "aws_s3_bucket" "ingestion_data_bucket" {
  bucket_prefix = var.data_ingestion_bucket_prefix
  tags = {
    bucket_use = "stores ingested data"
  }
}

## allows eventbridge notifications
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket      = aws_s3_bucket.ingestion_data_bucket.id
  eventbridge = true
  lambda_function {
    lambda_function_arn = aws_lambda_function.processing_lambda_handler_resource.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.processing_lambda_handler_resource.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.ingestion_data_bucket.arn
}


resource "aws_s3_bucket_versioning" "ingestion_versioning" {
  bucket = aws_s3_bucket.ingestion_data_bucket.bucket
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_object_lock_configuration" "ingestion_object_lock" {
  bucket     = aws_s3_bucket.ingestion_data_bucket.bucket
  depends_on = [aws_s3_bucket_versioning.ingestion_versioning]

  rule {
    default_retention {
      mode = "GOVERNANCE"
      days = 1
    }
  }
}

resource "aws_s3_bucket" "ingestion_code_bucket" {
  bucket_prefix = var.code_ingestion_bucket_prefix
  tags = {
    bucket_use = "ingests data"
  }
}

resource "aws_s3_object" "lambda_code" {
  bucket = aws_s3_bucket.ingestion_code_bucket.bucket
  key    = "ingestion/function.zip"
  # etag = filemd5(data.archive_file.lambda.output_path) 
  source     = data.archive_file.lambda.output_path
  depends_on = [data.archive_file.lambda]
}

resource "aws_s3_object" "lambda_layer" {
  bucket = aws_s3_bucket.ingestion_code_bucket.bucket
  key    = "layer/layer.zip"
  source = data.archive_file.layer_code.output_path
  # etag   = filemd5(data.archive_file.layer_code.output_path)
  depends_on = [data.archive_file.layer_code]
}

resource "aws_s3_object" "utility_layer" {
  bucket = aws_s3_bucket.ingestion_code_bucket.bucket
  key    = "layer/util.zip"
  source = data.archive_file.util.output_path
  # etag = filemd5(data.archive_file.util.output_path)
  depends_on = [data.archive_file.util]
}