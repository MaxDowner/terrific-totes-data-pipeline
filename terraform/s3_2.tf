## s3 Bucket Provision - stores processed data (transform stage)

resource "aws_s3_bucket" "processed_data_bucket" {
  bucket_prefix = var.processed_data_bucket_prefix
  tags = {
    bucket_use = "stores processed data"
  }
}

## s3 Bucket Provision - stores processing code for lambda (transform stage)

resource "aws_s3_bucket" "processing_code_bucket" {
  bucket_prefix = var.processing_code_bucket_prefix
  tags = {
    bucket_use = "processes data"
  }
}

## allows eventbridge notifications
resource "aws_s3_bucket_notification" "bucket_to_load_notification" {
  bucket      = aws_s3_bucket.processed_data_bucket.id
  eventbridge = true
  lambda_function {
    lambda_function_arn = aws_lambda_function.loading_lambda_handler_resource.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_process_to_load_bucket]
}


resource "aws_lambda_permission" "allow_process_to_load_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.loading_lambda_handler_resource.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.processed_data_bucket.arn
}

## Lambda code - retrieves from s3 bucket 

resource "aws_s3_object" "lambda_2_code" {
  bucket = aws_s3_bucket.processing_code_bucket.bucket
  key    = "processing/function.zip"
  source     = data.archive_file.lambda_2.output_path
  depends_on = [data.archive_file.lambda_2]
}

resource "aws_s3_object" "lambda_2_layer" {
  bucket = aws_s3_bucket.processing_code_bucket.bucket
  key    = "layer/layer.zip"
  source = data.archive_file.layer_code.output_path
  depends_on = [data.archive_file.layer_code]
}

resource "aws_s3_object" "utility_layer_2" {
  bucket = aws_s3_bucket.processing_code_bucket.bucket
  key    = "layer/util.zip"
  source = data.archive_file.util_2.output_path
  depends_on = [data.archive_file.util]
}

resource "aws_s3_object" "refresh_log" {
  bucket = "totes-s3-logs"
  key    = "logs/last_run.csv"
  source = "${path.module}/../logs/last_run_test.csv"
}

