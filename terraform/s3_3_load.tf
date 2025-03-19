## s3 Bucket Provision - stores loading code for lambda (transform stage)

resource "aws_s3_bucket" "loading_code_bucket" {
  bucket_prefix = var.loading_code_bucket_prefix
  tags = {
    bucket_use = "loading lambda data"
  }
}

## Lambda code - retrieves from s3 bucket 

resource "aws_s3_object" "lambda_3_load_code" {
  bucket = aws_s3_bucket.loading_code_bucket.bucket
  key    = "loading/function.zip"
  source     = data.archive_file.lambda_3_load.output_path
  depends_on = [data.archive_file.lambda_3_load]
}

resource "aws_s3_object" "lambda_3_load_layer" {
  bucket = aws_s3_bucket.loading_code_bucket.bucket
  key    = "layer/layer.zip"
  source = data.archive_file.layer_code.output_path
  depends_on = [data.archive_file.layer_code]
}

resource "aws_s3_object" "utility_layer_3_load" {
  bucket = aws_s3_bucket.loading_code_bucket.bucket
  key    = "layer/util_3_load.zip"
  source = data.archive_file.util_3_load.output_path
  depends_on = [data.archive_file.util_3_load, aws_s3_bucket.loading_code_bucket]
}

