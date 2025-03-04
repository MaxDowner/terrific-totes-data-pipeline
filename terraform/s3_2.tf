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

## Lambda code - retrieves from s3 bucket 

resource "aws_s3_object" "lambda_2_code" {
  bucket = aws_s3_bucket.processing_code_bucket.bucket
  key    = "processing/function.zip"
  # etag = filemd5(data.archive_file.lambda.output_path) 
  source     = data.archive_file.lambda_2.output_path
  depends_on = [data.archive_file.lambda_2]
}

resource "aws_s3_object" "lambda_2_layer" {
  bucket = aws_s3_bucket.processing_code_bucket.bucket
  key    = "layer/layer.zip"
  # etag   = filemd5(data.archive_file.layer_code.output_path)
  ## source and depends_on below need to be changed to reflect lambda 2 locations
  source = data.archive_file.layer_code.output_path
  depends_on = [data.archive_file.layer_code]
}

resource "aws_s3_object" "utility_layer_2" {
  bucket = aws_s3_bucket.processing_code_bucket.bucket
  key    = "layer/util.zip"
  # etag = filemd5(data.archive_file.util.output_path)
  ## source and depends_on below need to be changed to reflect lambda 2 locations
  source = data.archive_file.util.output_path
  depends_on = [data.archive_file.util]
}



